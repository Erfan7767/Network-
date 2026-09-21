"""Production adapter registry — the binding ADR-0001 specified and nothing shipped.

Why this module exists
----------------------
ADR-0001 says engines reach hardware *only* through the AdapterRegistry, keyed
by the identified ``(vendor, os, model)`` tuple — never through vendor-name
conditionals. The registry, the nine capability-bound interfaces and the
Preflight Engine (E11) all shipped, and all of them were tested. But no module
in the program ever constructed a registry: ``AdapterRegistry`` appeared in
``src/`` exactly twice, both of them in this adapter package's own text, and in
``tests/`` three times. So in the installed product
``AdapterRegistry.resolve()`` could only ever return ``None``, and preflight —
had anything wired it — could only ever answer ``NO_ADAPTER ⇒ NOT_MODELED``
for every node of every vendor, including Cisco.

This module is the missing binding: one registry, populated for every vendor
family the platform ships an allowlist for.

No vendor knowledge is written here
-----------------------------------
Everything an adapter answers with is derived from data that already has an
owner, so this module cannot drift into a second, unofficial source of vendor
facts:

* **which families exist** — the ``vendor_family`` string inside
  ``specs/data/allowlists/<family>.json``. A family with no allowlist has no
  execution path at all (L10/T3), so it is not registered and resolves to
  nothing;
* **the registration key** — that same string split on ``/``: ``juniper/junos``
  registers as ``vendor="juniper", os="junos"``. Pure string surgery on data,
  not a hand-written table;
* **the discovery commands** — the parser catalog ∩ the family's READ_ONLY
  allowlist, i.e. exactly what :meth:`DiscoveryCrawl.plan_for` will issue. An
  adapter therefore can never advertise a command the crawl would not send;
* **the configuration-dump command** — the READ_ONLY entry whose declared
  purpose is ``configuration (hash baseline)`` (shared with the executor, so
  the two cannot disagree);
* **configuration capability per feature** — whether the family's renderer
  declares that feature with at least one non-optional line, combined with the
  renderer's own ``verified`` flag.

The last point is where honesty does the work. A renderer that declares a
feature but carries ``verified: false`` — five of the six do, and their own
notes say the templates have never been run against a device — yields
``CapabilityState.UNKNOWN``, not ``SUPPORTED``: the model exists and has not
been proven. That maps onto preflight's existing algebra (``UNKNOWN ⇒
PARTIALLY_MODELED``) and onto register item OI-0140, which states that
capability answers grow per lab evidence only. Claiming ``SUPPORTED`` off an
unverified renderer would be exactly the kind of quiet overstatement the
constitution exists to forbid.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from ..access.allowlist import CommandAllowlist
from ..access.executor import CONFIG_CAPTURE_PURPOSE, config_capture_command
from ..access.serial_transport import SerialConsoleTransport, SerialProfile
from ..core.failures import Failure, FailureClass
from ..parsers.catalog import CATALOG_BUILDERS, canonical_families
from ..parsers.registry import Parser
from ..specs_data import specs_data_dir
from .interfaces import (
    AccessAdapter,
    CapabilityState,
    ConfigAdapter,
    DiscoveryAdapter,
    ExecSession,
)
from .registry import AdapterMatch, AdapterRegistry

#: A renderer line starting with this marker is optional — it is documentation
#: of what an operator may add, not a line the renderer will always emit. Only
#: mandatory lines count toward "this feature has an execution model".
OPTIONAL_LINE_MARKER = "?"


def _load_json(directory: str) -> dict[str, dict]:
    """``{file stem: parsed json}`` for every ``*.json`` in ``directory``.

    Returns an empty mapping when the data pack is absent, which is the typed
    "not configured" condition every caller already handles — never a guess.
    """
    out: dict[str, dict] = {}
    if not directory:
        return out
    for path in sorted(Path(directory).glob("*.json")):
        try:
            out[path.stem] = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            # A file we cannot read is not a family we silently invent.
            continue
    return out


def split_family(vendor_family: str) -> tuple[str, str]:
    """``"juniper/junos"`` → ``("juniper", "junos")``.

    The canonical family string is ``<vendor>/<os>`` in every allowlist file,
    so the registration key is a split, not a lookup table. A family string
    without a ``/`` has no separable os and therefore cannot be registered —
    announced, never defaulted.
    """
    if "/" not in vendor_family:
        raise ValueError(
            f"vendor_family={vendor_family!r} is not in <vendor>/<os> form; "
            f"it cannot yield a registration key")
    vendor, os_name = vendor_family.split("/", 1)
    if not vendor or not os_name:
        raise ValueError(f"vendor_family={vendor_family!r} has an empty vendor or os")
    return vendor, os_name


class DataDrivenCliAdapter(AccessAdapter, DiscoveryAdapter, ConfigAdapter):
    """One adapter per vendor family, built entirely from shipped data.

    Implements the three interfaces the v1 product actually exercises:
    session lifecycle over the (family-agnostic) serial console transport,
    layered discovery reads, and running-config capture. Everything else
    inherits the interfaces' typed ``NOT_SUPPORTED`` defaults — no method here
    pretends to work.
    """

    def __init__(
        self,
        *,
        vendor_family: str,
        allowlist: CommandAllowlist,
        parsers: tuple[Parser, ...] = (),
        renderer: Optional[dict] = None,
        port_factory=None,
        clock=None,
        sleep=None,
    ) -> None:
        self.vendor_family = vendor_family
        self._allowlist = allowlist
        self._renderer = renderer or {}
        self._port_factory = port_factory
        self._clock = clock
        self._sleep = sleep
        self._sessions: dict[str, SerialConsoleTransport] = {}
        #: layer name (the command itself) → parser, for exactly the commands
        #: the crawl would plan for this family.
        self._layer_commands: dict[str, Parser] = {}
        for parser in parsers:
            command = parser.info.command_ref
            if allowlist.is_readable(command):
                self._layer_commands[command] = parser
        self._config_command = config_capture_command(allowlist)

    # ------------------------------------------------------- introspection
    @property
    def discovery_layers(self) -> tuple[str, ...]:
        """The commands this adapter can read, in deterministic order."""
        return tuple(sorted(self._layer_commands))

    @property
    def config_capture_command_name(self) -> Optional[str]:
        return self._config_command

    @property
    def renderer_verified(self) -> bool:
        """The renderer's own lab-verification flag (``false`` when absent)."""
        return bool(self._renderer.get("verified", False))

    def declared_features(self) -> tuple[str, ...]:
        """Renderer features with at least one mandatory command line."""
        features = self._renderer.get("features") or {}
        out = []
        for name, body in sorted(features.items()):
            lines = [ln for ln in (body or {}).get("commands") or []
                     if ln.strip() and not ln.strip().startswith(OPTIONAL_LINE_MARKER)]
            if lines:
                out.append(name)
        return tuple(out)

    # ------------------------------------------------------------ capability
    def capability(self, operation: str) -> CapabilityState:
        """Answer from data. Never a hopeful ``UNKNOWN`` for something this
        adapter demonstrably does not do, and never ``SUPPORTED`` for a model
        nobody has verified on hardware."""
        if operation == "open_session:serial_console":
            return CapabilityState.SUPPORTED
        if operation.startswith("open_session:"):
            return CapabilityState.NOT_SUPPORTED
        if operation == "close_session":
            return CapabilityState.SUPPORTED
        if operation.startswith("discovery_layer:"):
            layer = operation.split(":", 1)[1]
            return (CapabilityState.SUPPORTED if layer in self._layer_commands
                    else CapabilityState.NOT_SUPPORTED)
        if operation == "capture_running_config":
            return (CapabilityState.SUPPORTED if self._config_command is not None
                    else CapabilityState.NOT_SUPPORTED)
        # Configuration operations arrive as ``<OPERATION>:<feature>``
        # (preflight builds them from IRNode.operation and IRNode.feature).
        if ":" in operation:
            feature = operation.split(":", 1)[1]
            if feature not in self.declared_features():
                return CapabilityState.NOT_SUPPORTED
            return (CapabilityState.SUPPORTED if self.renderer_verified
                    else CapabilityState.UNKNOWN)
        return CapabilityState.NOT_SUPPORTED

    # ------------------------------------------------------- access adapter
    def open_session(self, device_ref: str, method: str) -> ExecSession:
        if method != "serial_console":
            raise Failure(cls=FailureClass.BLOCKED, causes=(
                f"NOT_SUPPORTED: open_session:{method} — this adapter implements "
                f"serial_console only (T2)",))
        profile = SerialProfile(port=device_ref)
        transport = SerialConsoleTransport(
            profile, port_factory=self._port_factory,
            clock=self._clock if self._clock else __import__("time").monotonic,
            sleep=self._sleep if self._sleep else __import__("time").sleep)
        transport.open()
        self._sessions[device_ref] = transport
        return transport

    def close_session(self, device_ref: str) -> None:
        transport = self._sessions.pop(device_ref, None)
        if transport is not None:
            transport.close()

    def acquire_lock(self, device_ref: str) -> bool:
        """Console attachment is exclusive by construction: we hold the open
        port handle, so no other process on this host can hold it too."""
        return device_ref in self._sessions

    def release_lock(self, device_ref: str) -> None:
        return None

    def human_session_active(self, device_ref: str) -> bool:
        return device_ref not in self._sessions

    # --------------------------------------------------- discovery adapter
    def run_layer(self, device_ref: str, layer: str) -> bytes:
        if layer not in self._layer_commands:
            raise Failure(cls=FailureClass.BLOCKED, causes=(
                f"NOT_MODELED: discovery layer {layer!r} is not an allowlisted, "
                f"parseable command for {self.vendor_family!r} (T2)",))
        session = self._sessions.get(device_ref)
        if session is None:
            raise Failure(cls=FailureClass.BLOCKED, causes=(
                "SESSION_NOT_OPEN: run_layer requires open_session first",))
        return session.execute(layer, timeout_s=30.0)

    # ------------------------------------------------------ config adapter
    def capture_running_config(self, device_ref: str) -> bytes:
        if self._config_command is None:
            raise Failure(cls=FailureClass.BLOCKED, causes=(
                f"NOT_MODELED: {self.vendor_family!r} declares no READ_ONLY command "
                f"with purpose {CONFIG_CAPTURE_PURPOSE!r} — the configuration of this "
                f"device cannot be read, and that is a data gap, not a transport "
                f"failure (T2)",))
        session = self._sessions.get(device_ref)
        if session is None:
            raise Failure(cls=FailureClass.BLOCKED, causes=(
                "SESSION_NOT_OPEN: capture_running_config requires open_session first",))
        return session.execute(self._config_command, timeout_s=60.0)


