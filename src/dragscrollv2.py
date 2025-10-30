#!/usr/bin/env python3
"""
DragScrollV2 - Menu Bar Controller for DragScroll
A simple menu bar app that controls the DragScroll binary.

This app does NOT do the actual drag-scrolling. It just starts/stops
the DragScroll binary and configures it via macOS defaults commands.

All the actual mouse/keyboard monitoring and scrolling is handled by
the original DragScroll C binary by emreyolcu.
"""

import rumps
import subprocess
import json
import os
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================

# Where we store user preferences (in their home directory)
PREFS_FILE = Path.home() / ".dragscrollv2_prefs.json"

# Default settings
DEFAULT_PREFS = {
    "enabled": False,           # Is DragScroll currently running?
    "mode": "ctrl_option",      # "ctrl_option" or "middle_mouse"
    "speed": 3                  # Scrolling speed (1=slow, 3=normal, 5=fast)
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def load_preferences():
    """
    Load user preferences from disk.
    If the file doesn't exist, return default preferences.
    """
    if PREFS_FILE.exists():
        try:
            with open(PREFS_FILE, 'r') as f:
                prefs = json.load(f)
                # Merge with defaults in case new settings were added
                return {**DEFAULT_PREFS, **prefs}
        except Exception as e:
            print(f"Error loading preferences: {e}")
            return DEFAULT_PREFS.copy()
    return DEFAULT_PREFS.copy()


def save_preferences(prefs):
    """
    Save user preferences to disk.
    """
    try:
        with open(PREFS_FILE, 'w') as f:
            json.dump(prefs, f, indent=2)
    except Exception as e:
        print(f"Error saving preferences: {e}")


def is_dragscroll_running():
    """
    Check if the DragScroll process is currently running.
    Returns: True if running, False otherwise
    """
    try:
        # Use pgrep to find the DragScroll process
        result = subprocess.run(
            ['pgrep', '-x', 'DragScroll'],
            capture_output=True,
            text=True
        )
        # pgrep returns 0 if found, 1 if not found
        return result.returncode == 0
    except Exception as e:
        print(f"Error checking if DragScroll is running: {e}")
        return False


def start_dragscroll():
    """
    Start the DragScroll binary.
    
    IMPORTANT: We use 'open -a' instead of running the binary directly.
    This is required for macOS to properly recognize the accessibility permissions.
    
    Returns: True if started successfully, False otherwise
    """
    try:
        # Check if it's already running
        if is_dragscroll_running():
            print("DragScroll is already running")
            return True
        
        # Start DragScroll using 'open -a' (macOS application launcher)
        # This ensures macOS recognizes it as the app we granted permissions to
        subprocess.Popen(
            ['open', '-a', 'DragScroll'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # Give it a moment to start
        import time
        time.sleep(0.5)
        
        # Verify it started
        if is_dragscroll_running():
            print("DragScroll started successfully")
            return True
        else:
            print("DragScroll failed to start - check accessibility permissions")
            return False
            
    except Exception as e:
        print(f"Error starting DragScroll: {e}")
        return False


def stop_dragscroll():
    """
    Stop the DragScroll binary.
    """
    try:
        if not is_dragscroll_running():
            print("DragScroll is not running")
            return True
        
        # Kill the DragScroll process
        subprocess.run(['killall', 'DragScroll'], check=False)
        
        print("DragScroll stopped")
        return True
        
    except Exception as e:
        print(f"Error stopping DragScroll: {e}")
        return False


def configure_dragscroll(mode, speed):
    """
    Configure DragScroll via macOS defaults commands.
    
    Mode can be:
    - "ctrl_option": Hold Ctrl+Option keys to activate scrolling
    - "middle_mouse": Click middle mouse button to toggle scrolling on/off
    - "shift": Hold Shift key to activate scrolling
    
    Speed is an integer (1-10, where 3 is normal).
    
    These settings are written to macOS preferences and DragScroll reads them.
    DragScroll must be restarted for changes to take effect.
    """
    try:
        # Configure activation mode
        if mode == "middle_mouse":
            # Button 3 = middle mouse (scroll wheel click)
            # Setting button to non-zero enables button toggle mode
            subprocess.run(
                ['defaults', 'write', 'com.emreyolcu.DragScroll', 'button', '-int', '3'],
                check=True
            )
            # Clear modifier keys (empty array = disabled)
            subprocess.run(
                ['defaults', 'write', 'com.emreyolcu.DragScroll', 'keys', '-array'],
                check=True
            )
            print("Configured for middle mouse button toggle mode")
            
        elif mode == "shift":
            # Setting button to 0 disables button mode
            subprocess.run(
                ['defaults', 'write', 'com.emreyolcu.DragScroll', 'button', '-int', '0'],
                check=True
            )
            # Set modifier key to Shift (this is DragScroll's default)
            subprocess.run(
                ['defaults', 'write', 'com.emreyolcu.DragScroll', 'keys', '-array', 'shift'],
                check=True
            )
            print("Configured for Shift hold mode")
            
        else:  # ctrl_option
            # Setting button to 0 disables button mode
            subprocess.run(
                ['defaults', 'write', 'com.emreyolcu.DragScroll', 'button', '-int', '0'],
                check=True
            )
            # Set modifier keys to Control + Option
            subprocess.run(
                ['defaults', 'write', 'com.emreyolcu.DragScroll', 'keys', '-array', 'control', 'option'],
                check=True
            )
            print("Configured for Ctrl+Option hold mode")
        
        # Configure speed
        subprocess.run(
            ['defaults', 'write', 'com.emreyolcu.DragScroll', 'speed', '-int', str(speed)],
            check=True
        )
        print(f"Configured speed: {speed}")
        
        return True
        
    except Exception as e:
        print(f"Error configuring DragScroll: {e}")
        return False


# =============================================================================
# MENU BAR APP CLASS
# =============================================================================

class DragScrollV2App(rumps.App):
    """
    The main menu bar application.
    
    This creates a menu bar icon and handles user interactions.
    All the actual drag-scrolling is done by the DragScroll binary.
    """
    
    def __init__(self):
        # Initialize the app with a mouse icon
        # The icon will show the current status
        super(DragScrollV2App, self).__init__(
            "DragScrollV2",
            icon=None,  # We'll set this based on status
            quit_button=None  # We'll add our own quit button
        )
        
        # Load user preferences
        self.prefs = load_preferences()
        
        # Sync actual DragScroll state with saved preferences on startup
        # This fixes the "enabled but doesn't work" issue
        actual_running = is_dragscroll_running()
        if self.prefs["enabled"] and not actual_running:
            # Prefs say enabled but it's not running - fix it
            configure_dragscroll(self.prefs["mode"], self.prefs["speed"])
            start_dragscroll()
        elif not self.prefs["enabled"] and actual_running:
            # Prefs say disabled but it's running - stop it
            stop_dragscroll()
        
        # Build the menu
        self.menu = [
            rumps.MenuItem("Enable DragScroll", callback=self.toggle_dragscroll),
            None,  # Separator
        ]
        
        # Create activation mode submenu items
        self.middle_mouse_item = rumps.MenuItem("Middle Mouse (Toggle)", callback=self.set_middle_mouse)
        self.ctrl_option_item = rumps.MenuItem("Ctrl+Option (Hold)", callback=self.set_ctrl_option)
        self.shift_item = rumps.MenuItem("Shift (Hold)", callback=self.set_shift)
        
        # Create speed submenu items
        self.slow_item = rumps.MenuItem("Slow", callback=lambda _: self.set_speed(1))
        self.normal_item = rumps.MenuItem("Normal", callback=lambda _: self.set_speed(3))
        self.fast_item = rumps.MenuItem("Fast", callback=lambda _: self.set_speed(5))
        
        # Add to menu
        self.menu.add(self.middle_mouse_item)
        self.menu.add(self.ctrl_option_item)
        self.menu.add(self.shift_item)
        self.menu.add(None)  # Separator
        self.menu.add(self.slow_item)
        self.menu.add(self.normal_item)
        self.menu.add(self.fast_item)
        self.menu.add(None)  # Separator
        self.menu.add(rumps.MenuItem("About DragScrollV2", callback=self.show_about))
        self.menu.add(rumps.MenuItem("Quit", callback=self.quit_app))
        
        # Update the UI to reflect current state
        self.update_ui()
    
    
    def update_ui(self):
        """
        Update the menu bar icon and menu items to reflect current state.
        """
        # Update the enable/disable menu item
        if self.prefs["enabled"]:
            self.menu["Enable DragScroll"].title = "Disable DragScroll"
            self.title = "🖱️"  # Mouse icon when enabled
        else:
            self.menu["Enable DragScroll"].title = "Enable DragScroll"
            self.title = "🖱️🚫"  # Mouse with slash when disabled
        
        # Update activation mode checkmarks
        self.middle_mouse_item.state = (self.prefs["mode"] == "middle_mouse")
        self.ctrl_option_item.state = (self.prefs["mode"] == "ctrl_option")
        self.shift_item.state = (self.prefs["mode"] == "shift")
        
        # Update speed checkmarks
        speed = self.prefs["speed"]
        self.slow_item.state = (speed == 1)
        self.normal_item.state = (speed == 3)
        self.fast_item.state = (speed == 5)
    
    
    def toggle_dragscroll(self, sender):
        """
        Enable or disable DragScroll.
        """
        if self.prefs["enabled"]:
            # Currently enabled, so disable it
            if stop_dragscroll():
                self.prefs["enabled"] = False
                save_preferences(self.prefs)
                self.update_ui()
                rumps.notification(
                    "DragScrollV2",
                    "Disabled",
                    "Drag scrolling has been disabled"
                )
        else:
            # Currently disabled, so enable it
            # First, configure DragScroll with current settings
            configure_dragscroll(self.prefs["mode"], self.prefs["speed"])
            
            # Then start it
            if start_dragscroll():
                self.prefs["enabled"] = True
                save_preferences(self.prefs)
                self.update_ui()
                
                # Show a helpful notification
                if self.prefs["mode"] == "middle_mouse":
                    message = "Click middle mouse button to toggle scrolling"
                else:
                    message = "Hold Ctrl+Option and drag to scroll"
                
                rumps.notification(
                    "DragScrollV2",
                    "Enabled",
                    message
                )
            else:
                # Failed to start
                rumps.alert(
                    "Failed to start DragScroll",
                    "Make sure you've granted accessibility permissions.\n\n"
                    "Go to System Settings → Privacy & Security → Accessibility\n"
                    "and add /Applications/DragScroll.app"
                )
    
    
    def set_middle_mouse(self, sender):
        """
        Switch to middle mouse button toggle mode.
        """
        if self.prefs["mode"] != "middle_mouse":
            self.prefs["mode"] = "middle_mouse"
            save_preferences(self.prefs)
            
            # If DragScroll is running, restart it with new config
            if self.prefs["enabled"]:
                configure_dragscroll(self.prefs["mode"], self.prefs["speed"])
                stop_dragscroll()
                start_dragscroll()
                
                rumps.notification(
                    "DragScrollV2",
                    "Mode Changed",
                    "Click middle mouse button to toggle scrolling"
                )
            
            self.update_ui()
    
    
    def set_ctrl_option(self, sender):
        """
        Switch to Ctrl+Option hold mode.
        """
        if self.prefs["mode"] != "ctrl_option":
            self.prefs["mode"] = "ctrl_option"
            save_preferences(self.prefs)
            
            # If DragScroll is running, restart it with new config
            if self.prefs["enabled"]:
                configure_dragscroll(self.prefs["mode"], self.prefs["speed"])
                stop_dragscroll()
                start_dragscroll()
                
                rumps.notification(
                    "DragScrollV2",
                    "Mode Changed",
                    "Hold Ctrl+Option and drag to scroll"
                )
            
            self.update_ui()
    
    
    def set_shift(self, sender):
        """
        Switch to Shift hold mode.
        """
        if self.prefs["mode"] != "shift":
            self.prefs["mode"] = "shift"
            save_preferences(self.prefs)
            
            # If DragScroll is running, restart it with new config
            if self.prefs["enabled"]:
                configure_dragscroll(self.prefs["mode"], self.prefs["speed"])
                stop_dragscroll()
                start_dragscroll()
                
                rumps.notification(
                    "DragScrollV2",
                    "Mode Changed",
                    "Hold Shift and drag to scroll"
                )
            
            self.update_ui()
    
    
    def set_speed(self, speed):
        """
        Change the scrolling speed.
        """
        if self.prefs["speed"] != speed:
            self.prefs["speed"] = speed
            save_preferences(self.prefs)
            
            # If DragScroll is running, restart it with new config
            if self.prefs["enabled"]:
                configure_dragscroll(self.prefs["mode"], self.prefs["speed"])
                stop_dragscroll()
                start_dragscroll()
                
                speed_name = {1: "Slow", 3: "Normal", 5: "Fast"}.get(speed, "Custom")
                rumps.notification(
                    "DragScrollV2",
                    "Speed Changed",
                    f"Scrolling speed set to {speed_name}"
                )
            
            self.update_ui()
    
    
    def show_about(self, sender):
        """
        Show the About dialog with credits and version info.
        """
        about_text = (
            "DragScrollV2\n"
            "Version 1.0\n\n"
            "A menu bar wrapper for easy drag-scrolling on macOS.\n\n"
            "Credits:\n"
            "• Original DragScroll by Emre Yolcu\n"
            "  github.com/emreyolcu/drag-scroll\n"
            "• DragScrollV2 wrapper by gitwrecked5on\n"
            "  https://github.com/gitwrecked5on/dragscrollv2\n\n"
            "Built with rumps (Ridiculously Uncomplicated macOS Python Statusbar apps)\n"
            "License: MIT"
        )
        
        rumps.alert(
            title="About DragScrollV2",
            message=about_text,
            ok="OK"
        )
    
    
    def quit_app(self, sender):
        """
        Clean up and quit the app.
        """
        # ALWAYS stop DragScroll when quitting the UI, regardless of enabled state
        # This ensures the UI and the backend stay in sync
        if is_dragscroll_running():
            stop_dragscroll()
            print("Stopped DragScroll on quit")
        
        # Quit
        rumps.quit_application()


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    # Create and run the app
    app = DragScrollV2App()
    app.run()