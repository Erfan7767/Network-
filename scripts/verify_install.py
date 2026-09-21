"""Verify the install is healthy.

Boots the CLI and prints the result of every subcommand. Exits 0 on
success, non-zero on any failure. Designed to be run in CI right after
``pip install -e .`` to catch the "it imports but doesn't actually
work" class of bugs.

Usage:
    python scripts/verify_install.py
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _run(cmd: list[str], *, timeout: int = 60) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, cwd=str(ROOT), capture_output=True, text=True, timeout=timeout,
        env={"PYTHONPATH": "src", **__import__("os").environ},
    )


def main() -> int:
    py = sys.executable

    print("=" * 60)
    print("NetOps Autopilot — install verification")
    print("=" * 60)

    # 1. Top-level --help
    print("\n[1/8] CLI --help")
    r = _run([py, "-m", "netops_autopilot", "--help"])
    if r.returncode != 0:
        print("FAIL:", r.stderr)
        return 1
    print("ok")

    # 2. health subcommand
    print("\n[2/8] health subcommand")
    r = _run([py, "-m", "netops_autopilot", "health"])
    if r.returncode != 0:
        print("FAIL:", r.stderr)
        return 1
    print("ok:", r.stdout.strip()[:120])

    # 3. config subcommand (smoke)
    print("\n[3/8] config subcommand (smoke)")
    r = _run([py, "-m", "netops_autopilot", "config", "--help"])
    if r.returncode != 0:
        print("FAIL:", r.stderr)
        return 1
    print("ok")

    # 4. full test suite smoke
    print("\n[4/8] test suite (smoke: import-only)")
    r = _run([py, "-c", (
        "import sys; sys.path.insert(0, 'src');"
        "from netops_autopilot.autopilot import AutopilotEngine;"
        "from netops_autopilot.ledger.store import LedgerStore;"
        "from netops_autopilot.adapters.cisco_iosxe import CiscoIosXeSerialAdapter;"
        "from netops_autopilot.llm.providers import build_provider;"
        "from netops_autopilot.core.ratelimit import RateLimiter;"
        "from netops_autopilot.core.cache import LRUCache;"
        "print('imports ok')"
    )], timeout=30)
    if r.returncode != 0:
        print("FAIL:", r.stderr)
        return 1
    print(r.stdout.strip())

    # 5. version + key import
    print("\n[5/8] package version")
    r = _run([py, "-c", (
        "import sys; sys.path.insert(0, 'src');"
        "import netops_autopilot;"
        "print(getattr(netops_autopilot, '__version__', 'dev'))"
    )], timeout=10)
    if r.returncode != 0:
        print("FAIL:", r.stderr)
        return 1
    print("version:", r.stdout.strip())

    # 6. HTML report renders a non-empty string
    print("\n[6/8] HTML report renders")
    r = _run([py, "-c", (
        "import sys; sys.path.insert(0, 'src');"
        "from netops_autopilot.reporting.html_report import render_html_report, report_from_autopilot;"
        "data = report_from_autopilot("
        "  report={'final': 'COMPLETE-STAGED', 'phases': []},"
        "  run_id='verify', ledger_event_count=0, chain_ok=True);"
        "html = render_html_report(data);"
        "assert len(html) > 1000, 'html too small';"
        "print('html bytes:', len(html))"
    )], timeout=10)
    if r.returncode != 0:
        print("FAIL:", r.stderr)
        return 1
    print(r.stdout.strip())

    # 7. End-to-end engine run on the simulated fabric
    print("\n[7/8] end-to-end engine run")
    r = _run([py, "-c", (
        "import sys; sys.path.insert(0, 'src'); sys.path.insert(0, '.');\n"
        "from netops_autopilot.autopilot.orchestrator import AutopilotEngine;\n"
        "from netops_autopilot.autopilot.answer_script import answer_script;\n"
        "from netops_autopilot.cli import ScriptedIO;\n"
        "from netops_autopilot.ledger.store import LedgerStore;\n"
        "from netops_autopilot.core.timeauth import TimeAuthority;\n"
        "import datetime;\n"
        "tz = datetime.timezone.utc;\n"
        "ta = TimeAuthority(clock=lambda: datetime.datetime.now(tz));\n"
        "store = LedgerStore(':memory:');\n"
        "kid = store.keys.create_key('verify');\n"
        # The answers come from answer_script(), the single source of truth for
        # the orchestrator's question order. They used to be a hand-written
        # literal list here; when the orchestrator grew the access-retry,
        # DNS and typed-BOND questions the list silently slid one slot out of
        # alignment, 'seed-01' landed on the intent question, and this check
        # failed with final=BLOCKED-BLOCKED while the engine was behaving
        # exactly as designed.
        "answers = answer_script(access_retry='n', intent='2');\n"
        "engine = AutopilotEngine(store=store, key_id=kid, io=ScriptedIO(list(answers)),"
        " time_authority=ta);\n"
        "from tests.support.simfabric import SimFabricFactory;\n"
        "fabric = SimFabricFactory(include_access=True, access_behavior='allow');\n"
        "report = engine.run(\n"
        "  probe_port_session_factory=lambda p: fabric.probe(p),\n"
        "  mgmt_session_factory=fabric.open,\n"
        "  port='SIM0', execute=False);\n"
        "assert report.final == 'COMPLETE-STAGED', f'final={report.final}';\n"
        "assert store.verify_chain().ok, 'ledger chain broken';\n"
        "print('run ok, devices:', report.crawl.totals.get('devices', 0) if report.crawl else 0)\n"
    )], timeout=60)
    if r.returncode != 0:
        print("FAIL:", r.stderr)
        return 1
    print(r.stdout.strip())

    # 8. Every supported vendor family resolves a shipped adapter.
    print("\n[8/8] adapter registry covers every vendor family")
    r = _run([py, "-c", (
        "import sys; sys.path.insert(0, 'src');\n"
        "from netops_autopilot.adapters.bootstrap import default_registry, registered_families;\n"
        "reg = default_registry();\n"
        "fams = registered_families();\n"
        "assert len(fams) == 6, f'expected six vendor families, got {fams}';\n"
        "for vendor, os_name in fams:\n"
        "    a = reg.resolve(vendor=vendor, os=os_name);\n"
        "    assert a is not None, f'no adapter for {vendor}/{os_name}';\n"
        "assert reg.resolve(vendor='nobody', os='never') is None, "
        "'an unknown vendor must resolve to nothing, never to a guess';\n"
        "print('adapters shipped for:', ', '.join(f'{v}/{o}' for v, o in fams))\n"
    )], timeout=30)
    if r.returncode != 0:
        print("FAIL:", r.stderr)
        return 1
    print(r.stdout.strip())

    print("\n" + "=" * 60)
    print("ALL 8 CHECKS PASSED")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
