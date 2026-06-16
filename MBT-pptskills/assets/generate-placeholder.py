"""
生成占位图的 Python 脚本
使用 PIL/Pillow 创建 1024x1024 的灰底占位图
"""
from PIL import Image, ImageDraw, ImageFont
import os

# 创建 1024x1024 的图片
width, height = 1024, 1024
img = Image.new('RGB', (width, height), color='#E0E0E0')

# 绘制文字
draw = ImageDraw.Draw(img)
text = "Image Placeholder"

# 尝试使用系统字体，如果失败则使用默认字体
try:
    # Windows 常见字体路径
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 60)
except:
    # 使用默认字体
    font = ImageFont.load_default()

# 计算文字位置（居中）
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x = (width - text_width) / 2
y = (height - text_height) / 2

# 绘制文字
draw.text((x, y), text, fill='#666666', font=font)

# 保存图片
output_path = os.path.join(os.path.dirname(__file__), 'placeholder.png')
img.save(output_path, 'PNG')

print(f'Placeholder image created: {output_path}')
