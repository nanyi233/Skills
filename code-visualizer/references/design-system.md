# Design System · 设计令牌与组件样式

所有 code-visualizer 项目共享同一套设计系统，用户跨主题学习时不会被风格差异分散注意力。

---

## 颜色系统

**基本原则：暗色主题 + 冷色 UI + 暖色动画语义**

冷色（蓝紫）留给静态 UI（导航、按钮、卡片边框）；暖色（黄红粉）留给"正在动"的元素（当前指针、正在交换的元素），让动画在画面上自然吸睛。

```css
:root {
  /* 背景层级 */
  --bg-0: #0B0F19;        /* 最底层 */
  --bg-1: #111827;        /* 卡片 / pane */
  --bg-2: #1F2937;        /* 输入框 / hover */
  --bg-3: #374151;        /* 边框 */

  /* 文字层级 */
  --fg-0: #F9FAFB;        /* 主文字 */
  --fg-1: #E5E7EB;        /* 正文 */
  --fg-2: #9CA3AF;        /* 次要 */
  --fg-3: #6B7280;        /* 禁用 / 辅助 */

  /* UI 强调色（冷色系） */
  --accent: #818CF8;      /* 主强调（按钮、链接、当前页） */
  --accent-hi: #A5B4FC;   /* hover */
  --accent-dim: #4F46E5;  /* 按下 / 深色背景上 */

  /* 动画语义色（暖色系，保留给"正在动"的元素） */
  --viz-active: #FBBF24;  /* 当前指针 / 正在处理 */
  --viz-read:   #22D3EE;  /* 读 / 比较 */
  --viz-write:  #EC4899;  /* 写 / 交换 */
  --viz-done:   #10B981;  /* 完成 / 已排序 */
  --viz-error:  #EF4444;  /* 错误 / 无效 */
  --viz-ghost:  rgba(156, 163, 175, 0.3); /* 历史路径 / 灰化 */

  /* 代码高亮 */
  --code-bg:    #0F172A;
  --code-line:  rgba(129, 140, 248, 0.15); /* 当前行高亮 */
  --code-kw:    #C084FC;  /* 关键字 */
  --code-fn:    #60A5FA;  /* 函数名 */
  --code-str:   #34D399;  /* 字符串 */
  --code-num:   #FBBF24;  /* 数字 */
  --code-cmt:   #6B7280;  /* 注释 */
}
```

**动画色用法守则**：

- 静态状态用冷色或灰色
- 当某个元素**正在被处理**时，加上暖色之一
- 一帧画面里不要超过 3 种暖色同时出现（眼花）
- 动画结束后，暖色应过渡回冷色 / 灰色

---

## 字体

```css
:root {
  --font-sans: ui-sans-serif, -apple-system, "Segoe UI", "PingFang SC", "Hiragino Sans GB", sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, "Cascadia Code", Menlo, Consolas, monospace;
}

body { font-family: var(--font-sans); }
code, pre, .mono { font-family: var(--font-mono); }
```

**字号比例（perfect fourth, 1.333）**：

```css
:root {
  --text-xs:   12px;
  --text-sm:   14px;
  --text-base: 16px;
  --text-lg:   19px;
  --text-xl:   25px;
  --text-2xl:  33px;
  --text-3xl:  44px;  /* hero 标题 */
}
```

代码片段用 `--text-sm` 或 `--text-base`，不要用 12px（移动端看不清）。

---

## 间距

4px 基底，避免奇数值。

```css
:root {
  --sp-1: 4px;
  --sp-2: 8px;
  --sp-3: 12px;
  --sp-4: 16px;
  --sp-5: 24px;
  --sp-6: 32px;
  --sp-7: 48px;
  --sp-8: 64px;
}
```

**布局间距**：组件内部用 `--sp-2/3/4`，卡片之间用 `--sp-5/6`，section 之间用 `--sp-7/8`。

---

## 动画时长与缓动

```css
:root {
  --t-fast:   150ms;  /* 状态反馈：hover / click */
  --t-base:   300ms;  /* 元素移动 / 切换 */
  --t-slow:   600ms;  /* 大幅度过渡 / 强调 */
  --t-step:  1000ms;  /* 单步动画的默认时长（可被 speed slider 改） */

  --ease:        cubic-bezier(0.4, 0, 0.2, 1);     /* 标准过渡 */
  --ease-out:    cubic-bezier(0, 0, 0.2, 1);       /* 入场（淡入、滑入） */
  --ease-in:     cubic-bezier(0.4, 0, 1, 1);       /* 出场 */
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1); /* 满足感的小弹跳 */
}
```

**动画总原则**：

