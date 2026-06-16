# AI 绘图提示词清单模板

本文档是 MBT-pptskills 生成的 PROMPTS.md 的格式示例。

---

## 使用说明

1. 将下表中的提示词输入 **Midjourney**、**DALL-E** 或 **Stable Diffusion**
2. 生成的图片保存为对应编号（如 `01-knowledge-icon.png`）
3. 在 `create-ppt.js` 中，将对应的 `path: "./assets/placeholder.png"` 改为 `path: "./assets/01-knowledge-icon.png"`
4. 重新运行 `node create-ppt.js` 生成最终 PPT

---

## 提示词表格

| 编号 | 位置 | 用途 | 尺寸建议 | AI 绘图提示词（英文） |
|------|------|------|----------|---------------------|
| IMAGE-01 | SLIDE 2, 第1张卡片 | 知识内化图标 | 1024×1024 | minimalist line art icon of a brain with circuit patterns, representing knowledge mastery, clean blue and white color scheme, transparent background, modern flat design |
| IMAGE-02 | SLIDE 2, 第2张卡片 | 项目构建图标 | 1024×1024 | minimalist line art icon of tools and gears, representing project building and hands-on work, clean blue and white color scheme, transparent background, modern flat design |
| IMAGE-03 | SLIDE 2, 第3张卡片 | 教学能力图标 | 1024×1024 | minimalist line art icon of a person presenting or teaching, representing communication and teaching ability, clean blue and white color scheme, transparent background, modern flat design |
| IMAGE-04 | SLIDE 1, 右侧配图 | 成长路径概念图 | 2048×2048 | abstract illustration of a person climbing stairs towards expertise, growth journey concept, blue gradient background, modern minimalist style |
| IMAGE-05 | SLIDE 6, 左侧引用块 | 费曼学习法插图 | 1024×1024 | illustration of Feynman technique, teacher explaining to students, knowledge transfer concept, clean blue and white color scheme, modern flat design |

---

## 提示词撰写技巧

### 基本结构
```
[主体描述] + [风格] + [配色方案] + [背景] + [细节要求]
```

### 示例拆解

**IMAGE-01 提示词**：
```
minimalist line art icon of a brain with circuit patterns,
representing knowledge mastery,
clean blue and white color scheme,
transparent background,
modern flat design
```

拆解：
- **主体**：brain with circuit patterns（带电路图案的大脑）
- **用途**：representing knowledge mastery（代表知识掌握）
- **风格**：minimalist line art icon（极简线条图标）
- **配色**：clean blue and white（蓝白配色）
- **背景**：transparent background（透明背景，便于叠加）
- **细节**：modern flat design（现代扁平化设计）

### 配色建议

根据 PPT 配色方案（参考 `design-guidelines.md`）：
- 主色调：蓝色 (#00B4D8, #48CAE4)
- 强调色：金色 (#FFB703)
- 背景：深蓝 (#0B1D3A) 或透明

提示词中常用配色描述：
- `clean blue and white color scheme`（蓝白配色）
- `blue gradient with gold accents`（蓝色渐变 + 金色点缀）
- `dark blue background with cyan highlights`（深蓝背景 + 青色高光）

### 风格关键词

- **极简风格**：minimalist, clean, simple, flat design
- **线条艺术**：line art, outline icon, stroke illustration
- **现代科技**：modern, tech, digital, futuristic
- **手绘风格**：hand-drawn, sketchy, illustrative
- **3D 立体**：3D render, isometric, depth

---

## 尺寸规范

| 用途 | 推荐尺寸 | 原因 |
|------|----------|------|
| 卡片图标（1×1 英寸） | 1024×1024 px | 正方形，高清，适合缩放 |
| 大型配图（3×3 英寸） | 2048×2048 px | 更大尺寸，细节丰富 |
| 横向配图（2×1.5 英寸） | 1920×1440 px | 16:12 横向比例 |
| 竖向配图（1×1.5 英寸） | 1024×1536 px | 2:3 竖向比例 |

**提示**：始终生成比实际显示尺寸更大的图片（至少 1024px），以确保在高分辨率投影时不失真。

---

## 常见图标主题示例

### 知识/学习类
- `brain with circuit patterns`（电路大脑）
- `light bulb with gears`（齿轮灯泡）
- `book with growing tree`（书本与成长之树）
- `graduation cap with data flow`（学位帽与数据流）

### 项目/实践类
- `tools and gears`（工具与齿轮）
- `building blocks stacking`（积木堆叠）
- `code editor with binary`（代码编辑器与二进制）
- `hands assembling puzzle`（组装拼图）

### 教学/沟通类
- `person presenting at board`（演讲者与白板）
- `speech bubble with knowledge`（知识对话气泡）
- `network of connected people`（人际网络）
- `megaphone with sound waves`（扩音器与声波）

### 成长/进步类
- `stairs ascending`（上升的楼梯）
- `arrow pointing upward with milestones`（向上箭头与里程碑）
- `plant growing from seed to tree`（从种子到大树）
- `mountain peak with path`（山峰与路径）

---

## Midjourney 特定参数（可选）

如果使用 Midjourney，可在提示词后添加参数：

```
minimalist line art icon of a brain with circuit patterns, clean blue and white color scheme, transparent background --v 6 --ar 1:1 --style raw
```

常用参数：
- `--v 6`：使用 Midjourney v6 模型
- `--ar 1:1`：1:1 正方形比例
- `--ar 16:9`：16:9 横向比例
- `--style raw`：更真实的风格
- `--s 50`：风格化程度（0-1000，默认 100）

---

## 批量生成建议

1. **先生成关键图标**（如 SLIDE 2 的 3 张卡片图标）
2. **验证风格一致性**（确保所有图标视觉风格统一）
3. **批量生成次要配图**（标题页装饰、引用块配图等）
4. **替换 PPT 后预览**（确认尺寸、位置、对比度）

---

## 版权说明

- 使用 AI 生成的图片版权归用户所有（根据各平台政策）
- 商业使用前请确认所用 AI 工具的版权条款
- 建议标注"AI Generated"或工具名称（如"Created with Midjourney"）

---

## 示例：完整的 3 卡片图标提示词

**场景**：PPT 讲"如何成为专家"，需要 3 张卡片图标

| 编号 | 用途 | 提示词 |
|------|------|--------|
| IMAGE-01 | 知识掌握 | `minimalist line art icon of a brain with glowing neural connections, representing deep knowledge and mastery, blue and cyan color palette, transparent background, modern tech style, high detail` |
| IMAGE-02 | 项目实践 | `minimalist line art icon of hands building with gears and tools, representing hands-on project work, blue and gold color palette, transparent background, modern tech style, high detail` |
| IMAGE-03 | 教学输出 | `minimalist line art icon of a person standing at a podium presenting, representing teaching and communication skills, blue and white color palette, transparent background, modern tech style, high detail` |

**风格保持一致**：所有提示词都包含 `minimalist line art icon` + `transparent background` + `modern tech style`，确保视觉统一。

---

**生成日期**：2026-06-12  
**PPT 主题**：[在此填写具体 PPT 主题]  
**配色方案**：深蓝科技风（参考 design-guidelines.md）
