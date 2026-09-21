"""Desktop Application Package — native computer application layer.

This package provides the native desktop integration for NetOps Autopilot,
making it a REAL computer application (تطبيق كمبيوتر) rather than just a web platform.

Components:
- port_scanner: Auto-detect serial/COM ports for real hardware connection
- system_info: System diagnostics and environment info
- native_window: Native window management with pywebview fallback

The desktop app is a first-class citizen: it launches the FastAPI backend
in a background thread, opens a native window (or browser fallback),
and provides hardware-aware features like automatic port detection.
"""

from pathlib import Path

DESKTOP_DIR = Path(__file__).resolve().parent

__all__ = ["DESKTOP_DIR"]
