# Page Catalog · 12 种页面类型

每个 code-visualizer 项目从这 12 种里挑 4-8 页。每条目说明：用途、必备元素、反例、最小骨架。

阅读顺序：先看「★必选」，再按 Step 2 的决策原则补够 4-8 页。

---

## 1. `index.html` — 导览页 ★必选

**用途**：用开场动画 hook 注意力 → 告诉用户主题是什么、能学到什么 → 链接到所有页。

**必备元素**

- 顶部导航条（与其它页一致）
- **一个开场动画**（loop 自动播 / hover 触发）—— 浓缩主题最核心的"动起来"瞬间
  - 排序主题：数组从乱到有序
  - TCP 主题：3 个包来回飞
  - 闭包主题：栈帧弹走、堆对象还在
- 主题名 + 一句话定位（< 20 字）
- 卡片网格：每张卡 = 一个子页面，含小图标 + 1 行说明
- 最末："适合什么人 / 学完能干什么"（≤ 80 字）

**反例**

- ❌ 长篇主题介绍 / 历史背景 / 概念定义
- ❌ 一张静态 banner / 大段教科书定义
- ❌ 卡片只有标题没有视觉提示
- ❌ 把所有概念都堆在首页

**最小骨架**

```html
<nav class="topnav">...</nav>
<section class="hero">
  <svg class="hero-anim" viewBox="0 0 600 200">
    <!-- 持续 loop 的核心动画，例：数组排序的 4-5 帧 -->
  </svg>
  <h1>主题名</h1>
  <p class="tagline">一句话定位（≤20 字）</p>
</section>
<section class="page-grid">
  <a class="page-card" href="animation.html">
    <svg class="card-icon">...</svg>
    <h3>动画演示</h3>
    <p>逐步看主流程</p>
  </a>
  <!-- ... 其它页卡片 -->
</section>
```

**适合主题**：全部

---

## 2. `animation.html` — 核心动画

**用途**：把主流程的每一步用动画展开。能播放、暂停、单步、回放、调速。

**必备元素**

- 主可视化舞台（占主屏幕 60%+）
- 控件栏：`⏮ ⏪ ⏯ ⏩ ⏭ | 速度 slider | 进度条`
- 当前步骤的代码联动高亮（侧边或下方）
- 暂停时弹出当前步骤旁注（≤ 1 行）
- 步数指示：「当前 第 7 步 / 共 23 步」

**反例**

- ❌ 只有"播放"一个按钮（用户错过关键帧就完了）
- ❌ 进度条不能拖（必须从头看）
- ❌ 代码片段在动画下方但跟动画不联动
- ❌ 步骤间用 setTimeout 闪烁切换（不是 transition）

**最小骨架**

```html
<nav class="topnav">...</nav>
<main class="anim-layout">
  <div class="stage">
    <svg id="anim-stage" viewBox="0 0 800 400"><!-- 数组、节点、包等 --></svg>
    <div class="annotation" id="step-note"><!-- 暂停时显示当前步注释 --></div>
  </div>
  <aside class="code-panel">
    <pre><code id="code-display">function quicksort(arr, lo, hi) {
  ...
}</code></pre>
  </aside>
  <div class="controls">
    <button data-act="rewind">⏮</button>
    <button data-act="prev">⏪</button>
    <button data-act="play">▶</button>
    <button data-act="next">⏩</button>
    <button data-act="end">⏭</button>
    <input type="range" min="0.25" max="3" step="0.25" value="1" data-act="speed">
    <span class="step-counter">0 / 23</span>
  </div>
  <input type="range" class="scrubber" min="0" max="22" value="0">
</main>
<script src="js/controls.js"></script>
<script src="js/viz/animation.js"></script>
```

`controls.js` 提供 `Player({steps, render, codeLine})` 类，自动绑定上面所有控件。详见 [assets/controls.js](../assets/controls.js)。

**适合主题**：算法、协议、流程、解析过程

---

## 3. `internals.html` — 内部状态透视

**用途**：把运行时**平时看不见的状态**放出来。这页是 code-visualizer 真正的价值所在。

**必备元素**

- 多窗格布局（典型 2x2）：
  - 左上 / 主图：当前可视化主体（数组、网络、调用栈等）
  - 右上 / 状态面板：透视的不可见状态（`i/j/pivot` 指针 / 调用栈 / 堆对象）
  - 左下 / 代码：联动高亮当前行
  - 右下 / 数据流：变量值变化日志
