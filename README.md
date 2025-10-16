# DragScrollV2

**Making Mac mice suck less** - A menu bar wrapper for DragScroll

## The Story (Why This Exists)

If you're a Windows refugee forced to use a Mac, you've probably noticed: **mouse support on macOS is genuinely terrible**.

On Windows, middle-click drag scrolling "just works." You click the middle mouse button, move the mouse, and boom - smooth scrolling in any direction.

On Mac? Nothing. Apple expects you to use their trackpad.

### The Journey

I spent hours trying solutions:
- Hammerspoon (compatibility issues)
- Mac Mouse Fix ($3)
- Smart Scroll ($14)
- Found [DragScroll](https://github.com/emreyolcu/drag-scroll) by Emre Yolcu (great, but command-line only)

**So I built this wrapper.**

## Features

- ✅ Menu bar icon (🖱️🚫 = dormant, 🖱️ = active)
- ✅ Click to toggle on/off
- ✅ Visual notifications
- ✅ Activation methods:
  - **Ctrl + Option** (recommended - preserves middle-click)
  - **Middle Mouse Button**
- ✅ Speed presets (Slow/Normal/Fast)
- ✅ Launch at login
- ✅ **100% FREE**

## Installation

### Quick Start

```bash
cd dragscrollv2
./install.sh
python3 src/dragscroll-menubar.py
```

### Detailed Steps

1. **Run installer**:
   ```bash
   ./install.sh
   ```

2. **Launch menu bar app**:
   ```bash
   python3 src/dragscroll-menubar.py
   ```

3. **Grant Accessibility permissions**:
   - macOS will prompt you
   - Go to System Settings → Privacy & Security → Accessibility
   - Enable DragScroll

4. **Enable and test**:
   - Click 🖱️🚫 in menu bar → "Enable DragScroll"
   - Hold **Ctrl + Option** and move mouse
   - Should scroll!

5. **(Optional) Enable Launch at Login**:
   - Click menu bar icon → "Launch at Login"

## Usage

### Basic

1. Enable: Click 🖱️🚫 → "Enable DragScroll"
2. Activate scrolling: Hold **Ctrl + Option** + move mouse
3. Disable: Click 🖱️ → "Disable DragScroll"

### Tips

- **Use Ctrl + Option** - Keeps middle-click working for opening links
- **Adjust speed** - Try different presets
- **Per-app conflicts** - Disable when needed (some apps conflict)

## Troubleshooting

**App not scrolling?**
- Check Accessibility permissions
- Verify correct keys (Ctrl + Option)
- Try different speeds

**Middle-click not working?**
- Switch to "Ctrl + Option" mode in settings

**App won't start?**
```bash
pip3 install rumps --break-system-packages
```

See TROUBLESHOOTING.md for more help.

## Technical Details

- **Python 3** + **rumps**: Menu bar interface
- **C** (DragScroll): Core engine
- **RAM Usage**: ~20-35 MB (lightweight)

## Credits

- **Original DragScroll**: [Emre Yolcu](https://github.com/emreyolcu/drag-scroll)
- **Wrapper & UI**: [gitwrecked5on](https://github.com/gitwrecked5on)

## License

MIT License - See [LICENSE](LICENSE)

---

**Why doesn't macOS have this built-in?** 🤷‍♂️