- 元素位置变化必用 `transform: translate()` + `transition`，**绝不**用 `left/top` 直接改坐标（不会触发硬件加速，且会重排）
- 入场用 `--ease-out` + opacity 0→1
- 出场用 `--ease-in` + opacity 1→0
- 强调（如交换完成）用 `--ease-spring` 加一点弹跳
- 单步动画时长统一从 `--t-step` 派生，方便 speed slider 全局缩放

---

## 组件样式

### 顶部导航

```html
<nav class="topnav">
  <a class="brand" href="index.html">⟢ 主题名</a>
  <a href="animation.html">动画</a>
  <a href="internals.html" class="active">内部状态</a>
  <a href="playground.html">Playground</a>
  <a href="apply.html">真实应用</a>
</nav>
```

```css
.topnav {
  display: flex; align-items: center; gap: var(--sp-4);
  padding: var(--sp-3) var(--sp-5);
  background: var(--bg-1);
  border-bottom: 1px solid var(--bg-3);
  position: sticky; top: 0; z-index: 100;
  backdrop-filter: blur(8px);
}
.topnav .brand { font-weight: 600; margin-right: auto; color: var(--fg-0); }
.topnav a { color: var(--fg-2); text-decoration: none; padding: var(--sp-1) var(--sp-2); border-radius: 6px; }
.topnav a:hover { color: var(--fg-0); background: var(--bg-2); }
.topnav a.active { color: var(--accent-hi); background: rgba(129, 140, 248, 0.1); }
```

### 按钮

```css
button {
  font-family: inherit; font-size: var(--text-sm);
  padding: var(--sp-2) var(--sp-4);
  background: var(--bg-2); color: var(--fg-1);
  border: 1px solid var(--bg-3); border-radius: 6px;
  cursor: pointer; transition: all var(--t-fast) var(--ease);
}
button:hover { background: var(--bg-3); color: var(--fg-0); }
button.primary { background: var(--accent-dim); color: white; border-color: var(--accent); }
button.primary:hover { background: var(--accent); }
button:disabled { opacity: 0.4; cursor: not-allowed; }
button.icon { padding: var(--sp-2); width: 36px; height: 36px; display: inline-flex; align-items: center; justify-content: center; }
```

### 卡片 / pane

```css
.pane, .card {
  background: var(--bg-1);
  border: 1px solid var(--bg-3);
  border-radius: 12px;
  padding: var(--sp-5);
}
.pane > h3, .card > h3 {
  margin: 0 0 var(--sp-4); font-size: var(--text-sm);
  color: var(--fg-2); text-transform: uppercase; letter-spacing: 0.08em;
}
```

### 控件栏（播放器）

```html
<div class="controls">
  <button class="icon" data-act="rewind" title="重置">⏮</button>
  <button class="icon" data-act="prev" title="上一步">⏪</button>
  <button class="icon primary" data-act="play" title="播放/暂停">▶</button>
  <button class="icon" data-act="next" title="下一步">⏩</button>
  <button class="icon" data-act="end" title="跳到结尾">⏭</button>
  <span class="step-counter">0 / 23</span>
  <label>
    速度
    <input type="range" min="0.25" max="3" step="0.25" value="1" data-act="speed">
    <span class="speed-readout">1x</span>
  </label>
</div>
<input type="range" class="scrubber" min="0" max="22" value="0">
```

```css
.controls {
  display: flex; align-items: center; gap: var(--sp-3);
  padding: var(--sp-3) var(--sp-4);
  background: var(--bg-1); border-radius: 8px;
}
.controls label { display: inline-flex; align-items: center; gap: var(--sp-2); color: var(--fg-2); font-size: var(--text-sm); }
.step-counter { color: var(--fg-2); font-family: var(--font-mono); font-size: var(--text-sm); margin-left: auto; }
.scrubber { width: 100%; }
input[type="range"] { accent-color: var(--accent); }
```

### 代码面板（带行高亮）

```html
<pre class="code-panel"><code id="code">
<span class="line" data-line="1">function quicksort(arr, lo, hi) {</span>
<span class="line" data-line="2">  if (lo &lt; hi) {</span>
<span class="line current" data-line="3">    const p = partition(arr, lo, hi);</span>
<span class="line" data-line="4">    quicksort(arr, lo, p - 1);</span>
<span class="line" data-line="5">    quicksort(arr, p + 1, hi);</span>
<span class="line" data-line="6">  }</span>
<span class="line" data-line="7">}</span>
</code></pre>
```

