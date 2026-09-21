"""A static WAN handoff must produce a real path off the site, or be refused.

The operator was asked how the WAN is fed and answered "static". Until now the
answer was validated as present and then ignored: the WAN interface was given
an address out of this platform's own IPAM pool — an address no provider ever
issued — and **no default route was ever emitted**. The run then reported
``COMPLETE-APPLIED`` with ``SERVICE_UP:internet_egress`` passing, because the
canned route table in the test double already carried a default route from
somewhere else.

Two separate falsehoods, both measured before either was fixed:

* the site had no egress, and the design claimed it did;
* the verification that should have caught that was grading a route line
  nobody configured.

These tests pin the fix and the two ways it could silently regress.
"""

from __future__ import annotations

import pytest

from netops_autopilot.engines.design_engine import (
    DesignEngine, parse_static_handoff, static_handoff_device_address)
from netops_autopilot.engines.verification import VerificationPlanner
from netops_autopilot.engines.verification_executor import (
    Outcome, TestSpec, VerificationExecutor)


def _run(scenario="hotel"):
    from netops_autopilot.autopilot.orchestrator import AutopilotEngine
    from netops_autopilot.cli.scenarios import make_scenario_io
    from tests.support.simfabric import SimFabricFactory, make_ledger_stack

    store, key_id, _c, ta = make_ledger_stack()
    fabric = SimFabricFactory(include_access=True, access_behavior="allow")
    io = make_scenario_io(scenario)
    io.append_answers({"bond_confirm": "BOND"})
    engine = AutopilotEngine(store=store, key_id=key_id, io=io, time_authority=ta)
    report = engine.run(
        probe_port_session_factory=lambda p: fabric.probe(p),
        mgmt_session_factory=fabric, port="SIM0", execute=True)
    return fabric, report


def _sent(fabric, device="seed-01"):
    return fabric.open(device, ()).written_config


# ====================================================== the handoff is real
def test_the_wan_takes_the_providers_block_not_this_platforms_pool():
    """The address on the WAN is the one the provider issued."""
    _fabric, report = _run("hotel")   # handoff: static 203.0.113.0/30 gw 203.0.113.1
    wan = {z.zone: z for z in report.design.zones}["wan"]

    assert wan.subnet == "203.0.113.0/30"
    # and it is not the provider's own address
    assert wan.gateway != "203.0.113.1"
    assert wan.gateway == "203.0.113.2"
    assert "wan" in report.design.provider_assigned_zones


def test_a_default_route_to_the_provider_next_hop_reaches_the_wire():
    """Without this line the site has an address and no way out."""
    fabric, report = _run("hotel")

    assert "ip route 0.0.0.0 0.0.0.0 203.0.113.1" in _sent(fabric)
    assert report.final == "COMPLETE-APPLIED"
    # and egress is graded from the routing table this run actually produced
    assert "T018:SERVICE_UP:internet_egress" in report.verification["passed"]


def test_the_default_route_is_planned_with_its_own_inverse():
    """A route that cannot be removed is a change that cannot be rolled back."""
    _fabric, report = _run("hotel")

    planned = [line for rec in report.execution["change_records"]
               for line in (rec.get("rollback_commands") or ())]
    assert any("no ip route 0.0.0.0 0.0.0.0 203.0.113.1" in line
               for line in planned), planned


# ================================================= refusal beats invention
@pytest.mark.parametrize("handoff", [
    "ISP fiber, static IP /30",              # says static, gives nothing
    "static 203.0.113.0/30",                 # block but no next hop
    "static gw 203.0.113.1",                 # next hop but no block
    "static 203.0.113.0/30 gw 10.0.0.1",     # next hop is outside the block
    "Two uplinks, BGP to upstream AS",       # a capability this platform lacks
])
def test_a_static_handoff_without_usable_facts_is_refused(handoff):
    assert parse_static_handoff(handoff) is None


def test_the_design_refuses_rather_than_inventing_a_wan_address():
    """The whole point: no invented address, no invented route."""
    from tests.test_design_engine import _build, _engine_and_intent

    engine, bp, intent = _engine_and_intent()
    design = engine.design(intent=intent, blueprint=bp, report=_build(),
                           answers={"router_device": "core-sw1",
                                    "wan_handoff": "ISP fiber, static IP /30"},
                           site_block_v4="10.50.0.0/16")

    assert design.blocked is True
    assert any(r.startswith("WAN_STATIC_HANDOFF_INCOMPLETE")
               for r in design.blocked_reasons), design.blocked_reasons
    # and no zone was given an address out of thin air
    assert {z.zone for z in design.zones if z.kind == "WAN"} == set()


def test_the_device_address_never_collides_with_the_provider_next_hop():
    block, hop = "203.0.113.0/30", "203.0.113.1"
    assert static_handoff_device_address(block, hop) == "203.0.113.2"
    # if the provider took the first usable, this device takes the next
    assert static_handoff_device_address(block, "203.0.113.2") == "203.0.113.1"


# ============================================ egress is not a vacuous pass
def _grade(route_text: str):
    from netops_autopilot.engines.verification_executor import Evidence

    ex = VerificationExecutor(collector=None, session_for=lambda d, c: None)
    ev = Evidence(device_ref="seed-01", command="show ip route", raw_id="ev-1",
                  event_id="evt-1", sha256="0" * 64, truncated=False,
                  text=route_text)
    spec = TestSpec(test_id="T018:SERVICE_UP:internet_egress",
                    kind="SERVICE_UP", src_zone="", dst_zone="",
                    derivation="internet egress")
    result, why = ex._grade_egress(spec, ev, "seed-01")
    return result, why


_CONNECTED = "C        203.0.113.0/29 is directly connected, Vlan40\n"


def test_a_default_route_via_an_unreachable_next_hop_is_not_egress():
    """This is the false success that was measured, pinned shut."""
    text = (_CONNECTED
            + "S*    0.0.0.0/0 [1/0] via 10.99.0.254\n")
    result, why = _grade(text)

    assert result.outcome is Outcome.FAIL
    assert "10.99.0.254" in why and "no usable egress" in why


def test_a_default_route_via_the_provider_next_hop_is_egress():
    text = (_CONNECTED
            + "S*    0.0.0.0/0 [1/0] via 203.0.113.1\n")
    result, _why = _grade(text)

    assert result.outcome is Outcome.PASS


def test_no_default_route_at_all_is_still_a_failure():
    result, why = _grade(_CONNECTED)

    assert result.outcome is Outcome.FAIL
    assert "no `S* 0.0.0.0/0`" in why
