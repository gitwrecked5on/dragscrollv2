# DragScrollV2

Drag-to-scroll for macOS. Hold a key (or click middle mouse) and drag anywhere to scroll — the way every other OS handles it. Basically allow the user to 'pinch' the screen with their cursor, and move it around as needed.

Built as a menu bar wrapper around [emreyolcu/drag-scroll](https://github.com/emreyolcu/drag-scroll).

---

## For Users — Install from DMG

### Step 1: Download
Get `DragScrollV2-v1.0.dmg` from the [Releases page](https://github.com/gitwrecked5on/dragscrollv2/releases).

### Step 2: Install
Open the DMG → drag **DragScrollV2** into **Applications** → eject the DMG.

### Step 3: Launch
Open DragScrollV2 from Applications.

> On first launch, the app automatically installs DragScroll (the scrolling engine) to `/Applications`. This is expected — DragScroll is bundled inside DragScrollV2 and extracted on first run. **You will see two apps in your Applications folder: DragScroll and DragScrollV2. This is normal and cannot be avoided** — DragScrollV2 is the UI wrapper, DragScroll is the engine that does the actual mouse monitoring. macOS requires the engine to be a standalone app to grant it Accessibility permissions correctly.

### Step 4: Grant Permissions
macOS requires Accessibility access for mouse monitoring. When prompted:

1. Go to **System Settings → Privacy & Security → Accessibility**
2. Add **DragScroll.app** and toggle it **ON**

> Only DragScroll needs this permission, not DragScrollV2.

### Step 5: Use It
Click 🖱️🚫 in your menu bar → **Enable DragScroll**

| Mode | How to activate |
|------|----------------|
| Ctrl+Option (default) | Hold Ctrl+Option, click and drag to scroll |
| Middle Mouse | Click middle mouse button to toggle scrolling on/off |
| Shift | Hold Shift and drag to scroll |

### Updating
Download the new DMG → drag to Applications → click **Replace** → relaunch. No uninstall needed. Your settings are preserved.

### Uninstalling
1. Click 🖱️ → **Quit**
2. Delete **DragScrollV2.app** and **DragScroll.app** from `/Applications`
3. Go to **System Settings → Privacy & Security → Accessibility** and remove DragScroll from the list
4. Delete preferences: `rm -f ~/.dragscrollv2_prefs.json` (optional)

---

## For Developers — Build from Source

### Prerequisites
- macOS
- Python 3
- Internet connection (DragScroll binary is downloaded automatically if not present)

### Repo Structure
```
dragscrollv2/
├── src/
│   └── dragscrollv2.py      # App logic — the only file you edit day-to-day
├── dragscrollv2.spec         # PyInstaller config — controls how the app is packaged
├── build_dmg.sh              # Run this to produce the DMG
├── icon.png                  # App icon
├── QUICKSTART.md             # End-user focused quick reference
└── README.md
```

### Build
```bash
git clone https://github.com/gitwrecked5on/dragscrollv2.git
cd dragscrollv2
chmod +x build_dmg.sh
./build_dmg.sh
```

This produces `DragScrollV2-v1.0.dmg`. Follow the user install steps above to test it.

`build/` and `dist/` are created during the build and automatically deleted once the DMG is ready. To keep them for debugging (e.g. inspecting the PyInstaller output), comment out the cleanup lines near the bottom of `build_dmg.sh`.

### Dev Workflow
```
Edit src/dragscrollv2.py
→ ./build_dmg.sh
→ Open DMG → drag to Applications → Replace
→ Quit and relaunch DragScrollV2
→ Test changes
→ git commit && git push
```

### Releasing a New Version
1. Update the version string in `dragscrollv2.py` (`show_about`) and `dragscrollv2.spec`
2. Run `./build_dmg.sh`
3. `git tag v1.x && git push --tags`
4. Create a GitHub Release and attach the DMG

> The DMG is not committed to the repo. It lives on GitHub Releases only.

---

## How It Works

DragScrollV2 is a thin Python menu bar app (using [rumps](https://github.com/jaredks/rumps)) that wraps the DragScroll C binary:

- **DragScrollV2** — the UI. Reads your settings, starts/stops DragScroll, lives in the menu bar.
- **DragScroll** — the engine. Monitors mouse and keyboard events, performs the actual scrolling. Written in C by [emreyolcu](https://github.com/emreyolcu).

Settings are stored in `~/.dragscrollv2_prefs.json` and persist across updates.

---

## Credits

- [DragScroll](https://github.com/emreyolcu/drag-scroll) by Emre Yolcu — the scrolling engine
- [rumps](https://github.com/jaredks/rumps) — macOS menu bar framework
- DragScrollV2 wrapper by [gitwrecked5on](https://github.com/gitwrecked5on/dragscrollv2)

## License

MIT