const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

async function convertSvgToPng() {
  const logoSvgPath = path.join(__dirname, 'logo.svg');
  const logoSvg = fs.readFileSync(logoSvgPath);
  
  // Convert to 192x192 PNG
  await sharp(logoSvg)
    .resize(192, 192)
    .toFile(path.join(__dirname, 'logo192.png'));
  
  // Convert to 512x512 PNG
  await sharp(logoSvg)
    .resize(512, 512)
    .toFile(path.join(__dirname, 'logo512.png'));
    
  console.log('SVG to PNG conversion completed successfully!');
}

convertSvgToPng().catch(err => console.error('Error converting SVG to PNG:', err));