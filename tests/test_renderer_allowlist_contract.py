"""Every command the renderer produces must pass the allowlist gate.

This is not a style check — it is a contract between the renderer (which
knows what a network change looks like for a vendor) and the allowlist
(which knows what the platform is allowed to send to that vendor's devices).
A command the renderer produces but the allowlist does not recognize would be
rejected by the executor on a real device, and the apply would roll back.
Finding that here, from data alone, means the defect is caught before it
reaches a device — the same role a pre-deployment syntax check plays for a
human engineer.

The test binds every renderer template with realistic values (CIDR addresses,
integer VLAN ids, interface names) so that the allowlist's structural matcher
sees the same token shapes a real device would receive. An earlier version of
this test bound ``{address}`` to a bare ``X`` and falsely reported Junos SVI
and RouterOS SVI as ungated — the allowlist expected ``<ip>/<prefix>`` and
the single-token substitution did not match. CIDR values are the correct
binding because that is what the design engine actually fills.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

import pytest

from netops_autopilot.access.allowlist import CommandAllowlist, CONFIG_CLASSES
from netops_autopilot.specs_data import specs_data_dir

RENDERER_DIR = Path(specs_data_dir("renderers")) if specs_data_dir("renderers") else None
ALLOWLIST_DIR = Path(specs_data_dir("allowlists")) if specs_data_dir("allowlists") else None

# File stems that have both a renderer and an allowlist.
_RENDERER_STEMS = (
    "arubaos",
    "cisco_iosxe",
    "fortios",
    "junos",
    "routeros",
)

# --- realistic bindings ---------------------------------------------------

_INTF = "Gi1/0/1"
_VLAN = "10"
_NAME = "users"
_NET = "10.240.0.0"
_MASK = "255.255.255.192"
_PREFIX = "26"
_GW = "10.240.0.1"
_IP_CIDR = f"{_GW}/{_PREFIX}"
_POOL = "DHCP_POOL"
_DNS = "1.1.1.1 9.9.9.9"

_BINDINGS: dict[str, str] = {
    "vlan_id": _VLAN, "vlan": _VLAN, "id": _VLAN,
    "name": _NAME, "hostname": "edge-sw",
    "intf": _INTF, "interface": _INTF, "port": _INTF,
    "trunk_intf": _INTF, "access_intf": _INTF, "svi_intf": "Vlan10",
    "unit": _VLAN,
    "ip": _GW, "address": _IP_CIDR, "subnet": f"{_NET}/{_PREFIX}",
    "net": _NET, "network": _NET, "mask": _MASK, "prefix": _PREFIX,
    "gateway": _GW, "gw": _GW, "default_gw": _GW,
    "first": _GW, "last": "10.240.0.10",
    "exclude_first": _GW, "exclude_last": "10.240.0.10",
    "pool": _POOL, "dns": _DNS, "servers": _DNS,
    "domain": "example.local",
    "target": "8.8.8.8",
    "args": "10.0.0.0/8",
    "mac": "0011.2233.4455",
    "asn": "65001",
    "remote_as": "65001",
    "tag": "100",
    "site_name": "HQ",
}

_SUBST = re.compile(r"\{([A-Za-z0-9_]+)\}")


def _bind(template: str) -> str:
    """Bind a renderer template with realistic values.

    Every placeholder that looks like an address gets a CIDR value; every
    placeholder that looks like a VLAN id gets an integer; interface names
    get realistic Cisco-style names. The binding is deliberately broad so
    that a ``<ip>/<prefix>`` placeholder in the allowlist sees a literal
    with a slash, not a bare word that would fail the structural match.
    """

    def _rep(m: re.Match) -> str:
        name = m.group(1).lower()
        return _BINDINGS.get(name, "X")

    return _SUBST.sub(_rep, template)


def _family_from_stem(stem: str) -> Optional[str]:
    """The allowlist ``vendor_family`` for a renderer file stem."""
    if not ALLOWLIST_DIR:
        return None
    for path in sorted(ALLOWLIST_DIR.glob("*.json")):
        if path.stem == stem:
            data = json.loads(path.read_text(encoding="utf-8"))
            return data.get("vendor_family")
    return None


@pytest.mark.parametrize("stem", _RENDERER_STEMS)
def test_every_renderer_command_passes_the_allowlist_gate(stem: str):
    """No renderer command is silently ungated.

    This catches two classes of defect:
    1. A renderer template whose placeholder shape disagrees with the
       allowlist template's placeholder shape (the address/subnet case
       that cost Junos and RouterOS their SVI commands).
    2. A renderer feature whose commands were never added to the allowlist
       at all — the command would reach the executor and be rejected,
       causing a rollback on a real device.
    """
    renderer_path = RENDERER_DIR / f"{stem}.json"
    assert renderer_path.exists(), f"renderer not found: {renderer_path}"
    renderer = json.loads(renderer_path.read_text(encoding="utf-8"))

    family = _family_from_stem(stem)
    assert family is not None, f"no allowlist for renderer stem {stem!r}"
    allowlist = CommandAllowlist.load_vendor(str(ALLOWLIST_DIR), family)

    features = renderer.get("features") or {}
    ungated: list[str] = []

    for feat_name, body in sorted(features.items()):
        lines = body.get("commands") or []
        # Skip optional lines (prefixed with ?) — they are documentation,
        # not commands the renderer will emit.
        mandatory = [ln for ln in lines
                     if ln.strip() and not ln.strip().startswith("?")]
        for line in mandatory:
            baked = _bind(line).strip()
            gate = allowlist.gate(baked)
            if gate is None:
                ungated.append(f"{feat_name}: {line!r} → baked={baked!r}")
            elif gate not in CONFIG_CLASSES:
                # A READ_ONLY or FORBIDDEN template matched — the renderer is
                # trying to configure through a command that is not a config
                # class. That is a renderer defect, not a gap to fill.
                ungated.append(
                    f"{feat_name}: {line!r} → baked={baked!r} → class={gate} "
                    f"(not in CONFIG_CLASSES)")

    assert ungated == [], (
        f"renderer '{stem}' has {len(ungated)} command(s) that the "
        f"allowlist will reject on a real device:\n"
        + "\n".join(f"  • {u}" for u in ungated))


def test_all_six_vendor_families_have_an_allowlist():
    """Guard against a renderer being added without its matching allowlist."""
    if not RENDERER_DIR or not ALLOWLIST_DIR:
        pytest.skip("data pack not available")
    renderer_stems = {p.stem for p in RENDERER_DIR.glob("*.json")}
    allowlist_stems = {p.stem for p in ALLOWLIST_DIR.glob("*.json")}
    missing = renderer_stems - allowlist_stems
    assert missing == set(), (
        f"renderer(s) without a matching allowlist: {sorted(missing)}")
