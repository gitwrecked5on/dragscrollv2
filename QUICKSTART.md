# DragScrollV2 – Quick Start

## For End Users (Installing from DMG)

### Step 1: Download
Download `DragScrollV2-v1.0.dmg` from the [Releases page](https://github.com/gitwrecked5on/dragscrollv2/releases).

### Step 2: Install
1. Double-click the DMG
2. Drag **DragScrollV2** into the **Applications** folder
3. Eject the DMG

### Step 3: Launch
Open DragScrollV2 from your Applications folder.

> On first launch it will automatically install DragScroll (the scrolling engine) to /Applications. This is normal.

### Step 4: Grant Permissions
macOS will prompt you to allow Accessibility access. You **must** do this or scrolling won't work.

1. Click "Open System Settings" when prompted
2. Go to **Privacy & Security → Accessibility**
3. Find **DragScroll** and toggle it **ON**

### Step 5: Use It
Click the 🖱️ icon in your menu bar → **Enable DragScroll**

**Default mode — Ctrl+Option+drag:**
- Hold Ctrl+Option, then click and drag anywhere to scroll
- Release the keys to stop

**To switch to Middle Mouse mode:**
- Click 🖱️ → Activation Mode → Middle Mouse (Toggle)
- Click your middle mouse button to start scrolling, click again to stop

---

## For Developers (Building from Source)

### Prerequisites
- macOS
- Python 3
- Internet connection (DragScroll is downloaded automatically if not present)

### Build

```bash
git clone https://github.com/gitwrecked5on/dragscrollv2.git
cd dragscrollv2
chmod +x build_dmg.sh
./build_dmg.sh
```

This produces `DragScrollV2-v1.0.dmg`. Follow the end user steps above to install it.

---

## Troubleshooting

**Scrolling doesn't work:**
Go to System Settings → Privacy & Security → Accessibility.
Remove DragScroll from the list, re-add it, and make sure it's toggled ON.

**App shows in Dock instead of menu bar only:**
Make sure you're launching DragScrollV2.app, not running dragscrollv2.py directly with Python.

**To fully uninstall:**
```bash
killall DragScroll 2>/dev/null; killall DragScrollV2 2>/dev/null
rm -rf /Applications/DragScroll.app /Applications/DragScrollV2.app
rm -f ~/Library/Preferences/com.emreyolcu.DragScroll.plist
rm -f ~/.dragscrollv2_prefs.json
```