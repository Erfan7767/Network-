"""The capability the product *ships* must be the capability it *claims*.

Every assertion in this file exists because something in the shipped program
disagreed with something the documentation, the register or a sibling module
said — and the disagreement was invisible, because each side was individually
well-tested.

1. **The adapter registry was never constructed.** ADR-0001 routes every engine
   through ``AdapterRegistry``; the registry, the nine interfaces and the
   Preflight Engine all shipped and all had tests, but no module in ``src/``
   ever built a registry, so ``resolve()`` could only return ``None``.
   ``adapters/bootstrap.default_registry()`` is that binding, and these tests
   hold it to covering every family the platform ships an allowlist for.

2. **The configuration dump was a Cisco command for everybody.** Both readers
   in ``access/executor.py`` sent the literal ``show running-config``; on
   Junos/RouterOS/FortiGate/Aruba/UniFi that is not the configuration, the
   ``except Exception`` swallowed the refusal, and verification silently
   degraded to "state change not confirmed" while looking like a transport
   hiccup. The command now comes from the family's own allowlist, by declared
   purpose.

3. **RouterOS neighbour evidence was silently never collected.** The MNDP
   parser's ``command_ref`` used the space form ``/ip neighbor/print`` while
   the allowlist registers the path form ``/ip/neighbor/print``; the crawl's
   plan is that intersection matched on the exact string, so the command was
   dropped and nothing said so.

4. **A dropped command was invisible in both directions.** ``plan_for``
   answered "what will I send" and nothing answered "what can I read but not
   ask for" — ``CommandStatus.PARSER_MISSING`` was declared and never
   produced. ``plan_gaps_for`` is the complement, and it is what would have
   caught item 3 at the time.
"""

from __future__ import annotations

import pytest

from netops_autopilot.access.allowlist import AllowlistEntry, CommandAllowlist
from netops_autopilot.access.executor import (
    CONFIG_CAPTURE_PURPOSE,
    ConfigExecutor,
    config_capture_command,
)
from netops_autopilot.adapters.bootstrap import (
    DataDrivenCliAdapter,
    build_adapter,
    default_registry,
    families_from_data,
    registered_families,
    split_family,
)
from netops_autopilot.adapters.interfaces import CapabilityState
from netops_autopilot.core.failures import Failure, FailureClass
from netops_autopilot.engines.discovery_crawl import DiscoveryCrawlEngine
from netops_autopilot.parsers.catalog import default_registry as parser_registry
from netops_autopilot.specs_data import specs_data_dir

ALLOWLIST_DIR = specs_data_dir("allowlists")

SIX_FAMILIES = (
    "aruba/arubaos",
    "cisco/ios-xe",
    "fortinet/fortios",
    "juniper/junos",
    "mikrotik/routeros",
    "ubiquiti/unifi",
)


def _allowlist(family: str) -> CommandAllowlist:
    return CommandAllowlist.load_vendor(ALLOWLIST_DIR, family)


def _crawl() -> DiscoveryCrawlEngine:
    engine = DiscoveryCrawlEngine.__new__(DiscoveryCrawlEngine)
    engine._parsers = parser_registry()
    return engine


# ---------------------------------------------------------------- families
def test_every_shipped_allowlist_family_is_registered():
    """Six allowlists exist, so six adapters must ship — no more, no fewer."""
    assert families_from_data() == SIX_FAMILIES
    assert registered_families() == tuple(sorted(split_family(f) for f in SIX_FAMILIES))


def test_the_registry_resolves_an_adapter_for_every_family():
    registry = default_registry()
    for family in SIX_FAMILIES:
        vendor, os_name = split_family(family)
        adapter = registry.resolve(vendor=vendor, os=os_name)
        assert adapter is not None, f"no adapter shipped for {family}"
        assert isinstance(adapter, DataDrivenCliAdapter)
        assert adapter.vendor_family == family


def test_an_unknown_vendor_resolves_to_nothing_rather_than_to_a_guess():
    registry = default_registry()
    assert registry.resolve(vendor="nobody", os="never") is None
    # A real vendor with an os this build does not model is equally unknown.
    assert registry.resolve(vendor="cisco", os="nx-os") is None


def test_split_family_refuses_a_family_string_it_cannot_key_on():
    with pytest.raises(ValueError):
        split_family("cisco")
    with pytest.raises(ValueError):
        split_family("/junos")


# --------------------------------------------------- discovery layer honesty
@pytest.mark.parametrize("family", SIX_FAMILIES)
def test_adapter_layers_are_exactly_what_the_crawl_will_issue(family):
    """An adapter must never advertise a command the crawl would not send.

    Both are the same intersection (parser catalog ∩ READ_ONLY allowlist), so
    the two sets are equal by construction — asserted here so that a future
    change to either side breaks a test instead of breaking a device.
    """
    allowlist = _allowlist(family)
    planned = {cmd for cmd, _parser in _crawl().plan_for(family, allowlist)}
    adapter = build_adapter(family)
    assert set(adapter.discovery_layers) == planned
    for layer in adapter.discovery_layers:
        assert adapter.capability(f"discovery_layer:{layer}") is CapabilityState.SUPPORTED
    assert adapter.capability("discovery_layer:show me everything") \
        is CapabilityState.NOT_SUPPORTED


