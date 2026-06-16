---
name: MBT-pptskills
description: 生成专业 PPT（.pptx），不使用 emoji/icon，必须插入图片占位 + AI 绘图提示词。当用户说"做个 PPT"、"生成演示文稿"、"制作幻灯片"、"帮我做个课件"、或提供 PPT 主题时触发。输出 Node.js 脚本（pptxgenjs）+ assets/PROMPTS.md 提示词文档。
---

# MBT-pptskills

告别 AI 廉价感，生成有视觉质感的专业 PPT。

---

## 核心理念

**问题**：AI 生成的 PPT 往往使用 emoji（🧠🛠️🎤）作为图标，看起来廉价、不专业。

**解决方案**：
1. **不使用 emoji/icon** —— 用真实图片代替
2. **占位 + 提示词工作流** —— 先生成带占位图的 PPT（可预览结构），同时生成 `assets/PROMPTS.md`（AI 绘图提示词清单）
3. **用户后期批量替换** —— 根据提示词生成图片（Midjourney/DALL-E），替换占位图，得到最终专业 PPT

**设计系统优先**：复用配色、字体、布局模式，确保视觉一致性。

---

## 触发方式

当用户说以下内容时，主动触发此 skill：
- "做个 XXX 的 PPT"
- "生成 XXX 演示文稿"
- "制作 XXX 幻灯片"
- "帮我做个关于 XXX 的课件"
- "用 MBT-pptskills 做 PPT"

---

## 实施流程

### Step 1: 理解主题和结构

询问用户（如果信息不全）：
1. **PPT 主题**：讲什么内容？
2. **目标受众**：给谁看？（学生、团队、客户）
3. **幻灯片数量**：建议 5-10 张（标题页 + 3-7 张内容页 + 结论页）
4. **章节结构**：是否有明确的章节划分？

如果用户已提供详细信息（如"重新做'三年成为专家'PPT"），直接使用现有内容。

---

### Step 2: 设计幻灯片布局

为每张幻灯片选择合适的布局模式。参考 `design-guidelines.md` 中的典型布局：

#### 常用布局模式

1. **标题页**
   - 大标题 + 副标题 + 装饰元素
   - 可选：右侧大型配图（3×3 英寸）

2. **卡片式布局**（2-5 张卡片横排或网格）
   - 每张卡片：**顶部图片**（1×1 英寸）+ 标题 + 描述
   - 适合：核心观点、特征列表、对比

3. **时间轴布局**
   - 横向时间线 + 节点 + 下方卡片
   - 适合：成长路径、步骤流程

4. **金字塔布局**
   - 渐进式堆叠（从下到上宽度递减）
   - 适合：层次结构、学习深度

5. **引用块 + 列表**
   - 左侧大引用块 + 右侧行动卡片
   - 适合：方法论、最佳实践

6. **结论页**
   - 大引用 + 行动建议 + 装饰元素

#### 图片插入规则

**重要**：至少每张幻灯片插入 1 张图片，关键页面 2-3 张。

图片位置：
- 卡片顶部：替代 emoji（1×1 英寸）
- 标题页右侧：大型配图（3×3 英寸）
- 引用块配图：横向配图（2×1.5 英寸）
- 时间轴节点：小图标（0.8×0.8 英寸）

---

### Step 3: 生成 create-ppt.js

生成完整的 Node.js 脚本，基于 pptxgenjs。

#### 代码结构

