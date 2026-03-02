#!/usr/bin/env python3
"""
DragScrollV2 - Menu Bar Controller for DragScroll
A menu bar app that controls the DragScroll binary.

This app does NOT do the actual drag-scrolling. It manages the
DragScroll binary which does all the real work.

The DragScroll binary (by emreyolcu) is bundled inside this app.
On first launch we copy it to /Applications so macOS can find it.
"""

import rumps
import subprocess
import json
import os
import sys
import shutil
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================

PREFS_FILE = Path.home() / ".dragscrollv2_prefs.json"

DEFAULT_PREFS = {
    "enabled": False,
    "mode": "ctrl_option",
    "speed": 3,
    "launch_at_login": False
}

APP_NAME = "DragScrollV2"


# =============================================================================
# BUNDLE DETECTION & DRAGSCROLL SETUP
# =============================================================================

def get_bundle_dir():
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS)
    else:
        return Path(__file__).parent


def ensure_dragscroll_installed():
    dragscroll_dest = Path("/Applications/DragScroll.app")
    if dragscroll_dest.exists():
        return True
    bundle_dir = get_bundle_dir()
    dragscroll_source = bundle_dir / "DragScroll.app"
    if not dragscroll_source.exists():
        print(f"DragScroll.app not found in bundle at: {dragscroll_source}")
        return False
    print("First launch: installing DragScroll.app to /Applications...")
    try:
        shutil.copytree(str(dragscroll_source), str(dragscroll_dest))
        subprocess.run(['xattr', '-dr', 'com.apple.quarantine', str(dragscroll_dest)], capture_output=True)
        print("DragScroll.app installed successfully.")
        return True
    except Exception as e:
        print(f"Failed to install DragScroll.app: {e}")
        return False


# =============================================================================
# LAUNCH AT LOGIN
# =============================================================================

def get_app_path():
    if hasattr(sys, '_MEIPASS'):
        return str(Path(sys.executable).parent.parent.parent)
    return None


def set_launch_at_login(enabled):
    app_path = get_app_path()
    if not app_path:
        print("Launch at login: skipped (not running as bundled app)")
        return
    if enabled:
        script = f'''
        tell application "System Events"
            if not (exists login item "{APP_NAME}") then
                make login item at end with properties {{path:"{app_path}", hidden:false}}
            end if
        end tell
        '''
    else:
        script = f'''
        tell application "System Events"
            if exists login item "{APP_NAME}" then
                delete login item "{APP_NAME}"
            end if
        end tell
        '''
    try:
        subprocess.run(['osascript', '-e', script], capture_output=True)
        print(f"Launch at login: {'enabled' if enabled else 'disabled'}")
    except Exception as e:
        print(f"Error setting launch at login: {e}")


# =============================================================================
# PREFERENCES
# =============================================================================

def load_preferences():
    if PREFS_FILE.exists():
        try:
            with open(PREFS_FILE, 'r') as f:
                prefs = json.load(f)
                return {**DEFAULT_PREFS, **prefs}
        except Exception as e:
            print(f"Error loading preferences: {e}")
    return DEFAULT_PREFS.copy()


def save_preferences(prefs):
    try:
        with open(PREFS_FILE, 'w') as f:
            json.dump(prefs, f, indent=2)
    except Exception as e:
        print(f"Error saving preferences: {e}")


# =============================================================================
# DRAGSCROLL PROCESS MANAGEMENT
# =============================================================================