```css
.code-panel {
  background: var(--code-bg); padding: var(--sp-4); border-radius: 8px;
  font-family: var(--font-mono); font-size: var(--text-sm);
  line-height: 1.6; overflow-x: auto;
}
.code-panel .line {
  display: block; padding: 0 var(--sp-3); margin: 0 calc(-1 * var(--sp-3));
  border-left: 3px solid transparent;
  transition: all var(--t-base) var(--ease);
}
.code-panel .line.current {
  background: var(--code-line);
  border-left-color: var(--viz-active);
}
/* token coloring (用 viz/highlight.js 给 .line 套 span) */
.tok-kw { color: var(--code-kw); }
.tok-fn { color: var(--code-fn); }
.tok-str { color: var(--code-str); }
.tok-num { color: var(--code-num); }
.tok-cmt { color: var(--code-cmt); font-style: italic; }
```

### 注释 / 旁注气泡

```html
<div class="annotation" data-show="true">
  pivot 已固定，左侧都比它小，右侧都比它大
</div>
```

```css
.annotation {
  background: var(--bg-2); color: var(--fg-1);
  padding: var(--sp-3) var(--sp-4);
  border-left: 3px solid var(--viz-active);
  border-radius: 4px;
  font-size: var(--text-sm);
  opacity: 0; transform: translateY(-4px);
  transition: all var(--t-base) var(--ease-out);
}
.annotation[data-show="true"] { opacity: 1; transform: translateY(0); }
```

### 度量徽标

```html
<div class="metric"><span class="label">比较</span><b>23</b></div>
```

```css
.metric {
  display: inline-flex; align-items: baseline; gap: var(--sp-2);
  font-family: var(--font-mono);
}
.metric .label { color: var(--fg-2); font-size: var(--text-xs); }
.metric b { color: var(--fg-0); font-size: var(--text-lg); font-weight: 600;
  font-variant-numeric: tabular-nums; transition: color var(--t-fast) var(--ease); }
.metric b.flash { color: var(--viz-active); } /* JS: 数字变化时短暂 flash */
```

---

## 布局模式

### Stage（占满主屏的可视化舞台）

```css
main.stage {
  display: grid;
  grid-template-rows: 1fr auto auto;  /* 舞台 / 控件 / scrubber */
  height: calc(100vh - 56px);          /* 减去顶部 nav */
  gap: var(--sp-3);
  padding: var(--sp-4);
}
main.stage svg { width: 100%; height: 100%; }
```

### 双栏：动画 + 代码

```css
.anim-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  grid-template-rows: 1fr auto auto;
  grid-template-areas:
    "stage code"
    "controls controls"
    "scrubber scrubber";
  gap: var(--sp-3); padding: var(--sp-4);
  height: calc(100vh - 56px);
}
.anim-layout .stage { grid-area: stage; }
.anim-layout .code-panel { grid-area: code; }
.anim-layout .controls { grid-area: controls; }
.anim-layout .scrubber { grid-area: scrubber; }
```

### 2x2 网格（internals 页常用）

```css
.grid-2x2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: var(--sp-4);
  padding: var(--sp-4);
  height: calc(100vh - 56px);
}
.grid-2x2 .pane { display: flex; flex-direction: column; min-height: 0; }
.grid-2x2 .pane > svg, .grid-2x2 .pane > .scrollable { flex: 1; min-height: 0; }
```

### 卡片网格（首页 / apply 页）

```css
.page-grid, .case-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--sp-5);
  padding: var(--sp-6);
}
```

---

## 响应式 / 移动端

视口 < 720px 时：

- 顶部 nav 折叠成横向滚动，不要做汉堡菜单（这是工具页，不是文档）
- 双栏布局降级为单栏（代码面板移到动画下方，最高 40vh）
- 2x2 网格降级为 2 个单栏
- 控件栏的"速度 slider"可以隐藏，只留按钮
- 重要：**不要等比缩放 SVG 把所有东西挤成一团** —— 让 SVG 横向滚动比变形好

```css
@media (max-width: 720px) {
  .anim-layout { grid-template-columns: 1fr; grid-template-areas: "stage" "code" "controls" "scrubber"; }
  .grid-2x2 { grid-template-columns: 1fr; grid-template-rows: auto; height: auto; }
  .topnav { overflow-x: auto; white-space: nowrap; }
  .controls label { display: none; } /* 隐藏速度 slider */
}
```

---

## 不许做的事

- ❌ 引入 Tailwind / Bootstrap / 任何 CSS 框架
- ❌ 用 `!important`（除非 reset 系统样式）
- ❌ 用 `*` 全局选择器加样式（性能差）
- ❌ 内联 style（除了动画过程中用 JS 改的位置 / opacity）
- ❌ 在按钮 / 链接上加 `outline: none` 而不替代 focus 样式（无障碍灾难）
- ❌ 用 `<font>` `<center>` 等过时标签（连开玩笑都不行）

---

## 复制到项目

整个设计系统已经实现成 [`assets/base.css`](../assets/base.css)，**直接复制到项目的 `css/base.css` 就能用**。每个页面 HTML 顶部：

```html
<link rel="stylesheet" href="css/base.css">
```


