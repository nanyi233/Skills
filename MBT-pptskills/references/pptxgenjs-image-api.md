# pptxgenjs addImage API 参考

本文档说明如何在 pptxgenjs 中使用 `addImage()` 方法插入图片。

---

## 基本语法

```javascript
slide.addImage({
  path: "path/to/image.png",
  x: 1.0,
  y: 1.0,
  w: 2.0,
  h: 2.0
});
```

---

## 参数详解

### 必需参数

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `path` | String | 图片路径（相对或绝对） | `"./assets/logo.png"` |
| `x` | Number | 左上角 X 坐标（英寸） | `1.0` |
| `y` | Number | 左上角 Y 坐标（英寸） | `1.5` |
| `w` | Number | 宽度（英寸） | `2.0` |
| `h` | Number | 高度（英寸） | `1.5` |

### 可选参数

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `sizing` | Object | 图片缩放模式 | `null` |
| `hyperlink` | Object | 超链接配置 | `null` |
| `rounding` | Boolean | 圆角 | `false` |
| `transparency` | Number | 透明度（0-100） | `0` |

---

## 图片路径

### 相对路径（推荐）

```javascript
slide.addImage({
  path: "./assets/placeholder.png",  // 相对于脚本所在目录
  x: 1.0, y: 1.0, w: 2.0, h: 2.0
});
```

**优点**：跨机器可移植，不依赖绝对路径

### 绝对路径（不推荐）

```javascript
slide.addImage({
  path: "C:/Users/xxx/project/assets/image.png",
  x: 1.0, y: 1.0, w: 2.0, h: 2.0
});
```

**缺点**：在不同机器上路径会失效

### 支持的图片格式

- PNG（推荐，支持透明背景）
- JPG / JPEG
- GIF
- SVG（部分支持）

---

## sizing 选项

用于控制图片如何填充指定区域。

### type: "contain"（保持比例，完整显示）

```javascript
slide.addImage({
  path: "./assets/icon.png",
  x: 1.0, y: 1.0, w: 2.0, h: 2.0,
  sizing: {
    type: "contain",
    w: 2.0,
    h: 2.0
  }
});
```

- 图片完整显示在框内
- 保持原始比例
- 如果图片比例与框不匹配，会有留白

**适用场景**：图标、logo、需要完整显示的图片

### type: "cover"（裁剪以填充）

```javascript
slide.addImage({
  path: "./assets/background.jpg",
  x: 0, y: 0, w: 10, h: 5.625,
  sizing: {
    type: "cover",
    w: 10,
    h: 5.625
  }
});
```

- 填充整个框，可能裁剪图片
- 保持原始比例
- 无留白

**适用场景**：背景图、需要填满区域的配图

### type: "crop"（裁剪指定区域）

```javascript
slide.addImage({
  path: "./assets/photo.jpg",
  x: 1.0, y: 1.0, w: 3.0, h: 2.0,
  sizing: {
    type: "crop",
    x: 100,    // 裁剪起始点 X（像素）
    y: 50,     // 裁剪起始点 Y（像素）
    w: 600,    // 裁剪宽度（像素）
    h: 400     // 裁剪高度（像素）
  }
});
```

**适用场景**：只需要图片的一部分

---

## 常见场景示例

### 1. 卡片顶部图标（1×1 英寸正方形）

```javascript
// IMAGE-01: 核心观点 - 知识内化图标
slide.addImage({
  path: "./assets/placeholder.png",
  x: cx + 0.9,   // 卡片中心（假设 cx=0.6, 卡片宽2.8）
  y: cy + 0.15,  // 卡片顶部偏移
  w: 1.0,
  h: 1.0,
  sizing: {
    type: "contain",
    w: 1.0,
    h: 1.0
  }
});
```

### 2. 标题页右侧大型配图（3×3 英寸）

```javascript
// IMAGE-04: 标题页 - 成长路径概念图
slide.addImage({
  path: "./assets/placeholder.png",
  x: 6.5,
  y: 1.5,
  w: 3.0,
  h: 3.0,
  sizing: {
    type: "contain",
    w: 3.0,
    h: 3.0
  }
});
```

### 3. 全屏背景图（16:9）

```javascript
slide.addImage({
  path: "./assets/background.jpg",
  x: 0,
  y: 0,
  w: 10,
  h: 5.625,
  sizing: {
    type: "cover",
    w: 10,
    h: 5.625
  }
});
```

### 4. 带透明度的装饰图

```javascript
slide.addImage({
  path: "./assets/decoration.png",
  x: 7.0,
  y: 0.5,
  w: 2.5,
  h: 2.5,
  transparency: 30  // 30% 透明度
});
```

---

## 坐标计算技巧

### 居中对齐