- hover 状态面板任一元素 → 主图对应位置高亮（双向关联）
- 步进时所有面板同步更新

**透视什么不可见的状态？**

| 主题 | 不可见状态 |
|---|---|
| 排序算法 | i/j/pivot 指针、递归栈、每层区间 [lo, hi] |
| 闭包 | 已弹出的栈帧、堆里活着的环境对象、指向链 |
| Promise | 微任务队列、宏任务队列、当前调用栈 |
| GC | 标记位、根集合、引用图 |
| TCP | seq/ack 号、窗口大小、状态机标签 |
| 哈希表 | 槽位占用率、冲突链、resize 阈值 |

**反例**

- ❌ 状态面板只显示文字（应该也是图形）
- ❌ 状态和主图没联动（hover 不响应、步进不同步）
- ❌ "状态"只是把代码里的变量打印出来（要可视化结构）

**最小骨架**

```html
<main class="grid-2x2">
  <section class="pane main-stage"><svg id="main-svg"></svg></section>
  <section class="pane state-panel">
    <h3>看不见的状态</h3>
    <div class="state-stack" id="call-stack">
      <!-- 每个栈帧一张卡片，新入栈从下方滑入 -->
    </div>
    <div class="state-vars" id="vars">
      <span class="var">i = <b id="var-i">0</b></span>
      <span class="var">j = <b id="var-j">0</b></span>
    </div>
  </section>
  <section class="pane code-panel"><pre><code id="code"></code></pre></section>
  <section class="pane log-panel">
    <h3>变量历史</h3>
    <ul id="log"><!-- 时间倒序 --></ul>
  </section>
</main>
```

**适合主题**：任何有"运行时不可见状态"的主题（几乎都适合）

---

## 4. `playground.html` — 交互 Playground

**用途**：用户改输入 → 实时看输出 / 过程。把"看 demo" 变成"动手玩"。

**必备元素**

- **输入区**：根据主题选择
  - 数组类：可拖拽的元素 / textarea 输入 `[3,1,4,1,5]` / "随机生成"按钮
  - 数字类：slider + 直接输入
  - 字符串类：textarea + 长度上限
  - 选项类：下拉菜单 / 单选按钮
- **运行**按钮（或 `Ctrl+Enter`）+ **重置**按钮
- **输出区**：动画 + 最终结果
- **预设输入**：3-5 组典型用例（"试试这个：已排序数组 / 全相同 / 极大数据"）
- 显示**关键指标**（比较次数 / 交换次数 / 耗时）

**反例**

- ❌ 输入区只有一个 textarea（用户不知道格式）
- ❌ 没有预设（用户瞪着空白发呆）
- ❌ 输出只有最终结果，没有过程动画
- ❌ 改完输入要刷新页面才生效

**最小骨架**

```html
<main class="playground">
  <section class="input-zone">
    <h3>输入</h3>
    <div class="presets">
      <button data-preset="random">随机 10 个</button>
      <button data-preset="sorted">已有序</button>
      <button data-preset="reversed">逆序</button>
      <button data-preset="duplicates">大量重复</button>
    </div>
    <div class="array-editor" id="array-editor"><!-- 可拖拽柱子 --></div>
    <textarea id="input-text" placeholder="或粘贴 [3,1,4,1,5]"></textarea>
    <button class="primary" id="run">▶ 运行</button>
  </section>
  <section class="output-zone">
    <svg id="output-stage"></svg>
    <div class="metrics">
      <div>比较 <b id="m-cmp">0</b></div>
      <div>交换 <b id="m-swap">0</b></div>
      <div>耗时 <b id="m-time">0</b> ms</div>
    </div>
  </section>
</main>
```

**适合主题**：算法、纯函数、API、数据结构

---

## 5. `compare.html` — 对比 / 变体

**用途**：多变体并排，同输入下表现差异一目了然。

**必备元素**

- 横向多列布局（2-4 列），每列一个变体
- **统一节拍器**：所有列同步播放 / 暂停 / 单步
- **共用输入**：上方一个输入区控制所有列
- **指标对比**：每列底部计数器（比较 / 交换 / 时间）
- **赢家高亮**：跑完后步数最少 / 时间最短的列加金边

