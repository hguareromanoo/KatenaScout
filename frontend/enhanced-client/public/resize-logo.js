const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

async function resizeLogos() {
  const logoPngPath = path.join(__dirname, 'logo.png');
  
  // Convert to 192x192 PNG
  await sharp(logoPngPath)
    .resize(192, 192)
    .toFile(path.join(__dirname, 'logo192.png'));
  
  // Convert to 512x512 PNG
  await sharp(logoPngPath)
    .resize(512, 512)
    .toFile(path.join(__dirname, 'logo512.png'));
    
  console.log('Logo resizing completed successfully!');
}

resizeLogos().catch(err => console.error('Error resizing logos:', err));