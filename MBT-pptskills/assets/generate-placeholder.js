// 生成占位图的 Node.js 脚本
const { createCanvas } = require('canvas');
const fs = require('fs');
const path = require('path');

const width = 1024;
const height = 1024;

const canvas = createCanvas(width, height);
const ctx = canvas.getContext('2d');

// 背景色 #E0E0E0
ctx.fillStyle = '#E0E0E0';
ctx.fillRect(0, 0, width, height);

// 绘制中心文字 "Image Placeholder"
ctx.fillStyle = '#666666';
ctx.font = 'bold 60px Arial';
ctx.textAlign = 'center';
ctx.textBaseline = 'middle';
ctx.fillText('Image Placeholder', width / 2, height / 2);

// 保存为 PNG
const buffer = canvas.toBuffer('image/png');
const outputPath = path.join(__dirname, 'placeholder.png');
fs.writeFileSync(outputPath, buffer);

console.log('✅ Placeholder image created:', outputPath);
