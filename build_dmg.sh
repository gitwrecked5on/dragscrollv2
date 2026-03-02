#!/bin/bash
# build_dmg.sh
#
# Builds DragScrollV2.app and packages it as a DMG installer.
#
# Run this once to produce the distributable DMG.
# The DMG is what you upload to GitHub releases.
#
# Prerequisites: Python 3, pip (pyinstaller gets auto-installed if missing)

set -e  # Exit on any error

echo "🚀 Building DragScrollV2..."
echo ""

# ─────────────────────────────────────────
# Colors
# ─────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ─────────────────────────────────────────
# Step 1: Download and install DragScroll if not present
# The spec file bundles it inside DragScrollV2.app, so it must exist
# in /Applications at build time.
# ─────────────────────────────────────────
echo "==> Checking for DragScroll.app..."

if [ ! -d "/Applications/DragScroll.app" ]; then
    echo -e "${YELLOW}   DragScroll not found - downloading...${NC}"

    TMP_ZIP="/tmp/DragScroll_build.zip"
    rm -f "$TMP_ZIP"

    # Official download URL from github.com/emreyolcu/drag-scroll
    DRAGSCROLL_URL="https://github.com/emreyolcu/drag-scroll/releases/download/v1.3.1/DragScroll.zip"

    if ! curl -L -f --silent --show-error "$DRAGSCROLL_URL" -o "$TMP_ZIP"; then
        echo -e "${RED}✗ Download failed. Check your internet connection.${NC}"
        exit 1
    fi

    unzip -oq "$TMP_ZIP" -d /Applications/
    # Remove quarantine flag so macOS allows it to run
    xattr -dr com.apple.quarantine /Applications/DragScroll.app 2>/dev/null || true
    rm -f "$TMP_ZIP"

    echo -e "${GREEN}   ✓ DragScroll installed${NC}"
else
    echo -e "${GREEN}   ✓ DragScroll.app found${NC}"
fi
echo ""

# ─────────────────────────────────────────
# Step 2: Check required source files exist
# ─────────────────────────────────────────
for f in src/dragscrollv2.py dragscrollv2.spec icon.png; do
    if [ ! -f "$f" ]; then
        echo -e "${RED}✗ Missing required file: $f${NC}"
        exit 1
    fi
done
echo -e "${GREEN}==> Source files OK${NC}"
echo ""

# ─────────────────────────────────────────
# Step 3: Install Python dependencies
# ─────────────────────────────────────────
echo "==> Installing Python dependencies..."
python3 -m pip install --user --quiet rumps pyobjc-framework-Cocoa pyinstaller
echo -e "${GREEN}   ✓ Dependencies ready${NC}"
echo ""

# ─────────────────────────────────────────
# Step 4: Clean old builds
# ─────────────────────────────────────────
echo "==> Cleaning old builds..."
rm -rf build dist
echo -e "${GREEN}   ✓ Clean${NC}"
echo ""

# ─────────────────────────────────────────
# Step 5: Build the .app with PyInstaller
# Uses dragscrollv2.spec which bundles DragScroll.app inside DragScrollV2.app
# ─────────────────────────────────────────
echo "==> Building DragScrollV2.app (this takes ~1 minute)..."
python3 -m PyInstaller --clean --noconfirm dragscrollv2.spec

if [ ! -d "dist/DragScrollV2.app" ]; then
    echo -e "${RED}✗ Build failed - dist/DragScrollV2.app not found${NC}"
    exit 1
fi
echo -e "${GREEN}   ✓ App built${NC}"
echo ""

# ─────────────────────────────────────────
# Step 6: Package into a DMG
# Creates a nice installer: user opens DMG, drags app to Applications
# ─────────────────────────────────────────
echo "==> Creating DMG..."

DMG_NAME="DragScrollV2-v1.0.dmg"
DMG_TEMP="dmg_temp"

rm -f "$DMG_NAME"
rm -rf "$DMG_TEMP"
mkdir "$DMG_TEMP"

# Copy built app into temp folder
cp -R "dist/DragScrollV2.app" "$DMG_TEMP/"

# Add a symlink to /Applications so users can drag-install easily
ln -s /Applications "$DMG_TEMP/Applications"

# Create the compressed DMG
hdiutil create \
    -volname "DragScrollV2" \
    -srcfolder "$DMG_TEMP" \
    -ov \
    -format UDZO \
    "$DMG_NAME"

rm -rf "$DMG_TEMP"

# Clean up PyInstaller intermediate files now that DMG is created.
# Only needed during the build - the DMG has everything packaged.
# To keep for debugging, comment out the two lines below.
rm -rf build dist

echo -e "${GREEN}   ✓ Created $DMG_NAME ($(du -h "$DMG_NAME" | cut -f1))${NC}"
echo ""

# ─────────────────────────────────────────
# Done
# ─────────────────────────────────────────
echo -e "${GREEN}✅ BUILD COMPLETE${NC}"
echo ""
echo "Distributable: $DMG_NAME"
echo ""
echo "Next steps:"
echo "  1. Double-click $DMG_NAME to test the installer"
echo "  2. Drag DragScrollV2 → Applications"
echo "  3. Launch DragScrollV2 - it will install DragScroll automatically"
echo "  4. Grant Accessibility permissions to DragScroll (not DragScrollV2) when prompted"
echo "  4. Restart DragScrollV2"