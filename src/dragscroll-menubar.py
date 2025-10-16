#!/usr/bin/env python3
"""
DragScrollV2 - Menu Bar App
Makes Mac mice suck less by wrapping DragScroll with a proper UI.

Author: gitwrecked5on
Credits: Original DragScroll by Emre Yolcu (https://github.com/emreyolcu/drag-scroll)
License: MIT
"""

import rumps
import subprocess
import os
import time

class DragScrollApp(rumps.App):
    """Main menu bar application for controlling DragScroll"""
    
    def __init__(self):
        super(DragScrollApp, self).__init__("🖱️🚫", quit_button=None)
        self.dragscroll_running = False
        self.current_activation = "ctrl_option"
        
        self.menu = [
            rumps.MenuItem("Enable DragScroll", callback=self.toggle_app),
            rumps.separator,
            "Activation Method",
            rumps.MenuItem("  • Ctrl + Option (recommended)", callback=lambda _: self.set_activation("ctrl_option")),
            rumps.MenuItem("    Middle Mouse Button", callback=lambda _: self.set_activation("middle_mouse")),
            rumps.separator,
            rumps.MenuItem("Speed: Slow (3)", callback=lambda _: self.set_speed(3)),
            rumps.MenuItem("Speed: Normal (5)", callback=lambda _: self.set_speed(5)),
            rumps.MenuItem("Speed: Fast (8)", callback=lambda _: self.set_speed(8)),
            rumps.separator,
            rumps.MenuItem("Launch at Login", callback=self.toggle_launch_at_login),
            rumps.separator,
            rumps.MenuItem("About DragScrollV2", callback=self.show_about),
            "Quit"
        ]
        self.update_login_item_status()
        
    def toggle_app(self, sender):
        if self.dragscroll_running:
            subprocess.run(["killall", "DragScroll"], capture_output=True)
            self.dragscroll_running = False
            sender.title = "Enable DragScroll"
            self.title = "🖱️🚫"
            rumps.notification("DragScrollV2", "Disabled", "Drag scrolling is now OFF")
        else:
            self.start_dragscroll()
            self.dragscroll_running = True
            sender.title = "Disable DragScroll"
            self.title = "🖱️"
            
            if self.current_activation == "ctrl_option":
                message = "Drag scrolling enabled! Use Ctrl+Option + mouse movement"
            else:
                message = "Drag scrolling enabled! Click middle mouse button to activate"
            
            rumps.notification("DragScrollV2", "Enabled", message)
    
    def start_dragscroll(self):
        if self.current_activation == "ctrl_option":
            subprocess.run(["defaults", "write", "com.emreyolcu.DragScroll", "button", "-int", "0"])
            subprocess.run(["defaults", "write", "com.emreyolcu.DragScroll", "keys", "-array", "control", "option"])
        elif self.current_activation == "middle_mouse":
            subprocess.run(["defaults", "write", "com.emreyolcu.DragScroll", "button", "-int", "3"])
            subprocess.run(["defaults", "write", "com.emreyolcu.DragScroll", "keys", "-array"])
        
        subprocess.Popen(["/Applications/MyDragScroll.app/Contents/MacOS/DragScroll"])
    
    def set_activation(self, method):
        self.current_activation = method
        
        if method == "ctrl_option":
            self.menu["Activation Method"]["  • Ctrl + Option (recommended)"].title = "  • Ctrl + Option (recommended) ✓"
            self.menu["Activation Method"]["    Middle Mouse Button"].title = "    Middle Mouse Button"
        else:
            self.menu["Activation Method"]["  • Ctrl + Option (recommended)"].title = "  • Ctrl + Option (recommended)"
            self.menu["Activation Method"]["    Middle Mouse Button"].title = "    Middle Mouse Button ✓"
        
        if self.dragscroll_running:
            subprocess.run(["killall", "DragScroll"], capture_output=True)
            time.sleep(0.2)
            self.start_dragscroll()
            rumps.notification("DragScrollV2", "Activation Method Changed", 
                             f"Now using: {'Ctrl+Option' if method == 'ctrl_option' else 'Middle Mouse Button'}")
    
    def set_speed(self, speed):
        subprocess.run(["defaults", "write", "com.emreyolcu.DragScroll", "speed", "-int", str(speed)])
        if self.dragscroll_running:
            subprocess.run(["killall", "DragScroll"], capture_output=True)
            time.sleep(0.2)
            self.start_dragscroll()
        rumps.notification("DragScrollV2", "Speed Changed", f"Scroll speed set to {speed}")
    
    def toggle_launch_at_login(self, sender):
        plist_path = os.path.expanduser("~/Library/LaunchAgents/com.dragscrollv2.menubar.plist")
        
        if os.path.exists(plist_path):
            subprocess.run(["launchctl", "unload", plist_path], capture_output=True)
            os.remove(plist_path)
            sender.state = False
            rumps.notification("DragScrollV2", "Launch at Login", "Disabled")
        else:
            self.create_launch_agent()
            sender.state = True
            rumps.notification("DragScrollV2", "Launch at Login", "Enabled")
    
    def create_launch_agent(self):
        python_path = subprocess.run(["which", "python3"], capture_output=True, text=True).stdout.strip()
        script_path = os.path.abspath(__file__)
        
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.dragscrollv2.menubar</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python_path}</string>
        <string>{script_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>"""
        
        plist_path = os.path.expanduser("~/Library/LaunchAgents/com.dragscrollv2.menubar.plist")
        os.makedirs(os.path.dirname(plist_path), exist_ok=True)
        
        with open(plist_path, 'w') as f:
            f.write(plist_content)
        
        subprocess.run(["launchctl", "load", plist_path])
    
    def update_login_item_status(self):
        plist_path = os.path.expanduser("~/Library/LaunchAgents/com.dragscrollv2.menubar.plist")
        if os.path.exists(plist_path):
            self.menu["Launch at Login"].state = True
    
    def show_about(self, _):
        rumps.alert(
            title="About DragScrollV2",
            message="A menu bar wrapper for DragScroll\n\n"
                    "Making Mac mice suck less, one scroll at a time.\n\n"
                    "Created by: gitwrecked5on\n"
                    "Original DragScroll: Emre Yolcu\n\n"
                    "GitHub: github.com/gitwrecked5on/dragscrollv2",
            ok="Close"
        )

if __name__ == "__main__":
    try:
        import rumps
    except ImportError:
        print("Installing rumps...")
        subprocess.run(["pip3", "install", "rumps", "--break-system-packages"])
        import rumps
    
    DragScrollApp().run()