def is_dragscroll_running():
    try:
        result = subprocess.run(['pgrep', '-x', 'DragScroll'], capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error checking DragScroll status: {e}")
        return False


def start_dragscroll():
    try:
        if is_dragscroll_running():
            return True
        subprocess.Popen(['open', '-a', 'DragScroll'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        import time
        time.sleep(0.5)
        if is_dragscroll_running():
            print("DragScroll started.")
            return True
        else:
            print("DragScroll failed to start - check Accessibility permissions.")
            return False
    except Exception as e:
        print(f"Error starting DragScroll: {e}")
        return False


def stop_dragscroll():
    try:
        if not is_dragscroll_running():
            return True
        subprocess.run(['killall', 'DragScroll'], check=False)
        print("DragScroll stopped.")
        return True
    except Exception as e:
        print(f"Error stopping DragScroll: {e}")
        return False


def configure_dragscroll(mode, speed):
    try:
        if mode == "middle_mouse":
            subprocess.run(['defaults', 'write', 'com.emreyolcu.DragScroll', 'button', '-int', '3'], check=True)
            subprocess.run(['defaults', 'write', 'com.emreyolcu.DragScroll', 'keys', '-array'], check=True)
        elif mode == "shift":
            subprocess.run(['defaults', 'write', 'com.emreyolcu.DragScroll', 'button', '-int', '0'], check=True)
            subprocess.run(['defaults', 'write', 'com.emreyolcu.DragScroll', 'keys', '-array', 'shift'], check=True)
        else:  # ctrl_option
            subprocess.run(['defaults', 'write', 'com.emreyolcu.DragScroll', 'button', '-int', '0'], check=True)
            subprocess.run(['defaults', 'write', 'com.emreyolcu.DragScroll', 'keys', '-array', 'control', 'option'], check=True)
        subprocess.run(['defaults', 'write', 'com.emreyolcu.DragScroll', 'speed', '-int', str(speed)], check=True)
        return True
    except Exception as e:
        print(f"Error configuring DragScroll: {e}")
        return False


# =============================================================================
# MENU BAR APP
# =============================================================================

class DragScrollV2App(rumps.App):

    def __init__(self):
        super(DragScrollV2App, self).__init__("DragScrollV2", icon=None, quit_button=None)

        self.prefs = load_preferences()

        if not ensure_dragscroll_installed():
            rumps.alert("DragScroll Not Found", "DragScroll.app could not be installed.\nPlease reinstall DragScrollV2 from the DMG.")

        if is_dragscroll_running():
            stop_dragscroll()
        self.prefs["enabled"] = False
        save_preferences(self.prefs)

        # ── FLAT MENU - no submenus ────────────────────────────────────
        self.menu.add(rumps.MenuItem("Enable DragScroll", callback=self.toggle_dragscroll))
        self.menu.add(None)

        self.menu.add(rumps.MenuItem("── Activation Mode ──"))
        self.middle_mouse_item = rumps.MenuItem("  Middle Mouse (Toggle)", callback=self.set_middle_mouse)
        self.ctrl_option_item  = rumps.MenuItem("  Ctrl+Option (Hold)",    callback=self.set_ctrl_option)
        self.shift_item        = rumps.MenuItem("  Shift (Hold)",           callback=self.set_shift)
        self.menu.add(self.middle_mouse_item)
        self.menu.add(self.ctrl_option_item)
        self.menu.add(self.shift_item)
        self.menu.add(None)

        self.menu.add(rumps.MenuItem("── Scroll Speed ──"))
        self.slow_item      = rumps.MenuItem("  Slow",      callback=lambda _: self.set_speed(1))
        self.normal_item    = rumps.MenuItem("  Normal",    callback=lambda _: self.set_speed(3))
        self.fast_item      = rumps.MenuItem("  Fast",      callback=lambda _: self.set_speed(5))
        self.very_fast_item = rumps.MenuItem("  Very Fast", callback=lambda _: self.set_speed(7))
        self.menu.add(self.slow_item)
        self.menu.add(self.normal_item)
        self.menu.add(self.fast_item)
        self.menu.add(self.very_fast_item)
        self.menu.add(None)

        self.login_item = rumps.MenuItem("Launch at Login", callback=self.toggle_login)
        self.menu.add(self.login_item)
        self.menu.add(None)

        self.menu.add(rumps.MenuItem("About DragScrollV2", callback=self.show_about))
        self.menu.add(rumps.MenuItem("Quit", callback=self.quit_app))

        self.update_ui()


    def update_ui(self):
        if self.prefs["enabled"]:
            self.menu["Enable DragScroll"].title = "Disable DragScroll"
            self.title = "🖱️"
        else:
            self.menu["Enable DragScroll"].title = "Enable DragScroll"
            self.title = "🖱️🚫"

        self.middle_mouse_item.state = (self.prefs["mode"] == "middle_mouse")
        self.ctrl_option_item.state  = (self.prefs["mode"] == "ctrl_option")
        self.shift_item.state        = (self.prefs["mode"] == "shift")

        speed = self.prefs["speed"]
        self.slow_item.state      = (speed == 1)
        self.normal_item.state    = (speed == 3)
        self.fast_item.state      = (speed == 5)
        self.very_fast_item.state = (speed == 7)
        self.login_item.state     = self.prefs.get("launch_at_login", False)


    def toggle_dragscroll(self, sender):
        if self.prefs["enabled"]:
            if stop_dragscroll():
                self.prefs["enabled"] = False
                save_preferences(self.prefs)
                self.update_ui()
                rumps.notification("DragScrollV2", "Disabled", "Drag scrolling is off.")
        else:
            configure_dragscroll(self.prefs["mode"], self.prefs["speed"])
            if start_dragscroll():
                self.prefs["enabled"] = True
                save_preferences(self.prefs)
                self.update_ui()
                msg = ("Click middle mouse button to toggle scrolling"
                       if self.prefs["mode"] == "middle_mouse"
                       else "Hold Ctrl+Option and drag to scroll")
                rumps.notification("DragScrollV2", "Enabled", msg)
            else:
                rumps.alert("Failed to Start DragScroll",
                    "Grant Accessibility permissions to DragScroll:\n\n"
                    "System Settings → Privacy & Security → Accessibility\n"
                    "Add DragScroll.app and toggle it ON.")


    def set_middle_mouse(self, sender):
        self._set_mode("middle_mouse", "Click middle mouse button to toggle scrolling")

    def set_ctrl_option(self, sender):
        self._set_mode("ctrl_option", "Hold Ctrl+Option and drag to scroll")

    def set_shift(self, sender):
        self._set_mode("shift", "Hold Shift and drag to scroll")

    def _set_mode(self, mode, notification_msg):
        if self.prefs["mode"] != mode:
            self.prefs["mode"] = mode
            save_preferences(self.prefs)
            if self.prefs["enabled"]:
                configure_dragscroll(mode, self.prefs["speed"])
                stop_dragscroll()
                start_dragscroll()
                rumps.notification("DragScrollV2", "Mode Changed", notification_msg)
            self.update_ui()


    def set_speed(self, speed):
        if self.prefs["speed"] != speed:
            self.prefs["speed"] = speed
            save_preferences(self.prefs)
            if self.prefs["enabled"]:
                configure_dragscroll(self.prefs["mode"], speed)
                stop_dragscroll()
                start_dragscroll()
                name = {1: "Slow", 3: "Normal", 5: "Fast", 7: "Very Fast"}.get(speed, str(speed))
                rumps.notification("DragScrollV2", "Speed Changed", f"Scroll speed: {name}")
            self.update_ui()


    def toggle_login(self, sender):
        new_state = not self.prefs.get("launch_at_login", False)
        self.prefs["launch_at_login"] = new_state
        save_preferences(self.prefs)
        set_launch_at_login(new_state)
        self.update_ui()


    def show_about(self, sender):
        # ── Edit the message below to customise the About screen ──
        # \n = new line   • = bullet   ━ = divider line
        rumps.alert(
            title="DragScrollV2  •  v1.0",
            message=(
                "Drag-to-scroll for macOS.\n"
                "\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "\n"
                "  How to use:\n"
                "  • Enable via the menu bar icon\n"
                "  • Hold Ctrl+Option and drag to scroll\n"
                "  • Or switch to Middle Mouse mode\n"
                "\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "\n"
                "  Built on DragScroll by Emre Yolcu\n"
                "  github.com/emreyolcu/drag-scroll\n"
                "\n"
                "  Wrapped by gitwrecked5on\n"
                "  github.com/gitwrecked5on/dragscrollv2\n"
                "\n"
                "  License: MIT\n"
            ),
            ok="Close"
        )


    def quit_app(self, sender):
        if is_dragscroll_running():
            stop_dragscroll()
        rumps.quit_application()


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    app = DragScrollV2App()
    app.run()