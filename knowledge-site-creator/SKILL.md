---
name: knowledge-site-creator
description: 一句话生成任何领域的知识学习网站。AI自动理解主题、创作内容、生成页面、部署上线。适用于任何需要系统学习的知识领域：进化心理学、大模型术语、化学元素、历史事件等。
---

# Knowledge Site Creator - 通用知识学习网站生成器

AI理解主题，自动创作内容，生成网站，一键部署。

## 核心理念

设计系统优先：复用设计语言（极简主义、配色、布局、交互模式），不复用具体页面代码。

通用学习模式：闪卡（Flashcard）、学习（Learn）、测试（Quiz）、索引（Index）、进度（Progress）。

零模板依赖：AI参考设计系统，生成新页面，所有文案由AI创作。

## 触发方式

- "生成一个XXX学习网站"
- "创建XXX知识网站"
- "做个XXX学习工坊"

## 实施流程

### Step 1: 理解主题

AI深入分析主题：这是什么领域？为什么重要？目标受众是谁？如何表达更好？

### Step 2: 生成数据 + 网站配置

#### 2.1 数据文件（wordData.js）

```javascript
const WordRoots = [
  {
    id: 1,
    root: "知识点名称",
    origin: "分类",
    meaning: "一句话解释",
    description: "详细说明（200-300字）",
    examples: [{word, meaning, breakdown: {root}, explanation}],
    quiz: {question, options: string[4], correctAnswer: number}
  }
];
```

#### 2.2 配置文件（siteConfig.js）

```javascript
const siteConfig = {
  topic: "主题",
  siteName: "站点名称",
  itemName: "知识点称呼",
  itemCount: 30,
  hero: {title: ["行1","行2","行3"], subtitle: "...", animation: {enabled:true, demoCount:5}},
  stats: [{value, label}],
  footer: {tagline, description},
  cta: {primary, secondary}
};
```

### Step 3: 生成页面

参考设计规范（配色 #FBBF24、Inter字体、极简主义、圆角卡片），生成：
1. **index.html** - 首页（Hero区 + 动画演示 + 统计 + CTA + Footer）
2. **learn.html** - 学习页（渐进式卡片展示 + 上一个/下一个导航 + 标记已掌握 + 键盘快捷键）
3. **flashcard.html** - 闪卡页（卡片翻转动画 + 键盘快捷键 ← → 空格 M）
4. **roots.html** - 索引页（搜索框 + 筛选器 + 卡片网格布局）
5. **progress.html** - 进度页（统计 + 已掌握列表 + 成就系统）
6. **css/minimal.css** - 统一设计系统 + 响应式布局
7. **js/storage.js** - localStorage 进度管理

所有 HTML 必须包含完整的 SEO meta 标签（Open Graph、Twitter Card）。

代码质量要求：LocalStorage 操作必须有 try-catch、禁止 innerHTML 未转义数据、DOM 操作前检查元素存在。

### Step 4: 项目结构和部署

```bash
mkdir -p js css
# 写入所有文件
```

部署到 Vercel：确保项目独立部署，不共享 GitHub 仓库。