**反例**

- ❌ 各列用各自的播放按钮（无法比较节奏）
- ❌ 各列输入不同（不公平比较）
- ❌ 跑完没有"谁赢了"的总结

**最小骨架**

```html
<main class="compare">
  <header class="shared-input">
    <textarea id="shared-array">[5,3,8,1,9,2,7,4,6]</textarea>
    <button id="run-all">▶ 全部运行</button>
  </header>
  <section class="lanes">
    <div class="lane" data-algo="bubble">
      <h3>冒泡</h3>
      <svg></svg>
      <div class="metrics">cmp <b>0</b> · swap <b>0</b> · <b>0</b>ms</div>
    </div>
    <div class="lane" data-algo="quick">...</div>
    <div class="lane" data-algo="merge">...</div>
  </section>
</main>
```

**适合主题**：多种实现可选时（排序、查找、缓存淘汰、调度）

---

## 6. `timeline.html` — 时序图

**用途**：在时间轴上标记事件，多 swimlane 看不同主体的并发行为。

**必备元素**

- 横向时间轴（带刻度，单位：ms / step / tick）
- **多条 swimlane**（横排），每条代表一个主体（客户端 / 服务器 / 主线程 / 微任务队列）
- 事件用色块标记（含 hover 详情）
- **拖动时间游标**看每个时刻的"快照状态"
- 关键事件用箭头连接（如 TCP 包从 A → B）

**反例**

- ❌ 只有时间线没有 swimlane（看不出主体）
- ❌ 事件用 emoji 代替色块
- ❌ 不能拖游标（只能看终态）

**最小骨架**

```html
<main class="timeline">
  <div class="lanes">
    <div class="lane" data-actor="client">
      <span class="lane-label">Client</span>
      <div class="events">
        <span class="event" style="left: 10%" data-t="100" data-type="SYN">SYN</span>
        <span class="event" style="left: 35%" data-t="300" data-type="ACK">ACK</span>
      </div>
    </div>
    <div class="lane" data-actor="server">
      <span class="lane-label">Server</span>
      <div class="events">...</div>
    </div>
  </div>
  <svg class="arrows"><!-- 跨 lane 箭头：SYN → SYN-ACK 等 --></svg>
  <div class="time-axis"><!-- 刻度 --></div>
  <input type="range" class="cursor" min="0" max="1000" value="0">
  <aside class="snapshot"><!-- 当前游标位置的状态快照 --></aside>
</main>
```

**适合主题**：网络协议、并发、事件循环、Promise/async、生命周期

---

## 7. `complexity.html` — 复杂度曲线

**用途**：实测不同 n 下的运行时间，画出真实曲线（不是教科书 O(n²) 的抽象图）。

**必备元素**

- 折线图（SVG 或 Canvas）：x = 输入规模 n，y = 时间 ms / 操作次数
- 多算法叠加（不同颜色）
- 用户能调 n 上限 slider
- "重跑"按钮（多次跑取平均，减少抖动）
- 旁边附理论曲线对比（虚线）

**反例**

- ❌ 只画教科书理论曲线（没真实测量就没说服力）
- ❌ 单次跑（噪声大）
- ❌ y 轴线性，让 O(n) 和 O(n²) 看起来差不多（应该提供线性 / 对数切换）

**最小骨架**

```html
<main class="complexity">
  <aside class="controls">
    <label>n 上限：<input type="range" id="n-max" min="100" max="10000" step="100" value="1000"></label>
    <label>采样次数：<input type="number" id="trials" value="5"></label>
    <fieldset>
      <legend>算法</legend>
      <label><input type="checkbox" checked data-algo="bubble">冒泡 O(n²)</label>
      <label><input type="checkbox" checked data-algo="quick">快排 O(n log n)</label>
    </fieldset>
    <button id="run">重跑</button>
    <label><input type="radio" name="scale" value="linear" checked>线性</label>
    <label><input type="radio" name="scale" value="log">对数</label>
  </aside>
  <svg id="chart" viewBox="0 0 800 500"><!-- 坐标系 + 折线 --></svg>
  <div class="legend"></div>
</main>
```

**适合主题**：算法、数据结构操作复杂度、缓存命中率

---

## 8. `memory.html` — 内存布局

**用途**：把栈区 / 堆区画出来，箭头表示引用，单步执行代码看分配 / 释放。