def test_run_layer_refuses_a_layer_it_did_not_advertise():
    adapter = build_adapter("cisco/ios-xe")
    with pytest.raises(Failure) as exc:
        adapter.run_layer("seed-01", "show me everything")
    assert exc.value.cls is FailureClass.BLOCKED
    assert "NOT_MODELED" in exc.value.causes[0]


def test_run_layer_without_a_session_says_the_session_is_missing():
    adapter = build_adapter("cisco/ios-xe")
    with pytest.raises(Failure) as exc:
        adapter.run_layer("seed-01", "show version")
    assert "SESSION_NOT_OPEN" in exc.value.causes[0]


# --------------------------------------------- configuration-dump honesty
def test_cisco_and_junos_get_their_own_configuration_command():
    """The two families that declare a capture command get exactly theirs.

    Junos is the case that used to be wrong: it was sent ``show
    running-config``, which is not a Junos command at all.
    """
    assert config_capture_command(_allowlist("cisco/ios-xe")) == "show running-config"
    assert config_capture_command(_allowlist("juniper/junos")) == \
        "show configuration | display set"


@pytest.mark.parametrize("family", [
    "fortinet/fortios", "mikrotik/routeros", "aruba/arubaos", "ubiquiti/unifi",
])
def test_a_family_with_no_declared_capture_command_answers_not_modeled(family):
    """Four families declare no configuration dump, so none is invented.

    Borrowing the Cisco spelling here is what made verification vacuous: the
    read failed, the failure was swallowed, and the report said "state change
    not confirmed" — true, but hiding that the platform has no way to read
    this device's configuration at all.
    """
    assert config_capture_command(_allowlist(family)) is None
    adapter = build_adapter(family)
    assert adapter.capability("capture_running_config") is CapabilityState.NOT_SUPPORTED


def test_capture_running_config_names_the_data_gap_not_a_transport_failure():
    adapter = build_adapter("mikrotik/routeros")
    with pytest.raises(Failure) as exc:
        adapter.capture_running_config("rb-01")
    assert exc.value.cls is FailureClass.BLOCKED
    cause = exc.value.causes[0]
    assert "NOT_MODELED" in cause
    assert CONFIG_CAPTURE_PURPOSE in cause, "the cause must name the missing data"


def test_the_executor_uses_the_family_command_never_a_hardcoded_one():
    junos = ConfigExecutor(allowlist=_allowlist("juniper/junos"))
    assert junos.config_capture_command_name == "show configuration | display set"
    routeros = ConfigExecutor(allowlist=_allowlist("mikrotik/routeros"))
    assert routeros.config_capture_command_name is None


def test_the_purpose_marker_is_the_fallback_when_the_well_known_template_is_absent():
    """A family that does not register ``show running-config`` at all — the
    five non-Cisco families — still gets its own capture command through the
    purpose annotation. Junos is the real example:
    ``show configuration | display set``."""
    allowlist = CommandAllowlist((
        AllowlistEntry(template="show full-configuration", cls="READ_ONLY",
                       purpose="configuration (hash baseline)"),
    ))
    assert config_capture_command(allowlist) == "show full-configuration"

    # Both present: the well-known template wins, because it is the backward-
    # compatible answer the merged-allowlist callers (chat targeted changes,
    # orchestrator apply) rely on.
    both = CommandAllowlist((
        AllowlistEntry(template="show running-config", cls="READ_ONLY",
                       purpose="something else entirely"),
        AllowlistEntry(template="show full-configuration", cls="READ_ONLY",
                       purpose="configuration (hash baseline)"),
    ))
    assert config_capture_command(both) == "show running-config"


def test_a_family_that_registers_the_well_known_template_uses_it():
    """The well-known template is checked first: a family that registers it as
    READ_ONLY gets it, regardless of purpose annotation."""
    allowlist = CommandAllowlist((
        AllowlistEntry(template="show running-config", cls="READ_ONLY",
                       purpose="hash baseline"),
    ))
    assert config_capture_command(allowlist) == "show running-config"

    # Nothing registered at all ⇒ no capture path, never an invented one.
    assert config_capture_command(CommandAllowlist((
        AllowlistEntry(template="get system status", cls="READ_ONLY",
                       purpose="identity"),
    ))) is None


def test_a_capture_command_that_is_not_read_only_is_not_used():
    """A template promoted out of READ_ONLY has no discovery execution path,
    and the fallback is refused for the same reason."""
    allowlist = CommandAllowlist((
        AllowlistEntry(template="show running-config", cls="CONFIG_HIGH_RISK",
                       purpose="configuration (hash baseline)"),
    ))
    assert config_capture_command(allowlist) is None


