#!/usr/bin/env python3
"""
Build NetOps Autopilot as REAL executable — computer application (تطبيق كمبيوتر)

Creates standalone executables for Windows, macOS, Linux using PyInstaller.
The result is a REAL computer application, not a platform.

Usage:
    python build.py                # Build for current platform
    python build.py --onefile      # Single file executable
    python build.py --windowed     # No console (GUI only)
    python build.py --all          # Build all variants

Requirements:
    pip install pyinstaller pywebview fastapi uvicorn pyserial netmiko paramiko
"""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent


def check_pyinstaller() -> bool:
    try:
        import PyInstaller
        return True
    except ImportError:
        return False


def build_executable(onefile: bool = False, windowed: bool = False, name: str = "NetOpsAutopilot") -> int:
    """Build executable using PyInstaller."""

    if not check_pyinstaller():
        print("PyInstaller not installed")
        print("Install: pip install pyinstaller")
        return 1

    print("=" * 70)
    print(f"  Building {name} — REAL Computer Application")
    print(f"  Platform: {platform.system()} {platform.machine()}")
    print(f"  Mode: {'onefile' if onefile else 'onedir'} {'windowed' if windowed else 'console'}")
    print("=" * 70)
    print()

    # PyInstaller args
    args = [
        sys.executable, "-m", "PyInstaller",
        "--name", name,
        "--distpath", str(_HERE / "dist"),
        "--workpath", str(_HERE / "build"),
        "--specpath", str(_HERE),
        "--clean",
        "--noconfirm",
    ]

    if onefile:
        args.append("--onefile")
    else:
        args.append("--onedir")

    if windowed:
        args.append("--windowed")
    else:
        args.append("--console")

    # Add data files
    # Specs data
    specs_src = _HERE / "specs" / "data"
    if specs_src.exists():
        args.extend(["--add-data", f"{specs_src}{os.pathsep}specs/data"])

    # WebUI static
    webui_src = _HERE / "src" / "netops_autopilot" / "webui" / "static"
    if webui_src.exists():
        args.extend(["--add-data", f"{webui_src}{os.pathsep}netops_autopilot/webui/static"])

    # Simfabric fixtures
    sim_src = _HERE / "src" / "netops_autopilot" / "simfabric" / "fixtures"
    if sim_src.exists():
        args.extend(["--add-data", f"{sim_src}{os.pathsep}netops_autopilot/simfabric/fixtures"])

    # Hidden imports
    hidden = [
        "netops_autopilot",
        "netops_autopilot.web.server",
        "netops_autopilot.webui",
        "netops_autopilot.desktop",
        "netops_autopilot.desktop.port_scanner",
        "netops_autopilot.desktop.system_info",
        "netops_autopilot.desktop.native_window",
        "netops_autopilot.simfabric",
        "netops_autopilot.chat",
        "netops_autopilot.autopilot",
        "netops_autopilot.engines.blueprints",
        "fastapi",
        "uvicorn",
        "uvicorn.logging",
        "uvicorn.loops",
        "uvicorn.loops.auto",
        "uvicorn.protocols",
        "uvicorn.protocols.http",
        "uvicorn.protocols.http.auto",
        "uvicorn.protocols.websockets",
        "uvicorn.protocols.websockets.auto",
        "uvicorn.lifespan",
        "uvicorn.lifespan.on",
        "serial",
        "serial.tools.list_ports",
    ]

    for h in hidden:
        args.extend(["--hidden-import", h])

    # Main script
    args.append(str(_HERE / "desktop_app.py"))

    print(f"Running: {' '.join(args[:10])} ...")
    print()

    try:
        result = subprocess.run(args, cwd=str(_HERE))
        if result.returncode == 0:
            print()
            print("=" * 70)
            print(f"  ✓ Build successful!")
            print(f"  Output: {_HERE / 'dist' / name}")
            if onefile:
                exe = _HERE / "dist" / (f"{name}.exe" if platform.system() == "Windows" else name)
                if exe.exists():
                    size_mb = exe.stat().st_size / (1024*1024)
                    print(f"  Size: {size_mb:.1f} MB")
            print()
            print("  This is a REAL computer application (تطبيق كمبيوتر)")
            print("  Run it, connect hardware, discover, apply — fully automatic!")
            print("=" * 70)
            return 0
        else:
            print(f"Build failed with code {result.returncode}")
            return result.returncode
    except Exception as e:
        print(f"Build error: {e}")
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Build NetOps Autopilot executable")
    parser.add_argument("--onefile", action="store_true", help="Single file executable")
    parser.add_argument("--windowed", action="store_true", help="No console window (GUI only)")
    parser.add_argument("--name", default="NetOpsAutopilot", help="Executable name")
    parser.add_argument("--all", action="store_true", help="Build all variants")
    args = parser.parse_args()

    if args.all:
        # Build both console and windowed, onedir
        print("\n--- Building console version (onedir) ---\n")
        rc1 = build_executable(onefile=False, windowed=False, name=f"{args.name}")
        print("\n--- Building windowed version (onedir) ---\n")
        rc2 = build_executable(onefile=False, windowed=True, name=f"{args.name}-GUI")
        return rc1 or rc2

    return build_executable(onefile=args.onefile, windowed=args.windowed, name=args.name)


if __name__ == "__main__":
    sys.exit(main())