**必备元素**

- 左侧"栈区"（grow up 或 grow down 看实际语言习惯）
- 右侧"堆区"（自由布局的对象卡）
- **箭头连接**栈中的引用 → 堆中对象
- 单步执行按钮（每步对应一行代码）
- 颜色区分：基本类型（蓝）/ 引用（紫）/ 已释放（灰带斜线）
- 引用计数 / 标记位（GC 主题）

**反例**

- ❌ 栈和堆放一起没有边界（看不出区别）
- ❌ 箭头不会动（应该新引用建立时有"画箭头"动画）
- ❌ 释放只是消失（应该有 fade-out + 灰化阶段）

**最小骨架**

```html
<main class="memory">
  <section class="stack-zone">
    <h3>Stack</h3>
    <div class="frame" data-fn="main">
      <header>main()</header>
      <div class="local"><span class="name">x</span><span class="val">42</span></div>
      <div class="local"><span class="name">obj</span><span class="ref" data-points-to="h1">→</span></div>
    </div>
    <!-- 调用栈：新 frame 从顶部滑入 -->
  </section>
  <section class="heap-zone">
    <h3>Heap</h3>
    <div class="object" id="h1" data-refs="2">
      <span class="rc">RC: 2</span>
      <pre>{ name: "Alice", age: 30 }</pre>
    </div>
  </section>
  <svg class="arrows"><!-- ref 箭头 --></svg>
  <aside class="step-controls">
    <button data-act="prev">⏪</button>
    <button data-act="next">⏩</button>
    <pre class="code"><code></code></pre>
  </aside>
</main>
```

**适合主题**：闭包、引用 vs 值、GC、内存泄漏、智能指针、unique_ptr / shared_ptr

---

## 9. `flow.html` — 数据流 / 状态机

**用途**：节点 + 有向边的图。数据沿边流动，或当前状态在节点间跳转。

**必备元素**

- 节点（圆 / 矩形 / 卡片）+ 有向边（带箭头）
- 数据流模式：粒子沿边流动（dasharray + animation 实现）
- 状态机模式：当前状态节点高亮，转移时边亮起
- 触发条件标在边上（如 "SYN_RECEIVED → ESTABLISHED on ACK"）
- 历史路径用淡色显示

**反例**

- ❌ 只是静态流程图（不流动 / 不切换 = 没必要可视化）
- ❌ 边没有方向箭头
- ❌ 状态机切换瞬间跳转（没动画）

**最小骨架**

```html
<main class="flow">
  <svg id="graph" viewBox="0 0 800 500">
    <defs>
      <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/>
      </marker>
    </defs>
    <!-- 状态节点 -->
    <g class="node active" id="state-CLOSED" transform="translate(100,250)">
      <circle r="40"/><text>CLOSED</text>
    </g>
    <g class="node" id="state-SYN_SENT" transform="translate(300,150)">...</g>
    <!-- 边 -->
    <path class="edge" d="M 140 250 Q 220 200 260 150" marker-end="url(#arrow)"/>
    <text class="edge-label" x="200" y="195">send SYN</text>
  </svg>
  <aside class="event-log">
    <h3>事件日志</h3>
    <ul></ul>
  </aside>
  <div class="controls">
    <button data-event="open">主动打开</button>
    <button data-event="receive-syn">收到 SYN</button>
    <!-- ... -->
  </div>
</main>
```

**适合主题**：网络协议状态机、Promise 状态、Redux 单向数据流、编译器 pipeline、事件流

---

## 10. `build.html` — 从零构建

**用途**：用户从空白开始，一步步加代码，实时看每一步的运行结果。

**必备元素**

- 顶部代码编辑器（增量解锁：完成 step N 才解锁 step N+1）
- 下方实时运行 / 可视化结果区
- 步骤导航："Step 1: 创建空对象 → Step 2: 加 get 方法 → ..."
- 每步有"作弊：直接看答案"按钮
- 每步有"为什么这样写"折叠说明（默认收起）

**反例**

- ❌ 直接给完整代码（失去推导价值）
- ❌ 步骤之间不能跳来跳去
- ❌ 步骤变化时编辑器内容直接替换（应该 diff 高亮新增 / 修改）

**最小骨架**

