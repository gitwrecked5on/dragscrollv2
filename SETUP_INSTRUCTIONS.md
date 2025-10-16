# Setup Instructions

## A. Local Setup

### 1. Extract ZIP
Unzip `dragscrollv2.zip` to `/Users/av/create stuff/`

### 2. Navigate
```bash
cd "/Users/av/create stuff/dragscrollv2"
```

### 3. Run Installer
```bash
./install.sh
```

### 4. Launch App
```bash
python3 src/dragscroll-menubar.py
```

### 5. Grant Permissions
- Click menu bar icon → "Enable DragScroll"
- System Settings → Privacy & Security → Accessibility
- Enable DragScroll

### 6. Test
Hold Ctrl+Option and move mouse - should scroll!

---

## B. Publishing to GitHub

### 1. Initialize
```bash
cd "/Users/av/create stuff/dragscrollv2"
git init
git add .
git commit -m "Initial commit - DragScrollV2 v0.1"
```

### 2. Create Repo
- https://github.com/new
- Name: `dragscrollv2`
- Public
- Create

### 3. Push
```bash
git remote add origin https://github.com/gitwrecked5on/dragscrollv2.git
git branch -M main
git push -u origin main
```

### 4. Create Release
- Go to releases
- Tag: `v0.1`
- Title: `v0.1 - Initial Release`
- Publish

---

## C. LinkedIn Post

```
🖱️ Side Project: DragScrollV2

Built a free Mac utility for drag-scrolling (like Windows).

Problem: Mac has no native middle-mouse scrolling
Solution: Menu bar wrapper for DragScroll

Tech: Python, C, macOS APIs

GitHub: github.com/gitwrecked5on/dragscrollv2

Open to feedback!

#ProductManagement #SideProject #OpenSource
```

Post Tuesday/Wednesday morning for best engagement.

---

## D. Troubleshooting

**rumps not installed**:
```bash
pip3 install rumps --break-system-packages
```

**Not scrolling**:
- Check Accessibility permissions
- Verify Ctrl+Option keys
- Try different speeds

**Icon not showing**:
```bash
killall python3
python3 src/dragscroll-menubar.py
```

See TROUBLESHOOTING.md for more.
