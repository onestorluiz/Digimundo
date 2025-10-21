const { createCanvas } = require('canvas');
const fs = require('fs');
const path = require('path');

function createDMGBackground() {
  const width = 540;
  const height = 380;
  const canvas = createCanvas(width, height);
  const ctx = canvas.getContext('2d');

  // Gradient background
  const gradient = ctx.createLinearGradient(0, 0, width, height);
  gradient.addColorStop(0, '#1a1a2e');
  gradient.addColorStop(0.5, '#16213e');
  gradient.addColorStop(1, '#0f3460');

  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, width, height);

  // Grid pattern
  ctx.strokeStyle = 'rgba(102, 126, 234, 0.1)';
  ctx.lineWidth = 1;
  
  for (let i = 0; i < width; i += 20) {
    ctx.beginPath();
    ctx.moveTo(i, 0);
    ctx.lineTo(i, height);
    ctx.stroke();
  }
  
  for (let i = 0; i < height; i += 20) {
    ctx.beginPath();
    ctx.moveTo(0, i);
    ctx.lineTo(width, i);
    ctx.stroke();
  }

  // Title
  ctx.fillStyle = 'white';
  ctx.font = 'bold 36px Arial';
  ctx.textAlign = 'center';
  ctx.fillText('Digimundo', width / 2, 60);

  // Subtitle
  ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
  ctx.font = '16px Arial';
  ctx.fillText('AI-powered Digital Companions', width / 2, 90);

  // Arrow instruction
  ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
  ctx.font = '14px Arial';
  ctx.fillText('Drag to Applications folder →', width / 2, height - 30);

  // Save
  const buffer = canvas.toBuffer('image/png');
  fs.writeFileSync(path.join(__dirname, 'assets', 'dmg-background.png'), buffer);
  console.log('✅ DMG background created');
}

createDMGBackground();