```html
<main class="build">
  <aside class="step-nav">
    <ol>
      <li class="active">Step 1: 创建结构</li>
      <li>Step 2: 实现 get</li>
      <li>Step 3: 实现 put 与淘汰</li>
    </ol>
  </aside>
  <section class="editor-zone">
    <textarea id="editor" spellcheck="false"></textarea>
    <button id="run">▶ 运行</button>
    <button id="reveal">看答案</button>
    <details><summary>为什么这样写？</summary><p>因为...</p></details>
  </section>
  <section class="output-zone">
    <svg id="viz"></svg>
    <pre id="console"></pre>
  </section>
</main>
```

**适合主题**：设计模式、原理推导（手写 Promise / 手写 LRU / 手写 Vue 响应式）

---

## 11. `quiz.html` — 输入预测

**用途**：给定输入 + 代码，让用户预测输出。答完用动画展示正确执行过程。

**必备元素**

- 题面：代码片段 + 输入
- 选择题（多选项）或填空题
- 提交后显示对错 + **动画演示**正确过程（不只是给答案）
- 题目库 5-10 道，难度递增
- 进度指示「3 / 10」

**反例**

- ❌ 答完只显示文字答案（应该跳到动画）
- ❌ 全对 / 全错没分级反馈
- ❌ 题目重复 / 不够代表

**最小骨架**

```html
<main class="quiz">
  <header class="progress">第 <b>3</b> / 10 题 · <span class="streak">连对 2 题 🔥</span></header>
  <pre class="question-code"><code>const arr = [3,1,4];
arr.sort();
console.log(arr);</code></pre>
  <p class="prompt">输出会是什么？</p>
  <div class="options">
    <button data-correct="false">[3, 1, 4]</button>
    <button data-correct="true">[1, 3, 4]</button>
    <button data-correct="false">[4, 3, 1]</button>
    <button data-correct="false">undefined</button>
  </div>
  <section class="explanation hidden">
    <svg id="explain-anim"></svg>
    <button id="next">下一题 →</button>
  </section>
</main>
```

**适合主题**：任何确定行为的主题（最适合：JS 怪异行为、运算符优先级、闭包陷阱）

---

## 12. `apply.html` — 真实应用

**用途**：列举哪些库 / 系统 / 框架在用这个原理，附真实代码片段（不是教科书举例）。

**必备元素**

- 卡片列表：每张卡 = 一个真实项目
  - 项目名 + logo / 图标
  - 在哪一部分用到（"V8 在 sort 实现里使用 ..."）
  - **真实代码片段**（注明源文件 + 行号 + 链接）
  - 用了什么变体 / 优化
- 顶部"为什么这个原理重要"一句话
- 底部"延伸阅读"链接（论文 / 博客）

**反例**

- ❌ 只列项目名没有代码（凭口说）
- ❌ 代码是简化版（看不到真实工程考量）
- ❌ "ChatGPT 也用了"（没有验证的虚构）—— 只放有源链接的

**最小骨架**

```html
<main class="apply">
  <header>
    <h1>真实世界中的快速排序</h1>
    <p class="lead">虽然教科书简单，但生产实现都做了大量优化。</p>
  </header>
  <section class="case-grid">
    <article class="case">
      <header>
        <h3>V8 引擎（Chrome / Node.js）</h3>
        <span class="badge">ECMAScript Array.prototype.sort</span>
      </header>
      <p>使用 TimSort（混合插入 + 归并），不是教科书快排。短数组退化为插入排序。</p>
      <pre><code class="lang-cpp">// src/builtins/array-sort.tq:1234
macro Quicksort(...) { ... }</code></pre>
      <a href="https://github.com/v8/v8/blob/main/...">查看源码</a>
    </article>
    <!-- 更多 case -->
  </section>
</main>
```

**适合主题**：全部（首选用作 4-8 页中的最后一页 / 收尾页）

---

## 选页决策回顾

- **4 页（必备）**：`index.html` + `animation.html` + `internals.html` + `playground.html`
- **+1 / +2 页**：从 `compare` `timeline` `complexity` 中选最契合主题的
- **再补**：`memory` `flow` `build` `quiz` 之一，按主题需要
- **收尾页**：`apply.html`（如果有真实案例值得讲）

不要为了凑 8 页而硬塞 —— 4 页做扎实 &gt; 8 页凑数。


---

---

---
