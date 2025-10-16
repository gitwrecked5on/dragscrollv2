# Troubleshooting

## Installation Issues

### "command not found: git"
```bash
xcode-select --install
```
Then run `./install.sh` again.

### "pip3: command not found"
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python3
```

### "Permission denied"
```bash
chmod +x install.sh
./install.sh
```

---

## Runtime Issues

### Menu bar icon not appearing
```bash
# Check if running
ps aux | grep dragscroll

# Kill all
killall python3
killall DragScroll

# Install rumps
pip3 install rumps --break-system-packages

# Restart
python3 src/dragscroll-menubar.py
```

### Ctrl+Option doesn't work
**Checklist**:
1. Is app enabled? (Icon = 🖱️ not 🖱️🚫)
2. Holding BOTH Ctrl AND Option?
3. Check Accessibility permissions

**Test binary directly**:
```bash
/Applications/MyDragScroll.app/Contents/MacOS/DragScroll
```

### Middle-click not working
**Expected**: If using "Middle Mouse Button" mode, middle-click toggles DragScroll.

**Fix**: Switch to "Ctrl + Option" mode in menu.

### Scrolling too slow/fast
Try speed presets or:
```bash
defaults write com.emreyolcu.DragScroll speed -int 10
```
(Range: 1-20)

---

## macOS Issues

### "App can't be opened"
```bash
sudo xattr -cr /Applications/MyDragScroll.app
```

### Permissions not sticking
1. System Settings → Privacy & Security → Accessibility
2. Remove DragScroll
3. Close System Settings
4. Launch again
5. Re-grant

---

## Uninstallation

```bash
# Quit
killall python3
killall DragScroll

# Remove launch agent
launchctl unload ~/Library/LaunchAgents/com.dragscrollv2.menubar.plist
rm ~/Library/LaunchAgents/com.dragscrollv2.menubar.plist

# Remove app
sudo rm -rf /Applications/MyDragScroll.app

# Remove prefs
defaults delete com.emreyolcu.DragScroll
```

---

## Known Limitations

**Won't Fix**:
- No momentum scrolling (design limitation)
- No cursor change
- Some app conflicts

**Will Fix** (v1.0):
- Per-app disable list
- Custom modifier keys
- Preferences window

---

## Emergency Reset

```bash
killall python3
killall DragScroll
defaults delete com.emreyolcu.DragScroll
rm -rf /Applications/MyDragScroll.app
rm ~/Library/LaunchAgents/com.dragscrollv2.menubar.plist

# Reinstall
cd "/Users/av/create stuff/dragscrollv2"
./install.sh
python3 src/dragscroll-menubar.py
```
