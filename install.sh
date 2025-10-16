#!/bin/bash
set -e

echo "================================"
echo "  DragScrollV2 Installer"
echo "================================"
echo ""

if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: This script only works on macOS"
    exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "📦 Step 1: Installing dependencies..."

if ! command -v git &> /dev/null; then
    echo "Installing Xcode Command Line Tools..."
    xcode-select --install
    echo "⏳ Please complete the installation dialog, then run this script again."
    exit 0
fi

echo "Installing rumps (Python menu bar library)..."
pip3 install rumps --break-system-packages --quiet || {
    echo "⚠️  Warning: Could not install rumps. Will try again when app starts."
}

echo "✅ Dependencies installed"
echo ""

echo "🔨 Step 2: Compiling DragScroll..."

if [ ! -d "$SCRIPT_DIR/bin/drag-scroll-source" ]; then
    cd "$SCRIPT_DIR/bin"
    git clone https://github.com/emreyolcu/drag-scroll.git drag-scroll-source
    cd drag-scroll-source
else
    echo "Source already present, skipping clone..."
    cd "$SCRIPT_DIR/bin/drag-scroll-source"
fi

echo "Compiling DragScroll binary..."
clang -O2 -Wall -framework ApplicationServices -framework CoreFoundation \
    -o "$SCRIPT_DIR/bin/DragScroll" DragScroll/main.c

echo "✅ DragScroll compiled"
echo ""

echo "📦 Step 3: Creating app bundle..."

mkdir -p "$SCRIPT_DIR/bin/MyDragScroll.app/Contents/MacOS"
mv "$SCRIPT_DIR/bin/DragScroll" "$SCRIPT_DIR/bin/MyDragScroll.app/Contents/MacOS/DragScroll"

cat > "$SCRIPT_DIR/bin/MyDragScroll.app/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>DragScroll</string>
    <key>CFBundleIdentifier</key>
    <string>com.emreyolcu.DragScroll</string>
    <key>LSUIElement</key>
    <true/>
</dict>
</plist>
EOF

sudo cp -r "$SCRIPT_DIR/bin/MyDragScroll.app" /Applications/
sudo xattr -cr /Applications/MyDragScroll.app

echo "✅ App bundle installed to /Applications/"
echo ""

echo "⚙️  Step 4: Configuring defaults..."

defaults write com.emreyolcu.DragScroll button -int 0
defaults write com.emreyolcu.DragScroll keys -array control option
defaults write com.emreyolcu.DragScroll speed -int 5

echo "✅ Defaults configured"
echo ""

echo "🎉 Installation complete!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Next Steps:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Launch the menu bar app:"
echo "   python3 '$SCRIPT_DIR/src/dragscroll-menubar.py'"
echo ""
echo "2. Grant Accessibility permissions when prompted"
echo "   (System Settings → Privacy & Security → Accessibility)"
echo ""
echo "3. Click the 🖱️🚫 icon in your menu bar to enable"
echo ""
echo "4. Hold Ctrl+Option and move your mouse to scroll!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
