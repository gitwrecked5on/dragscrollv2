# DragScrollV2

A menu bar app for macOS that provides easy control over drag-scrolling functionality.

Built on top of [emreyolcu/drag-scroll](https://github.com/emreyolcu/drag-scroll) with a user-friendly UI similar to Rectangle.app.

## What This Does

- **Menu bar icon** that shows drag-scroll status
- **Three activation modes:**
  - **Middle Mouse Toggle**: Click middle mouse button to turn scrolling on/off
  - **Ctrl+Option Hold**: Hold Ctrl+Option while dragging to scroll
  - **Shift Hold**: Hold Lshit while dragging to scroll
- **Speed control**: Slow, Normal, Fast presets
- **Settings persist** across restarts

## Requirements

- macOS 10.9 or later (tested on Sequoia 15.3.1)
- Python 3 (tested with Python 3.14)
- A mouse (for middle-click mode)

## Installation

**1. Run the installer:**

```bash
cd /Users/av/Create\ Stuff/dragscrollv2
chmod +x install.sh
./install.sh
```

The installer will:
- Download the DragScroll binary
- Install it to `/Applications/DragScroll.app`
- Install Python dependencies (rumps)
- Fix Python 3.10+ compatibility issues automatically

**2. Grant accessibility permissions:**

The installer will prompt you to open System Settings. You need to:

1. Go to **System Settings** → **Privacy & Security** → **Accessibility**
2. Click the **+** button (you may need to unlock with your password)
3. Navigate to `/Applications` and add **DragScroll.app**
4. Make sure the checkbox next to DragScroll is **enabled**

**Important:** Only DragScroll.app needs permissions, not DragScrollV2.

**3. Launch the app:**

```bash
python3 src/dragscrollv2.py
```

You should see a 🖱️ icon appear in your menu bar.

## Usage

### First Time Setup

1. Click the 🖱️ icon in your menu bar
2. Click **"Enable DragScroll"**
3. The icon will change to show it's active
4. Choose your activation mode:
   - **Middle Mouse (Toggle)** - Click to turn on, move mouse to scroll, click again to turn off
   - **Ctrl+Option (Hold)** - Hold keys + drag to scroll

### Changing Settings

Click the menu bar icon to access:
- **Enable/Disable** - Toggle the app on/off
- **Activation Mode** - Switch between middle mouse and Ctrl+Option
- **Speed** - Adjust scrolling speed (Slow/Normal/Fast)

### Testing It Works

**For Middle Mouse Toggle mode:**
1. Click your middle mouse button (scroll wheel click)
2. Move your mouse (don't hold any buttons)
3. The window under your mouse should scroll
4. Click middle button again to turn off

**For Ctrl+Option Hold mode:**
1. Hold down Ctrl+Option keys
2. Click and drag with your mouse
3. The window should scroll
4. Release the keys to stop

## Troubleshooting

### "Menu bar icon doesn't appear"

Check for errors:
```bash
python3 src/dragscrollv2.py
```

If you see import errors, try reinstalling:
```bash
./install.sh
```

### "Scrolling doesn't work"

1. **Check if DragScroll is running:**
   ```bash
   pgrep -x DragScroll
   ```
   Should return a process ID. If not, DragScroll crashed.

2. **Check accessibility permissions:**
   - System Settings → Privacy & Security → Accessibility
   - Make sure DragScroll.app is in the list and enabled

3. **Try launching DragScroll manually:**
   ```bash
   open -a DragScroll
   ```
   If you get a permission popup, grant it.

### "Middle mouse button doesn't work"

Your mouse might not have a middle button or it might be button 2. Try Ctrl+Option mode instead.

### "DragScroll keeps asking for accessibility permissions"

This happens if macOS doesn't recognize the app. Try:
```bash
cd /Applications
xattr -dr com.apple.quarantine DragScroll.app
```

Then remove and re-add it in System Settings → Accessibility.

## How It Works

This app is just a thin wrapper around the original DragScroll binary:

1. **DragScrollV2** (the menu bar app) starts/stops **DragScroll** (the C binary)
2. DragScroll does the actual mouse/keyboard monitoring and scrolling
3. DragScrollV2 just makes it easier to control

All the heavy lifting is done by the original emreyolcu/drag-scroll project.

## Uninstallation

```bash
# Remove the apps
rm -rf /Applications/DragScroll.app
killall DragScrollV2 2>/dev/null

# Remove preferences
defaults delete com.emreyolcu.DragScroll 2>/dev/null

# Remove from accessibility permissions
# Go to System Settings → Privacy & Security → Accessibility
# Remove DragScroll from the list

# Uninstall Python packages (optional)
pip3 uninstall -y rumps pyobjc-framework-Cocoa
```

## Credits

- Original DragScroll by [emreyolcu](https://github.com/emreyolcu/drag-scroll)
- Menu bar UI built with [rumps](https://github.com/jaredks/rumps)

## License

MIT License - Same as the original DragScroll project
