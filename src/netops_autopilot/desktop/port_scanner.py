"""Serial port auto-detection for real hardware connection.

The human workflow is:
1. Plug all network devices together physically
2. Connect ONE device to computer via console cable (USB-to-Serial)
3. Run the program
4. Program auto-detects the connected port

This module provides deterministic port scanning with no hallucinations.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class SerialPortInfo:
    port: str
    description: str
    hwid: str
    is_usb: bool
    likely_console: bool


def list_serial_ports() -> List[SerialPortInfo]:
    """List all available serial ports with metadata.

    Uses pyserial's list_ports if available, otherwise returns empty list
    with a typed reason. Never fabricates ports.
    """
    try:
        from serial.tools import list_ports
    except ImportError:
        return []

    ports: List[SerialPortInfo] = []
    for p in list_ports.comports():
        desc = (p.description or "").strip()
        hwid = (p.hwid or "").strip()
        port_name = p.device

        # Heuristics for console cables: USB-to-Serial adapters
        # are typically CH340, CP210x, FTDI, PL2303
        is_usb = "USB" in hwid.upper() or "USB" in desc.upper()
        likely_console = any(
            chip in desc.upper() or chip in hwid.upper()
            for chip in ("CH340", "CH341", "CP210", "FTDI", "FT232", "PL2303", "USB SERIAL", "USB-SERIAL")
        )

        ports.append(SerialPortInfo(
            port=port_name,
            description=desc or port_name,
            hwid=hwid,
            is_usb=is_usb,
            likely_console=likely_console,
        ))

    # Sort: likely console cables first, then USB, then others
    ports.sort(key=lambda p: (not p.likely_console, not p.is_usb, p.port))
    return ports


def get_recommended_port() -> Optional[SerialPortInfo]:
    """Get the most likely console port, or None if none detected."""
    ports = list_serial_ports()
    if not ports:
        return None
    # Prefer likely console cables
    for p in ports:
        if p.likely_console:
            return p
    # Fall back to any USB serial
    for p in ports:
        if p.is_usb:
            return p
    # Last resort: first available
    return ports[0] if ports else None


def port_to_dict(p: SerialPortInfo) -> dict:
    return {
        "port": p.port,
        "description": p.description,
        "hwid": p.hwid,
        "is_usb": p.is_usb,
        "likely_console": p.likely_console,
    }
