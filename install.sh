#!/bin/bash

# DragScrollV2 Installer
# Sets up Python dependencies - you need to install DragScroll manually first

set -e  # Exit on error

echo "==> DragScrollV2 Installer"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check for Python 3
echo "==> Checking for Python 3..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    echo "Install from: https://www.python.org/downloads/"
    exit 1
fi

echo -e "${GREEN}✓ Found: $(python3 --version)${NC}"
echo ""

# Check if DragScroll is already installed
echo "==> Checking for DragScroll..."
if [ -d "/Applications/DragScroll.app" ]; then
    echo -e "${GREEN}✓ DragScroll.app found${NC}"
else
    echo -e "${YELLOW}⚠ DragScroll.app not found in /Applications${NC}"
    echo ""
    echo "You need to install DragScroll first. Here's how:"
    echo ""
    echo "METHOD 1 (Easiest - if you have Homebrew):"
    echo "  brew install --cask drag-scroll"
    echo ""
    echo "METHOD 2 (Manual compile - requires full Xcode):"
    echo "  1. Install Xcode from the Mac App Store (it's free but 10GB+)"
    echo "  2. Open Xcode once to accept the license"
    echo "  3. Run these commands:"
    echo "     git clone https://github.com/emreyolcu/drag-scroll.git"
    echo "     cd drag-scroll"
    echo "     xcodebuild -project DragScroll.xcodeproj -configuration Release"
    echo "     cp -R build/Release/DragScroll.app /Applications/"
    echo ""
    echo "METHOD 3 (Pre-built binary - if available):"
    echo "  1. Go to: https://github.com/emreyolcu/drag-scroll/releases"
    echo "  2. Download DragScroll.app.zip"
    echo "  3. Unzip and drag DragScroll.app to /Applications"
    echo "  4. Run: xattr -dr com.apple.quarantine /Applications/DragScroll.app"
    echo ""
    echo "After installing DragScroll, run this installer again."
    exit 1
fi
echo ""

# Install Python dependencies
echo "==> Installing Python dependencies..."
python3 -m pip install --user --upgrade pip --quiet 2>/dev/null || true
python3 -m pip install --user rumps pyobjc-framework-Cocoa --quiet

echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Fix rumps for Python 3.10+
PYTHON_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")
if [ "$PYTHON_MINOR" -ge 10 ]; then
    echo "==> Fixing rumps for Python 3.10+..."
    RUMPS_PATH=$(python3 -c "import rumps, os; print(os.path.dirname(rumps.__file__))" 2>/dev/null)
    
    if [ -n "$RUMPS_PATH" ] && [ -f "$RUMPS_PATH/rumps.py" ]; then
        [ ! -f "$RUMPS_PATH/rumps.py.backup" ] && cp "$RUMPS_PATH/rumps.py" "$RUMPS_PATH/rumps.py.backup"
        sed -i '' 's/from collections import Mapping, Iterable/from collections.abc import Mapping, Iterable, MutableMapping/g' "$RUMPS_PATH/rumps.py" 2>/dev/null || true
        echo -e "${GREEN}✓ Fixed${NC}"
    fi
    echo ""
fi

# Configure DragScroll defaults
echo "==> Setting default configuration..."
defaults write com.emreyolcu.DragScroll keys -array control option
defaults write com.emreyolcu.DragScroll speed -int 3
defaults write com.emreyolcu.DragScroll button -int 0
echo -e "${GREEN}✓ Configured for Ctrl+Option, Normal speed${NC}"
echo ""

echo "==> Installation complete!"
echo ""
echo -e "${YELLOW}IMPORTANT: Grant Accessibility Permissions${NC}"
echo ""
echo "1. Open System Settings → Privacy & Security → Accessibility"
echo "2. Click + and add /Applications/DragScroll.app"
echo "3. Ensure it's checked"
echo ""
echo -e "${GREEN}Launch the app:${NC}"
echo "  python3 src/dragscrollv2.py"
echo ""
read -p "Press Enter to open System Settings..."

open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
