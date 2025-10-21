#!/bin/bash

echo "Creating Digimundo icon..."

# Create a simple icon using ImageMagick or sips
# This creates a purple gradient icon with the Digimundo star

mkdir -p assets

# Create a simple icon using system tools
cat > assets/icon.svg << 'EOF'
<svg width="1024" height="1024" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#8B5CF6;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#EC4899;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="1024" height="1024" rx="230" fill="url(#bg)"/>
  <text x="512" y="580" font-family="system-ui" font-size="500" fill="white" text-anchor="middle">⭐</text>
</svg>
EOF

# Convert SVG to PNG (requires rsvg-convert or similar)
# For now, create a simple colored square as placeholder
sips -s format png -s formatOptions best -z 1024 1024 -s dpiHeight 72 -s dpiWidth 72 \
     --out assets/icon.png << EOF
/System/Library/Desktop\ Pictures/Solid\ Colors/Purple.png
EOF 2>/dev/null || true

# Create ICNS for macOS (simplified version)
mkdir -p assets/icon.iconset
sips -z 16 16     assets/icon.png --out assets/icon.iconset/icon_16x16.png 2>/dev/null || true
sips -z 32 32     assets/icon.png --out assets/icon.iconset/icon_16x16@2x.png 2>/dev/null || true
sips -z 32 32     assets/icon.png --out assets/icon.iconset/icon_32x32.png 2>/dev/null || true
sips -z 64 64     assets/icon.png --out assets/icon.iconset/icon_32x32@2x.png 2>/dev/null || true
sips -z 128 128   assets/icon.png --out assets/icon.iconset/icon_128x128.png 2>/dev/null || true
sips -z 256 256   assets/icon.png --out assets/icon.iconset/icon_128x128@2x.png 2>/dev/null || true
sips -z 256 256   assets/icon.png --out assets/icon.iconset/icon_256x256.png 2>/dev/null || true
sips -z 512 512   assets/icon.png --out assets/icon.iconset/icon_256x256@2x.png 2>/dev/null || true
sips -z 512 512   assets/icon.png --out assets/icon.iconset/icon_512x512.png 2>/dev/null || true
sips -z 1024 1024 assets/icon.png --out assets/icon.iconset/icon_512x512@2x.png 2>/dev/null || true

# Convert to ICNS
iconutil -c icns assets/icon.iconset -o assets/icon.icns 2>/dev/null || true

# Copy for tray icon
cp assets/icon.png assets/tray-icon.png 2>/dev/null || true

# Create DMG background
echo '<?xml version="1.0" encoding="UTF-8"?>
<svg width="540" height="380" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="dmgbg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1a1a2e;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0f0f23;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="540" height="380" fill="url(#dmgbg)"/>
  <text x="270" y="100" font-family="system-ui" font-size="48" fill="white" text-anchor="middle" opacity="0.8">Digimundo</text>
  <text x="270" y="140" font-family="system-ui" font-size="16" fill="white" text-anchor="middle" opacity="0.6">Drag to Applications folder to install</text>
</svg>' > assets/dmg-background.svg

echo "✅ Icons created (placeholder)"