```javascript
// 假设卡片：cx = 0.6, cardW = 2.8
// 图片：imgW = 1.0
const imgX = cx + (cardW - imgW) / 2;  // 0.6 + (2.8 - 1.0) / 2 = 1.5
```

### 右对齐

```javascript
const imgX = cx + cardW - imgW - padding;
```

### 垂直居中

```javascript
const imgY = cy + (cardH - imgH) / 2;
```

---

## 图片编号注释规范

每个 `addImage` 前必须添加注释，格式：

```javascript
// IMAGE-XX: SLIDE N, 位置描述 - 用途说明
```

示例：

```javascript
// IMAGE-01: SLIDE 2, 第1张卡片 - 知识内化图标
slide.addImage({
  path: "./assets/placeholder.png",
  x: 1.5, y: 2.55, w: 1.0, h: 1.0,
  sizing: { type: "contain", w: 1.0, h: 1.0 }
});

// IMAGE-02: SLIDE 2, 第2张卡片 - 项目构建图标
slide.addImage({
  path: "./assets/placeholder.png",
  x: 4.6, y: 2.55, w: 1.0, h: 1.0,
  sizing: { type: "contain", w: 1.0, h: 1.0 }
});
```

**作用**：
- 便于后期替换图片时定位
- 生成 PROMPTS.md 时提取编号和描述

---

## 常见错误

### 1. 路径错误

❌ **错误**：
```javascript
path: "C:\Users\xxx\image.png"  // Windows 反斜杠会被转义
```

✅ **正确**：
```javascript
path: "./assets/image.png"  // 使用正斜杠或相对路径
```

### 2. 尺寸超出幻灯片

❌ **错误**：
```javascript
x: 9.0, w: 3.0  // 9 + 3 = 12 > 10（幻灯片宽度）
```

✅ **正确**：
```javascript
x: 7.0, w: 3.0  // 7 + 3 = 10（刚好填满）
```

### 3. 图片不存在

如果 `path` 指向的文件不存在，pptxgenjs 会静默失败（PPT 中该位置为空）。

**解决**：
- 使用占位图（确保文件存在）
- 生成 PPT 前检查图片路径

---

## 与 addText 的对比

| 功能 | addText | addImage |
|------|---------|----------|
| 插入文字 | ✅ | ❌ |
| 插入图片 | ❌ | ✅ |
| 支持 emoji | ✅（但显示效果差） | ❌ |
| 透明背景 | ❌ | ✅（PNG） |
| 缩放模式 | ❌ | ✅（contain/cover/crop） |
| 视觉质感 | 低（emoji 廉价） | 高（真实图片） |

**结论**：用 `addImage` 代替 `addText(emoji)`，提升 PPT 视觉质感。

---

## 完整示例：替换 emoji

### 旧代码（使用 emoji）

```javascript
const pillars = [
  { title: "是否自己会", icon: "🧠" },
  { title: "是否有项目", icon: "🛠️" },
  { title: "是否能讲", icon: "🎤" }
];

pillars.forEach((p, i) => {
  const cx = 0.6 + i * 3.1;
  const cy = 2.3;
  
  // 卡片背景
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: cx, y: cy, w: 2.8, h: 2.6,
    fill: { color: "132E5B" }
  });
  
  // ❌ emoji（廉价感）
  slide.addText(p.icon, {
    x: cx, y: cy + 0.25, w: 2.8, h: 0.6,
    fontSize: 28, align: "center"
  });
});
```

### 新代码（使用图片）

```javascript
const pillars = [
  { title: "是否自己会", imageId: "IMAGE-01" },
  { title: "是否有项目", imageId: "IMAGE-02" },
  { title: "是否能讲", imageId: "IMAGE-03" }
];

pillars.forEach((p, i) => {
  const cx = 0.6 + i * 3.1;
  const cy = 2.3;
  
  // 卡片背景
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: cx, y: cy, w: 2.8, h: 2.6,
    fill: { color: "132E5B" }
  });
  
  // ✅ 图片（专业质感）
  // IMAGE-01/02/03: SLIDE 2, 卡片图标
  slide.addImage({
    path: "./assets/placeholder.png",
    x: cx + 0.9,   // 居中（0.6 + (2.8-1.0)/2）
    y: cy + 0.15,  // 稍微上移
    w: 1.0,
    h: 1.0,
    sizing: { type: "contain", w: 1.0, h: 1.0 }
  });
});
```

---

## 参考资料

- pptxgenjs 官方文档：https://gitbrent.github.io/PptxGenJS/docs/api-images.html
- 示例代码：`E:\Dev\教案2026年6月12日\create-ppt.js`
- 设计规范：`design-guidelines.md`

---

**最后更新**：2026-06-12