```javascript
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Claude";
pres.title = "PPT 主题";

// 配色方案（参考 design-guidelines.md）
const C = {
  darkBg: "0B1D3A",
  cardBg: "132E5B",
  accent: "00B4D8",
  gold: "FFB703",
  white: "FFFFFF",
  lightText: "CAE0F0",
  muted: "8BA4C7",
  // ... 其他颜色
};

// 阴影工厂
function cardShadow() {
  return { type: "outer", color: "000000", blur: 8, offset: 3, angle: 135, opacity: 0.25 };
}

// ===== SLIDE 1: 标题页 =====
{
  const slide = pres.addSlide();
  slide.background = { color: C.darkBg };
  
  // 装饰元素
  slide.addShape(pres.shapes.OVAL, {
    x: 6.5, y: -1.5, w: 5, h: 5,
    fill: { color: C.accent, transparency: 92 }
  });
  
  // 主标题
  slide.addText("PPT 主标题", {
    x: 0.8, y: 1.5, w: 7, h: 1.2,
    fontSize: 48, fontFace: "Arial Black", color: C.white, bold: true
  });
  
  // 可选：右侧配图
  // IMAGE-01: SLIDE 1, 右侧配图 - 主题概念图
  slide.addImage({
    path: "./assets/placeholder.png",
    x: 6.5, y: 1.5, w: 3.0, h: 3.0,
    sizing: { type: "contain", w: 3.0, h: 3.0 }
  });
}

// ===== SLIDE 2: 核心观点（3 卡片） =====
{
  const slide = pres.addSlide();
  slide.background = { color: C.darkBg };
  
  const pillars = [
    { title: "观点1", desc: "描述..." },
    { title: "观点2", desc: "描述..." },
    { title: "观点3", desc: "描述..." }
  ];
  
  pillars.forEach((p, i) => {
    const cx = 0.6 + i * 3.1;
    const cy = 2.3;
    
    // 卡片背景
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: cx, y: cy, w: 2.8, h: 2.6,
      fill: { color: C.cardBg },
      shadow: cardShadow(),
      rectRadius: 0.12
    });
    
    // ✅ 图片（代替 emoji）
    // IMAGE-0X: SLIDE 2, 第X张卡片 - XXX图标
    slide.addImage({
      path: "./assets/placeholder.png",
      x: cx + 0.9,   // 居中
      y: cy + 0.15,
      w: 1.0,
      h: 1.0,
      sizing: { type: "contain", w: 1.0, h: 1.0 }
    });
    
    // 卡片标题
    slide.addText(p.title, {
      x: cx + 0.2, y: cy + 1.25, w: 2.4, h: 0.4,
      fontSize: 16, fontFace: "Arial", color: C.white, bold: true, align: "center"
    });
    
    // 卡片描述
    slide.addText(p.desc, {
      x: cx + 0.2, y: cy + 1.7, w: 2.4, h: 0.8,
      fontSize: 12, fontFace: "Arial", color: C.muted, align: "center"
    });
  });
}

// ===== 其他幻灯片 =====
// ...

// ===== 保存 =====
const outputPath = "./output.pptx";
pres.writeFile({ fileName: outputPath }).then(() => {
  console.log("PPT saved to:", outputPath);
});
```

#### 关键要点

**a) 配色方案**

使用 `design-guidelines.md` 中定义的配色，或根据主题适当调整：
- 科技风：深蓝 + 青色
- 商务风：深灰 + 金色
- 教育风：蓝色 + 橙色

**b) 图片插入（核心）**

❌ **旧方式（emoji）**：
```javascript
slide.addText("🧠", { x, y, w, h, fontSize: 28, align: "center" });
```

✅ **新方式（图片占位）**：
```javascript
// IMAGE-01: SLIDE 2, 第1张卡片 - 知识内化图标
slide.addImage({
  path: "./assets/placeholder.png",
  x: cx + 0.9,   // 卡片内居中
  y: cy + 0.15,  // 顶部偏移
  w: 1.0,        // 1 英寸正方形
  h: 1.0,
  sizing: { type: "contain", w: 1.0, h: 1.0 }
});
```

**c) 图片编号注释**

每个 `addImage` 前必须添加注释：
```javascript
// IMAGE-XX: SLIDE N, 位置描述 - 用途说明
```

编号格式：`IMAGE-01`, `IMAGE-02`, ...（两位数字）

**d) 占位图路径**

所有 `addImage` 初始都指向统一占位图：
```javascript
path: "./assets/placeholder.png"
```

用户后期替换图片后，可手动修改路径：
```javascript
path: "./assets/01-knowledge-icon.png"
```

---

### Step 4: 生成 assets/PROMPTS.md

生成 AI 绘图提示词清单，格式参考 `PROMPTS-template.md`。

#### 文档结构

```markdown
# AI 绘图提示词清单

> 生成图片后，按编号替换 assets/ 目录下的占位图

## 使用说明

1. 将下表中的提示词输入 Midjourney/DALL-E/Stable Diffusion
2. 生成的图片保存为对应编号（如 `01-knowledge-icon.png`）
3. 在 create-ppt.js 中，将对应的 `path: "./assets/placeholder.png"` 改为 `path: "./assets/01-knowledge-icon.png"`
4. 重新运行 `node create-ppt.js` 生成最终 PPT

## 提示词表格

| 编号 | 位置 | 用途 | 尺寸建议 | AI 绘图提示词（英文） |
|------|------|------|----------|---------------------|
| IMAGE-01 | SLIDE 2, 第1张卡片 | XXX图标 | 1024×1024 | minimalist line art icon of ..., clean blue and white color scheme, transparent background, modern flat design |
| IMAGE-02 | SLIDE 2, 第2张卡片 | XXX图标 | 1024×1024 | ... |
| ... | ... | ... | ... | ... |
```

