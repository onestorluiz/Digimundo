#!/bin/bash

# Create a simple icon using ImageMagick (if available) or generate placeholder
echo "🎨 Creating Digimundo icon..."

# Create assets directory if it doesn't exist
mkdir -p assets

# Check if ImageMagick is installed
if command -v convert &> /dev/null; then
    echo "Creating icon with ImageMagick..."
    
    # Create a simple icon with gradient and text
    convert -size 1024x1024 \
        -background 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' \
        -fill white \
        -font Arial-Bold \
        -pointsize 300 \
        -gravity center \
        -annotate +0+0 'D' \
        xc:transparent \
        assets/icon.png
    
    # Convert to icns format for macOS
    if command -v iconutil &> /dev/null; then
        mkdir -p assets/icon.iconset
        sips -z 16 16     assets/icon.png --out assets/icon.iconset/icon_16x16.png
        sips -z 32 32     assets/icon.png --out assets/icon.iconset/icon_16x16@2x.png
        sips -z 32 32     assets/icon.png --out assets/icon.iconset/icon_32x32.png
        sips -z 64 64     assets/icon.png --out assets/icon.iconset/icon_32x32@2x.png
        sips -z 128 128   assets/icon.png --out assets/icon.iconset/icon_128x128.png
        sips -z 256 256   assets/icon.png --out assets/icon.iconset/icon_128x128@2x.png
        sips -z 256 256   assets/icon.png --out assets/icon.iconset/icon_256x256.png
        sips -z 512 512   assets/icon.png --out assets/icon.iconset/icon_256x256@2x.png
        sips -z 512 512   assets/icon.png --out assets/icon.iconset/icon_512x512.png
        sips -z 1024 1024 assets/icon.png --out assets/icon.iconset/icon_512x512@2x.png
        
        iconutil -c icns assets/icon.iconset -o assets/icon.icns
        rm -rf assets/icon.iconset
        echo "✅ Icon created successfully!"
    fi
else
    echo "ImageMagick not found. Creating placeholder icon..."
    # Create a simple SVG as placeholder
    cat > assets/icon.svg << 'EOF'
<svg width="1024" height="1024" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="1024" height="1024" rx="200" fill="url(#grad)"/>
  <text x="512" y="600" font-family="Arial" font-size="400" font-weight="bold" text-anchor="middle" fill="white">D</text>
</svg>
EOF
    echo "⚠️  Placeholder SVG created. Install ImageMagick for proper icon generation."
fi

echo "📦 Icon assets ready in ./assets/"