"""System information and diagnostics for the desktop app.

Provides real system info with no hallucinations — everything is
derived from actual OS queries.
"""

from __future__ import annotations

import platform
import sys
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class SystemInfo:
    os_name: str
    os_version: str
    architecture: str
    python_version: str
    hostname: str
    app_version: str
    app_dir: str
    has_pyserial: bool
    has_netmiko: bool
    has_paramiko: bool
    has_fastapi: bool
    has_webview: bool


def get_system_info() -> SystemInfo:
    """Collect real system information."""
    has_pyserial = False
    has_netmiko = False
    has_paramiko = False
    has_fastapi = False
    has_webview = False

    try:
        import serial
        has_pyserial = True
    except ImportError:
        pass

    try:
        import netmiko
        has_netmiko = True
    except ImportError:
        pass

    try:
        import paramiko
        has_paramiko = True
    except ImportError:
        pass

    try:
        import fastapi
        has_fastapi = True
    except ImportError:
        pass

    try:
        import webview
        has_webview = True
    except ImportError:
        pass

    # App version
    app_version = "0.1.0"
    try:
        from netops_autopilot import __version__
        app_version = __version__
    except ImportError:
        try:
            import importlib.metadata
            app_version = importlib.metadata.version("netops-autopilot")
        except Exception:
            pass

    return SystemInfo(
        os_name=platform.system(),
        os_version=platform.version(),
        architecture=platform.machine(),
        python_version=platform.python_version(),
        hostname=platform.node(),
        app_version=app_version,
        app_dir=str(Path(__file__).resolve().parent.parent.parent.parent),
        has_pyserial=has_pyserial,
        has_netmiko=has_netmiko,
        has_paramiko=has_paramiko,
        has_fastapi=has_fastapi,
        has_webview=has_webview,
    )


def system_info_to_dict(info: SystemInfo) -> dict:
    return {
        "os_name": info.os_name,
        "os_version": info.os_version,
        "architecture": info.architecture,
        "python_version": info.python_version,
        "hostname": info.hostname,
        "app_version": info.app_version,
        "app_dir": info.app_dir,
        "has_pyserial": info.has_pyserial,
        "has_netmiko": info.has_netmiko,
        "has_paramiko": info.has_paramiko,
        "has_fastapi": info.has_fastapi,
        "has_webview": info.has_webview,
        "ready_for_hardware": info.has_pyserial and info.has_netmiko,
        "ready_for_desktop": info.has_fastapi,
    }
