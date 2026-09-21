"""Native window management for the desktop application.

Provides a real computer application window using pywebview when available,
with fallback to browser and tkinter splash screen.

This is what makes it a تطبيق كمبيوتر حقيقي — not just a web platform.
"""

from __future__ import annotations

import os
import sys
import threading
import time
import webbrowser
from pathlib import Path
from typing import Optional, Callable


def has_webview() -> bool:
    try:
        import webview
        return True
    except ImportError:
        return False


def has_tkinter() -> bool:
    try:
        import tkinter
        return True
    except ImportError:
        return False


class DesktopApp:
    """Native desktop application wrapper."""

    def __init__(self, url: str, title: str = "NetOps Autopilot", width: int = 1400, height: int = 900):
        self.url = url
        self.title = title
        self.width = width
        self.height = height
        self._window = None
        self._use_webview = has_webview()

    def run(self, on_startup: Optional[Callable] = None) -> int:
        """Run the desktop application.

        If pywebview is available, opens a native window.
        Otherwise, shows tkinter splash and opens browser.

        Returns exit code.
        """
        if on_startup:
            on_startup()

        if self._use_webview:
            return self._run_webview()
        else:
            return self._run_browser_fallback()

    def _run_webview(self) -> int:
        """Run with pywebview native window."""
        try:
            import webview

            self._window = webview.create_window(
                title=self.title,
                url=self.url,
                width=self.width,
                height=self.height,
                min_size=(1200, 700),
                resizable=True,
                fullscreen=False,
                background_color="#0d1117",
            )

            # Start webview (blocks)
            webview.start(debug=False)
            return 0
        except Exception as e:
            print(f"WebView failed: {e}, falling back to browser")
            return self._run_browser_fallback()

    def _run_browser_fallback(self) -> int:
        """Fallback: tkinter splash + browser."""
        print(f"\n{'='*60}")
        print(f"  {self.title}")
        print(f"  Opening: {self.url}")
        print(f"{'='*60}\n")

        # Try to show tkinter splash if available
        if has_tkinter():
            try:
                self._show_tk_splash()
            except Exception:
                pass

        # Open browser
        try:
            webbrowser.open(self.url)
            print(f"Browser opened: {self.url}")
        except Exception as e:
            print(f"Please open manually: {self.url}")
            print(f"Error: {e}")

        print("\nPress Ctrl+C to stop the server.")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
            return 0

    def _show_tk_splash(self):
        """Show a tkinter splash screen with app info."""
        import tkinter as tk
        from tkinter import ttk

        root = tk.Tk()
        root.title(self.title)
        root.geometry("500x300")
        root.configure(bg="#0d1117")

        # Center window
        root.eval('tk::PlaceWindow . center')

        # Content
        frame = tk.Frame(root, bg="#0d1117")
        frame.pack(fill="both", expand=True, padx=30, pady=30)

        title_label = tk.Label(
            frame,
            text="NetOps Autopilot",
            font=("Segoe UI", 20, "bold"),
            fg="#58a6ff",
            bg="#0d1117"
        )
        title_label.pack(pady=(20, 5))

        subtitle = tk.Label(
            frame,
            text="Autonomous Network Engineer",
            font=("Segoe UI", 11),
            fg="#8b949e",
            bg="#0d1117"
        )
        subtitle.pack(pady=(0, 20))

        url_label = tk.Label(
            frame,
            text=self.url,
            font=("Consolas", 10),
            fg="#e6edf3",
            bg="#161b22",
            padx=10,
            pady=8
        )
        url_label.pack(pady=10, fill="x")

        info = tk.Label(
            frame,
            text="Server running — Browser should open automatically\nClose this window to stop the server",
            font=("Segoe UI", 9),
            fg="#8b949e",
            bg="#0d1117",
            justify="center"
        )
        info.pack(pady=10)

        # Auto-close after 3 seconds and keep running in background
        def close_splash():
            root.destroy()

        root.after(3000, close_splash)
        root.mainloop()


def launch_desktop_app(url: str, title: str = "NetOps Autopilot — Desktop Application") -> int:
    """Convenience launcher."""
    app = DesktopApp(url=url, title=title)
    return app.run()