#### 提示词撰写原则

**基本结构**：
```
[主体描述] + [用途说明] + [风格] + [配色] + [背景] + [细节]
```

**示例**：
```
minimalist line art icon of a brain with circuit patterns,
representing knowledge mastery,
clean blue and white color scheme,
transparent background,
modern flat design
```

**配色关键词**（根据 PPT 配色调整）：
- `clean blue and white color scheme`（蓝白配色）
- `blue gradient with gold accents`（蓝色渐变 + 金色）
- `dark blue background with cyan highlights`（深蓝 + 青色）

**风格关键词**：
- 极简：`minimalist`, `clean`, `simple`, `flat design`
- 线条：`line art`, `outline icon`, `stroke illustration`
- 科技：`modern`, `tech`, `digital`, `futuristic`

**背景要求**：
- 优先使用 `transparent background`（便于叠加在深色背景上）
- 如果需要浅色背景：`light gray background` 或 `white background`

#### 图片数量

- 最少：3 张（对应 3 张卡片的图标）
- 推荐：5-10 张（覆盖所有幻灯片的关键位置）
- 最多：不超过 20 张（避免过度依赖图片）

---

### Step 5: 输出文件清单

生成以下文件结构：

```
项目目录/
├── create-ppt.js        # PPT 生成脚本
├── assets/
│   ├── placeholder.png  # 占位图（从 skill 复制）
│   └── PROMPTS.md       # AI 绘图提示词清单
└── output.pptx          # 生成的 PPT（运行脚本后）
```

**执行步骤**：
1. 创建 `assets/` 目录
2. 复制 `~/.claude/skills/MBT-pptskills/assets/placeholder.png` 到项目
3. 写入 `create-ppt.js`
4. 写入 `assets/PROMPTS.md`
5. 运行 `node create-ppt.js` 生成初始 PPT

**告知用户**：
```
✅ PPT 已生成！

📁 文件清单：
- create-ppt.js（生成脚本）
- assets/placeholder.png（占位图）
- assets/PROMPTS.md（AI 绘图提示词，共 X 张图片）
- output.pptx（初始 PPT，包含占位图）

📌 下一步：
1. 打开 output.pptx 预览结构和布局
2. 根据 assets/PROMPTS.md 生成图片（Midjourney/DALL-E）
3. 替换 create-ppt.js 中的图片路径（placeholder.png → 01-xxx.png）
4. 重新运行 node create-ppt.js 生成最终 PPT
```

---

## 验证步骤

生成 PPT 后，自动运行以下检查：

1. **运行脚本**：`node create-ppt.js`
2. **检查输出**：确认 `output.pptx` 已生成
3. **打开 PPT**（如果可能）：在 PowerPoint/WPS 中打开，确认：
   - 占位图已正确插入到指定位置
   - 布局不破坏（图片尺寸合适）
   - 文字层次清晰（白色主标题 → 浅色副标题 → 灰色说明）
4. **检查 PROMPTS.md**：
   - 表格完整（编号、位置、用途、尺寸、提示词）
   - 提示词描述准确（与图片用途匹配）
   - 使用英文提示词（AI 绘图工具效果更好）

---

## 用户后期工作流

用户拿到生成的文件后，按以下步骤完成最终 PPT：

### 1. 预览初始 PPT

打开 `output.pptx`，查看布局和结构，确认：
- 幻灯片数量和顺序
- 卡片位置和间距
- 文字内容和层次

如有调整需求，修改 `create-ppt.js` 重新生成。

### 2. 批量生成图片

打开 `assets/PROMPTS.md`，按表格顺序生成图片：

**使用 Midjourney**：
```
/imagine minimalist line art icon of a brain with circuit patterns, clean blue and white color scheme, transparent background, modern flat design --v 6 --ar 1:1
```

**使用 DALL-E**：
直接粘贴提示词，生成后下载。

**保存图片**：
- 编号命名：`01-knowledge-icon.png`, `02-project-icon.png`, ...
- 保存到 `assets/` 目录

### 3. 替换图片路径

在 `create-ppt.js` 中，找到对应的 `addImage`，修改路径：