# --------------------------------------------------------------------- loading
def families_from_data() -> tuple[str, ...]:
    """Every vendor family with a shipped allowlist, sorted.

    The allowlist is the authority on which families exist: without one there
    is nothing the executor may send, so registering an adapter would advertise
    an execution path that cannot exist.
    """
    directory = specs_data_dir("allowlists")
    if not directory:
        return ()
    out: list[str] = []
    for path in sorted(Path(directory).glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        family = data.get("vendor_family")
        if family:
            out.append(family)
    return tuple(sorted(out))


def registered_families() -> tuple[tuple[str, str], ...]:
    """``(vendor, os)`` registration keys for every supported family, sorted."""
    return tuple(sorted(split_family(f) for f in families_from_data()))


def _parsers_for(family: str) -> tuple[Parser, ...]:
    """The catalog parsers whose declared family is this one (alias-aware)."""
    wanted = set(canonical_families(family))
    return tuple(p for p in (b() for b in CATALOG_BUILDERS)
                 if p.info.vendor_family in wanted)


def _renderer_for(os_name: str) -> Optional[dict]:
    """The renderer declaring this os, or ``None`` when the family has none.

    Joined on the renderer's own ``vendor_os`` field — the same string the
    allowlist's family suffix carries — so no filename convention is assumed
    and a family with no renderer (UniFi today) simply has no rendering model.
    """
    for data in _load_json(specs_data_dir("renderers")).values():
        if str(data.get("vendor_os", "")) == os_name:
            return data
    return None


def build_adapter(vendor_family: str, *, port_factory=None, clock=None,
                  sleep=None) -> DataDrivenCliAdapter:
    """One adapter for one family, from data. Raises if the family is unknown."""
    directory = specs_data_dir("allowlists")
    if not directory:
        raise Failure(cls=FailureClass.BLOCKED, causes=(
            "NOT_CONFIGURED: the specs data pack is unavailable, so no allowlist "
            "and therefore no adapter can be built (T2)",))
    allowlist = CommandAllowlist.load_vendor(directory, vendor_family)
    _vendor, os_name = split_family(vendor_family)
    return DataDrivenCliAdapter(
        vendor_family=vendor_family,
        allowlist=allowlist,
        parsers=_parsers_for(vendor_family),
        renderer=_renderer_for(os_name),
        port_factory=port_factory, clock=clock, sleep=sleep)


def default_registry(*, port_factory=None, clock=None, sleep=None) -> AdapterRegistry:
    """The registry the program ships: every supported family bound.

    Deterministic — families are registered in sorted order, so specificity
    tie-breaks in :meth:`AdapterRegistry.resolve` cannot depend on filesystem
    enumeration. An unregistered vendor resolves to ``None``, which preflight
    reports as ``NO_ADAPTER ⇒ NOT_MODELED``: the honest answer for a platform
    this build has no execution model for.
    """
    registry = AdapterRegistry()
    for family in families_from_data():
        vendor, os_name = split_family(family)
        registry.register(
            AdapterMatch(vendor=vendor, os=os_name),
            lambda family=family: build_adapter(
                family, port_factory=port_factory, clock=clock, sleep=sleep))
    return registry
