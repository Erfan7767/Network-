#!/usr/bin/env python3
"""
NetOps Autopilot — REAL Desktop Application Entry Point
تطبيق كمبيوتر حقيقي فعليا — بديل مهندسين الشبكات آلي تلقائي

This is the MAIN entry point for the REAL computer application.
Not a platform, not a web app — a REAL desktop program that happens to
use a webview for its UI, exactly like VS Code, Slack, Discord, etc.

Features:
- Native window with pywebview (or browser fallback)
- Auto-detect serial ports for real hardware
- System tray integration
- Splash screen
- Professional lifecycle management
- Works for small and large networks with microscopic precision
- 40-year expert level quality

Usage:
    python desktop_app.py              # Launch REAL desktop app
    python desktop_app.py --demo       # Launch + auto demo
    python desktop_app.py --port COM3  # Launch with specific port
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Ensure package is importable
_HERE = Path(__file__).resolve().parent
_SRC = _HERE / "src"
if _SRC.is_dir():
    sys.path.insert(0, str(_SRC))
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

# Import the enhanced app launcher
from app import main

if __name__ == "__main__":
    sys.exit(main())