# ------------------------------------------------- RouterOS neighbour fix
def test_routeros_neighbour_evidence_is_actually_planned():
    """Regression guard for the silent one-character drop.

    ``/ip neighbor/print`` (spaces) is not in the allowlist;
    ``/ip/neighbor/print`` (path form) is, and is the spelling every other
    RouterOS template in that file uses.
    """
    allowlist = _allowlist("mikrotik/routeros")
    assert allowlist.classify("/ip neighbor/print") is None
    assert allowlist.classify("/ip/neighbor/print") == "READ_ONLY"
    planned = {cmd for cmd, _ in _crawl().plan_for("mikrotik/routeros", allowlist)}
    assert "/ip/neighbor/print" in planned


# ------------------------------------------------------- plan gap visibility
def test_no_family_has_an_unissuable_parser_left():
    """After the RouterOS fix, every catalog parser can be issued somewhere."""
    crawl = _crawl()
    for family in SIX_FAMILIES:
        allowlist = _allowlist(family)
        assert crawl.plan_gaps_for(family, allowlist) == (), \
            f"{family} has parsers the allowlist will not let it issue"


def test_the_gap_detector_reports_a_vocabulary_mismatch():
    """Prove the detector works — the RouterOS bug is reproducible on demand.

    A parser whose ``command_ref`` no template matches is reported as
    ``NOT_ALLOWLISTED``; one that matches a non-READ_ONLY class is reported as
    ``WRONG_CLASS``. Both used to vanish without a trace.
    """
    crawl = _crawl()
    allowlist = CommandAllowlist((
        AllowlistEntry(template="/system/resource/print", cls="READ_ONLY",
                       purpose="identity"),
        # The MNDP command exists, but not as READ_ONLY.
        AllowlistEntry(template="/ip/neighbor/print", cls="CONFIG_HIGH_RISK",
                       purpose="neighbours"),
    ))
    gaps = crawl.plan_gaps_for("mikrotik/routeros", allowlist)
    assert len(gaps) == 1
    gap = gaps[0]
    assert gap.startswith("PARSER_UNISSUABLE:regex/routeros_ip_neighbor_print:")
    assert gap.endswith(":WRONG_CLASS:CONFIG_HIGH_RISK")

    # And the shape that actually shipped: no template at all.
    only_identity = CommandAllowlist((
        AllowlistEntry(template="/system/resource/print", cls="READ_ONLY",
                       purpose="identity"),
    ))
    gaps2 = crawl.plan_gaps_for("mikrotik/routeros", only_identity)
    assert gaps2[0].endswith(":NOT_ALLOWLISTED")


# ------------------------------------------------------ capability semantics
def test_a_verified_renderer_yields_supported_and_an_unverified_one_yields_unknown():
    """``verified`` is the renderer's own lab-verification flag, and it is the
    difference between "we have proven this on hardware" and "we have a model
    nobody has run". Register item OI-0140 says capability answers grow per lab
    evidence only, so an unverified model answers UNKNOWN — which preflight
    maps to PARTIALLY_MODELED — and never SUPPORTED.
    """
    cisco = build_adapter("cisco/ios-xe")
    assert cisco.renderer_verified is True
    assert cisco.capability("CREATE:vlan") is CapabilityState.SUPPORTED

    junos = build_adapter("juniper/junos")
    assert junos.renderer_verified is False
    assert junos.capability("CREATE:vlan") is CapabilityState.UNKNOWN


def test_an_undeclared_feature_is_not_supported_not_a_maybe():
    cisco = build_adapter("cisco/ios-xe")
    assert cisco.capability("CREATE:quantum_uplink") is CapabilityState.NOT_SUPPORTED


def test_unifi_has_no_rendering_model_and_says_so():
    """UniFi ships an allowlist but no renderer file, so it has no config
    features at all — reported, not approximated from another vendor's syntax.
    """
    unifi = build_adapter("ubiquiti/unifi")
    assert unifi.declared_features() == ()
    assert unifi.capability("CREATE:vlan") is CapabilityState.NOT_SUPPORTED


def test_optional_renderer_lines_do_not_count_as_an_execution_model():
    """A line the renderer marks optional is documentation, not a command it
    will emit; a feature made only of those has no model."""
    adapter = DataDrivenCliAdapter(
        vendor_family="test/family",
        allowlist=CommandAllowlist(()),
        renderer={"verified": True, "features": {
            "only_optional": {"commands": ["? maybe this", "? and this"]},
            "real": {"commands": ["? maybe this", "do the thing"]},
            "empty": {"commands": []},
        }})
    assert adapter.declared_features() == ("real",)


def test_operations_this_adapter_does_not_implement_are_not_supported():
    """The interface default is UNKNOWN ("cannot tell"). Here we can tell: the
    adapter has no such method, so it says NOT_SUPPORTED rather than leaving a
    caller to guess."""
    adapter = build_adapter("cisco/ios-xe")
    assert adapter.capability("bind_collectors") is CapabilityState.NOT_SUPPORTED
    assert adapter.capability("open_session:telnet") is CapabilityState.NOT_SUPPORTED
    assert adapter.capability("open_session:serial_console") is CapabilityState.SUPPORTED
    assert adapter.capability("close_session") is CapabilityState.SUPPORTED