```javascript
// IMAGE-01: SLIDE 2, 第1张卡片 - 知识内化图标
slide.addImage({
  path: "./assets/01-knowledge-icon.png",  // 改为实际图片路径
  x: 1.5, y: 2.55, w: 1.0, h: 1.0,
  sizing: { type: "contain", w: 1.0, h: 1.0 }
});
```

### 4. 重新生成最终 PPT

```bash
node create-ppt.js
```

打开 `output.pptx`，确认所有占位图已替换为真实图片。

---

## 设计原则

### 1. 视觉质感优先

- ✅ 真实图片（线条艺术、插画、照片）
- ❌ emoji、Unicode 符号、ASCII 艺术

### 2. 一致性

- 所有图标保持统一风格（极简线条、扁平化、插画等）
- 配色方案统一（蓝白、金色强调）
- 字体统一（Arial、Arial Black）

### 3. 呼吸感

- 卡片间距：至少 0.2 英寸
- 边距：左右 0.6-0.8 英寸
- 图片与文字间距：0.1-0.15 英寸

### 4. 层次清晰

- 主标题：48-72pt，白色
- 副标题：18-24pt，浅色
- 正文：12-14pt，浅色
- 说明：10-11pt，灰色

---

## 常见场景示例

### 场景 1：教学课件

**主题**："Python 入门教程"

**幻灯片结构**：
1. 标题页
2. 为什么学 Python（3 卡片：简单、强大、应用广）
3. Python 基础语法（代码示例 + 配图）
4. 实战项目（时间轴：爬虫 → 数据分析 → Web 开发）
5. 学习路径
6. 结论页

**图片需求**：
- IMAGE-01/02/03：3 张卡片图标（简单、强大、应用）
- IMAGE-04：代码编辑器配图
- IMAGE-05/06/07：时间轴节点图标
- 共 7 张图片

### 场景 2：团队分享

**主题**："2026 年度总结"

**幻灯片结构**：
1. 标题页
2. 核心成就（3 卡片：用户增长、营收翻倍、产品升级）
3. 关键数据（图表 + 配图）
4. 团队故事（照片墙）
5. 2027 展望
6. 结论页

**图片需求**：
- IMAGE-01/02/03：3 张卡片图标（增长、营收、产品）
- IMAGE-04：图表配图
- IMAGE-05-10：团队照片（真实照片）
- 共 10 张图片

### 场景 3：产品发布

**主题**："新产品 X 发布会"

**幻灯片结构**：
1. 标题页（产品大图）
2. 痛点分析（3 卡片）
3. 解决方案（产品截图 + 说明）
4. 核心功能（4 张卡片）
5. 定价与购买
6. 结论页

**图片需求**：
- IMAGE-01：产品渲染图（标题页）
- IMAGE-02/03/04：痛点图标
- IMAGE-05/06：产品截图
- IMAGE-07-10：功能图标
- 共 10 张图片

---

## 参考资料

- **设计规范**：`assets/design-guidelines.md`（配色、字体、布局）
- **API 文档**：`references/pptxgenjs-image-api.md`（addImage 用法）
- **提示词模板**：`assets/PROMPTS-template.md`（PROMPTS.md 格式示例）
- **现有示例**：`E:\Dev\教案2026年6月12日\create-ppt.js`（7 张幻灯片，557 行）

---

## 反面教材

❌ **不要做的事情**：

1. **不要使用 emoji**
   ```javascript
   // ❌ 错误
   slide.addText("🧠", { fontSize: 28 });
   ```

2. **不要忘记图片编号注释**
   ```javascript
   // ❌ 错误：没有注释
   slide.addImage({ path: "./assets/placeholder.png", ... });
   ```

3. **不要复用 shadow 对象**
   ```javascript
   // ❌ 错误
   const shadow = cardShadow();
   slide.addShape({ ..., shadow });
   slide.addShape({ ..., shadow });  // 复用会出错
   
   // ✅ 正确
   slide.addShape({ ..., shadow: cardShadow() });
   slide.addShape({ ..., shadow: cardShadow() });
   ```

4. **不要生成空的 PROMPTS.md**
   - 至少要有 3 张图片的提示词
   - 提示词必须是英文（AI 绘图工具效果更好）

5. **不要在深色背景上用浅灰文字**
   - 对比度不足，难以阅读
   - 用白色（#FFFFFF）或浅色（#CAE0F0）

---

## 版本与更新

- **创建日期**：2026-06-12
- **版本**：1.0
- **作者**：MBT
- **技术栈**：Node.js + pptxgenjs

---

**开始使用**：直接告诉我你的 PPT 主题，我会生成完整的脚本和提示词文档！
