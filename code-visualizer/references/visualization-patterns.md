# Visualization Patterns · 可视化代码模式

每个模式都给出：场景、HTML 结构、JS 驱动、常见坑。直接复制改成主题的版本。

**通用原则**

1. **位置变化必须用 `transform`**：`<g transform="translate(...)">` + CSS `transition`，而不是改 `x`/`y`/`cx`/`cy`（那是重排，不会平滑）
2. **SVG 节点用 `<g>` 包**：所有需要动的节点都套一层 `<g class="node">`，`transform` 加在 `<g>` 上，里面的 `<rect>` `<text>` 共同移动
3. **永远不直接 `innerHTML = newHTML` 重绘整个舞台**：那样动画断了。用 `enter / update / exit` 思路，已存在的节点保留，新节点淡入，删除节点淡出
4. **暖色用作"现在正在变"的语义**：默认冷色，正在动的元素加 `.active` `.reading` `.writing` `.done` 之一

---

## 模式 1：数组动画（柱状）

最基础，用于排序、查找、双指针、滑动窗口。

**HTML**

```html
<svg id="stage" viewBox="0 0 800 320" preserveAspectRatio="xMidYMax meet">
  <g id="bars"></g>
  <g id="pointers"></g>
</svg>
```

**JS（创建 / 更新柱）**

```js
const W = 800, H = 320, BAR_GAP = 4;

function renderBars(arr, hints = {}) {
  // hints: { i: 3, j: 5, pivot: 7, sorted: [0,1,2] }
  const stage = document.getElementById('bars');
  const max = Math.max(...arr);
  const barW = (W - BAR_GAP * (arr.length + 1)) / arr.length;

  // enter / update：每个值用唯一 key 跟踪。这里假设元素值是 unique；
  // 如有重复，给 arr 元素拼上原始下标做 key。
  const existing = new Map(
    [...stage.querySelectorAll('.bar')].map(el => [el.dataset.key, el])
  );

  arr.forEach((val, i) => {
    const key = String(val);
    let g = existing.get(key);
    if (!g) {
      g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      g.classList.add('bar');
      g.dataset.key = key;
      g.innerHTML = `
        <rect width="${barW}" height="${(val / max) * (H - 40)}" y="${H - 40 - (val / max) * (H - 40)}" rx="3"/>
        <text x="${barW / 2}" y="${H - 12}" text-anchor="middle">${val}</text>
      `;
      stage.appendChild(g);
    }
    const x = BAR_GAP + i * (barW + BAR_GAP);
    g.setAttribute('transform', `translate(${x}, 0)`);

    // 应用语义类
    g.classList.remove('reading', 'writing', 'pivot', 'done');
    if (i === hints.i || i === hints.j) g.classList.add('reading');
    if (hints.swapping?.includes(i)) g.classList.add('writing');
    if (i === hints.pivot) g.classList.add('pivot');
    if (hints.sorted?.includes(i)) g.classList.add('done');
    existing.delete(key);
  });

  existing.forEach(el => el.remove()); // exit
}
```

**CSS**

```css
.bar { transition: transform var(--t-base) var(--ease); }
.bar rect { fill: var(--accent); transition: fill var(--t-base) var(--ease); }
.bar text { fill: var(--fg-2); font-family: var(--font-mono); font-size: 12px; }
.bar.reading rect { fill: var(--viz-read); }
.bar.writing rect { fill: var(--viz-write); }
.bar.pivot rect   { fill: var(--viz-active); }
.bar.done rect    { fill: var(--viz-done); }
```

**坑**

- ❌ 用数组下标作 key —— 交换时两个柱子会"假交换"（其实是数据互相覆盖），动画就消失了
- ❌ 给 `rect` 直接加 `transform` —— 改 `<g>` 的 transform 才会让 text 一起动
- ❌ 一帧改了 50 个柱子的 transform —— 浏览器一次性合并，看不到中间过程。step 之间用 `setTimeout` 或 `Player` 拆开

---

## 模式 2：栈 / 队列动画

栈用于调用栈、撤销栈、表达式求值；队列用于 BFS、消息队列、Promise 微任务。

**HTML（栈）**

```html
<div class="stack" id="call-stack">
  <!-- 栈帧从底部累积，新 push 从顶部滑入 -->
</div>
```

**JS**

```js
function pushFrame({ fn, args, locals }) {
  const stack = document.getElementById('call-stack');
  const frame = document.createElement('div');
  frame.className = 'frame entering';
  frame.dataset.fn = fn;
  frame.innerHTML = `
    <header>${fn}(${args.join(', ')})</header>
    <ul class="locals">${
      Object.entries(locals).map(([k, v]) => `<li><span>${k}</span>=${v}</li>`).join('')
    }</ul>
  `;
  stack.prepend(frame);
  requestAnimationFrame(() => frame.classList.remove('entering'));
}

function popFrame() {
  const top = document.querySelector('.frame:not(.leaving)');
  if (!top) return;
  top.classList.add('leaving');
  top.addEventListener('transitionend', () => top.remove(), { once: true });
}
```

**CSS**

```css
.stack { display: flex; flex-direction: column; gap: 8px; padding: 16px; }
.frame {
  background: var(--bg-2); border: 1px solid var(--bg-3); border-left: 3px solid var(--accent);
  border-radius: 6px; padding: 8px 12px;
  transition: opacity var(--t-base) var(--ease), transform var(--t-base) var(--ease);
}
.frame.entering, .frame.leaving { opacity: 0; transform: translateY(-12px); }
.frame header { font-family: var(--font-mono); color: var(--fg-0); }
.frame .locals { list-style: none; padding: 4px 0 0; margin: 4px 0 0; border-top: 1px dashed var(--bg-3); font-size: 13px; }
.frame .locals li span { color: var(--accent-hi); }
```

**队列**与栈几乎一样：把 `prepend` 改 `append`，`flex-direction` 改 `row` 即可。

**坑**

- ❌ pop 直接 `el.remove()` —— 没有出场动画。先加 `.leaving`，等 `transitionend` 再 remove
- ❌ 入场动画在 `appendChild` 后立即去 `.entering` —— 浏览器合并两次状态，没动画。必须 `requestAnimationFrame` 后再去掉

---

## 模式 3：树 / 图（SVG）

二叉树、AVL、红黑树、Trie、状态机图、AST。

**布局算法**：简单版用 in-order 遍历分配 x，深度决定 y。复杂场景用 Reingold-Tilford。

```js
function layoutTree(root, gapX = 60, gapY = 80) {
  let x = 0;
  function dfs(node, depth) {
    if (!node) return;
    dfs(node.left, depth + 1);
    node.x = x++ * gapX;
    node.y = depth * gapY;
    dfs(node.right, depth + 1);
  }
  dfs(root, 0);
}
```

**渲染（enter / update / exit）**

```js
function renderTree(root, currentVisitId) {
  const nodesG = document.querySelector('#tree-svg #nodes');
  const edgesG = document.querySelector('#tree-svg #edges');
  const seenN = new Set(), seenE = new Set();

  function visit(node, parent) {
    if (!node) return;
    seenN.add(node.id);

    let g = nodesG.querySelector(`[data-id="${node.id}"]`);
    if (!g) {
      g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      g.classList.add('tree-node');
      g.dataset.id = node.id;
      g.innerHTML = `<circle r="20"/><text dy="5" text-anchor="middle">${node.val}</text>`;
      nodesG.appendChild(g);
    }
    g.setAttribute('transform', `translate(${node.x}, ${node.y})`);
    g.classList.toggle('red', node.color === 'red');
    g.classList.toggle('current', node.id === currentVisitId);

    if (parent) {
      const eid = `${parent.id}-${node.id}`;
      seenE.add(eid);
      let e = edgesG.querySelector(`[data-id="${eid}"]`);
      if (!e) {
        e = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        e.dataset.id = eid;
        e.classList.add('tree-edge');
        edgesG.appendChild(e);
      }
      e.setAttribute('x1', parent.x); e.setAttribute('y1', parent.y);
      e.setAttribute('x2', node.x);   e.setAttribute('y2', node.y);
    }
    visit(node.left, node);
    visit(node.right, node);
  }
  visit(root, null);

  [...nodesG.children].forEach(el => seenN.has(el.dataset.id) || el.remove());
  [...edgesG.children].forEach(el => seenE.has(el.dataset.id) || el.remove());
}
```

**CSS**

```css
.tree-node { transition: transform var(--t-base) var(--ease); }
.tree-node circle {
  fill: var(--bg-2); stroke: var(--accent); stroke-width: 2;
  transition: all var(--t-base) var(--ease);
}
.tree-node.red circle { stroke: var(--viz-error); }
.tree-node.current circle { fill: var(--viz-active); stroke: var(--viz-active); }
.tree-node text { fill: var(--fg-0); font-family: var(--font-mono); font-size: 14px; }
.tree-edge { stroke: var(--bg-3); stroke-width: 2; transition: all var(--t-base) var(--ease); }
.tree-edge.traversed { stroke: var(--viz-active); }
```

**坑**

- ❌ 旋转动画直接 swap 子树指针 —— 用户看不到旋转过程。先 highlight 旋转的边，pause 200ms，**再**做布局更新让节点滑到新位置
- ❌ 重布局把整树 innerHTML 替换 —— 节点重生成，没动画

---

## 模式 4：链表（节点 + 箭头）

单链表、双向链表、环形链表、跳表。

**HTML**

```html
<svg id="ll" viewBox="0 0 800 200">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--accent)"/>
    </marker>
  </defs>
  <g id="ll-nodes"></g>
  <g id="ll-arrows"></g>
</svg>
```

**JS**

```js
function renderList(head) {
  const nodes = []; let cur = head, i = 0;
  while (cur) { nodes.push({ ...cur, x: 60 + i * 130, y: 80 }); i++; cur = cur.next; }

  const ng = document.getElementById('ll-nodes');
  const ag = document.getElementById('ll-arrows');
  const seenN = new Set();

  nodes.forEach((n, i) => {
    seenN.add(n.id);
    let g = ng.querySelector(`[data-id="${n.id}"]`);
    if (!g) {
      g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      g.dataset.id = n.id;
      g.classList.add('ll-node');
      g.innerHTML = `<rect x="-40" y="-25" width="80" height="50" rx="6"/>
                     <line x1="20" y1="-25" x2="20" y2="25"/>
                     <text x="-10" y="5" text-anchor="middle">${n.val}</text>`;
      ng.appendChild(g);
    }
    g.setAttribute('transform', `translate(${n.x}, ${n.y})`);
  });
  [...ng.children].forEach(el => seenN.has(el.dataset.id) || el.remove());

  // 重画 next 箭头
  ag.innerHTML = '';
  for (let i = 0; i < nodes.length - 1; i++) {
    const a = nodes[i], b = nodes[i + 1];
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', a.x + 20); line.setAttribute('y1', a.y);
    line.setAttribute('x2', b.x - 40); line.setAttribute('y2', b.y);
    line.setAttribute('marker-end', 'url(#arrow)');
    line.classList.add('ll-arrow');
    ag.appendChild(line);
  }
}
```

**插入 / 删除动画**：先把要改的箭头标 `.dimmed`，pause 200ms，再实际改链表，让节点平滑移动到新位置。

**坑**

- ❌ 箭头从旧位置直接跳到新位置 —— 应该先变淡（提示"这条链接要变了"），再切换
- ❌ 插入新节点直接出现在最终位置 —— 应该从"调用方"位置滑入

---

## 模式 5：网络包飞行

TCP 握手、HTTP 请求、消息广播、分布式共识。

**HTML**

```html
<svg id="net" viewBox="0 0 800 400">
  <g class="actor" data-id="client" transform="translate(80, 200)">
    <rect x="-60" y="-30" width="120" height="60" rx="6"/>
    <text>Client</text>
  </g>
  <g class="actor" data-id="server" transform="translate(720, 200)">
    <rect x="-60" y="-30" width="120" height="60" rx="6"/>
    <text>Server</text>
  </g>
  <g id="packets"></g>
</svg>
```

**JS**

```js
async function sendPacket({ from, to, label, type, duration = 1200 }) {
  const A = document.querySelector(`.actor[data-id="${from}"]`);
  const B = document.querySelector(`.actor[data-id="${to}"]`);
  const a = A.transform.baseVal[0].matrix, b = B.transform.baseVal[0].matrix;

  const pg = document.getElementById('packets');
  const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  g.classList.add('packet', `packet-${type}`);
  g.innerHTML = `<rect x="-40" y="-14" width="80" height="28" rx="4"/>
                 <text>${label}</text>`;
  g.setAttribute('transform', `translate(${a.e}, ${a.f - 60})`);
  pg.appendChild(g);

  // 强制 reflow，让初始 transform 应用
  g.getBoundingClientRect();

  g.style.transition = `transform ${duration}ms var(--ease)`;
  g.setAttribute('transform', `translate(${b.e}, ${b.f - 60})`);

  await new Promise(r => setTimeout(r, duration));

  // 到达后高亮接收方
  B.classList.add('receiving');
  setTimeout(() => B.classList.remove('receiving'), 300);
  // 包消失（淡出）
  g.style.transition = `opacity 200ms var(--ease)`;
  g.style.opacity = '0';
  setTimeout(() => g.remove(), 200);
}
```

**用法**

```js
async function tcpHandshake() {
  await sendPacket({ from: 'client', to: 'server', label: 'SYN seq=x', type: 'syn' });
  await sendPacket({ from: 'server', to: 'client', label: 'SYN-ACK', type: 'synack' });
  await sendPacket({ from: 'client', to: 'server', label: 'ACK', type: 'ack' });
}
```

**CSS**

```css
.actor rect { fill: var(--bg-2); stroke: var(--accent); stroke-width: 2; }
.actor text { fill: var(--fg-0); text-anchor: middle; dominant-baseline: middle; }
.actor.receiving rect { stroke: var(--viz-active); fill: rgba(251, 191, 36, 0.1); }
.packet rect { fill: var(--bg-1); stroke: var(--accent-hi); stroke-width: 1.5; }
.packet text { fill: var(--fg-0); text-anchor: middle; dominant-baseline: middle; font-size: 11px; font-family: var(--font-mono); }
.packet-syn rect { stroke: var(--viz-read); }
.packet-ack rect { stroke: var(--viz-done); }
.packet-rst rect { stroke: var(--viz-error); }
```

**坑**

- ❌ 用 `setInterval` 改坐标做插值 —— 用 `transition` + 起止两个 transform 让浏览器自己插，更平滑
- ❌ 同一时刻发好几个包，全在同一条 y 上 —— 给每个包一个偏移避免重叠
- ❌ 包到达后一直留在屏幕上 —— 必须淡出，否则越积越多

---

## 模式 6：状态机（节点高亮 + 转移亮起）

TCP 状态、Promise 状态、Vue 编译阶段、AsyncFunction 状态。

**HTML**

```html
<svg id="fsm" viewBox="0 0 800 400">
  <g class="node" data-state="CLOSED" transform="translate(400, 200)">
    <circle r="50"/><text>CLOSED</text>
  </g>
  <g class="node" data-state="LISTEN" transform="translate(200, 100)">...</g>
  <!-- ... 其它节点 -->
  <path class="edge" data-from="CLOSED" data-to="LISTEN" d="M 350 175 Q 280 130 245 110" marker-end="url(#arrow)"/>
  <text class="edge-label" x="280" y="155">passive open</text>
</svg>
```

**JS**

```js
function setState(newState, transition) {
  document.querySelectorAll('.node').forEach(n => n.classList.toggle('active', n.dataset.state === newState));
  if (transition) {
    const edge = document.querySelector(`.edge[data-from="${transition.from}"][data-to="${transition.to}"]`);
    if (edge) {
      edge.classList.add('firing');
      setTimeout(() => edge.classList.remove('firing'), 600);
    }
  }
}
```

**CSS**

```css
.node circle { fill: var(--bg-2); stroke: var(--bg-3); stroke-width: 2; transition: all var(--t-base) var(--ease); }
.node.active circle { fill: var(--viz-active); stroke: var(--viz-active); }
.node text { fill: var(--fg-0); text-anchor: middle; dominant-baseline: middle; font-family: var(--font-mono); font-size: 13px; }
.edge { fill: none; stroke: var(--bg-3); stroke-width: 2; transition: stroke var(--t-base) var(--ease); }
.edge.firing { stroke: var(--viz-active); stroke-dasharray: 6 3; animation: dash 0.6s linear; }
.edge-label { fill: var(--fg-2); font-size: 11px; text-anchor: middle; }
@keyframes dash { from { stroke-dashoffset: 18; } to { stroke-dashoffset: 0; } }
```

**坑**

- ❌ 转移瞬间切状态 —— 用户没看到"边在亮起"。先 `.firing` 600ms，再切 `.active`
- ❌ 节点排版自动算 —— FSM 节点位置应该手工设计，让箭头不交叉

---

## 模式 7：时序图 / 时间轴 swimlane

事件循环、Promise 微/宏任务、TCP 完整生命周期。

**HTML**

```html
<div class="timeline" style="--total-ms: 2000">
  <div class="lane" data-actor="main">
    <span class="lane-label">主线程</span>
    <span class="event" style="--t: 0;    --d: 100;" data-type="exec">script</span>
    <span class="event" style="--t: 100;  --d: 50;"  data-type="micro">P.then</span>
    <span class="event" style="--t: 1000; --d: 80;"  data-type="macro">setTimeout</span>
  </div>
  <div class="lane" data-actor="micro">
    <span class="lane-label">微任务队列</span>
    <span class="event" style="--t: 100; --d: 40;" data-type="enqueue">enq</span>
  </div>
  <input type="range" class="time-cursor" min="0" max="2000" value="0">
</div>
```

**CSS**（用 CSS 变量做位置计算，无需 JS 算坐标）

```css
.timeline { display: grid; gap: 12px; padding: 24px; position: relative; }
.lane { position: relative; height: 48px; background: var(--bg-1); border-radius: 6px; }
.lane-label { position: absolute; left: 8px; top: 50%; transform: translateY(-50%); font-size: 12px; color: var(--fg-2); }
.event {
  position: absolute;
  left: calc(120px + (var(--t) / var(--total-ms)) * (100% - 130px));
  width: calc((var(--d) / var(--total-ms)) * (100% - 130px));
  top: 8px; bottom: 8px;
  background: var(--accent); color: white;
  display: inline-flex; align-items: center; justify-content: center;
  font-size: 11px; border-radius: 3px; padding: 0 4px; overflow: hidden;
}
.event[data-type="micro"] { background: var(--viz-read); }
.event[data-type="macro"] { background: var(--viz-write); }
.event[data-type="enqueue"] { background: var(--viz-ghost); }
.time-cursor { position: absolute; left: 130px; right: 24px; bottom: 0; }
```

**JS**（拖动游标显示快照）

```js
const cursor = document.querySelector('.time-cursor');
cursor.addEventListener('input', e => {
  const t = +e.target.value;
  document.querySelector('.snapshot').textContent = describeStateAt(t);
});
```

**坑**

- ❌ 用 `<canvas>` 画时间轴 —— DOM 更直观，可直接 hover 事件看 tooltip
- ❌ 事件用透明色叠加 —— 同一刻多事件应该错开 swimlane

---

## 模式 8：哈希表（槽位 + 冲突链）

哈希函数演示、开放寻址 vs 链地址、动态 resize。

**HTML**

```html
<div class="hashtable">
  <div class="slots">
    <div class="slot" data-idx="0"><div class="bucket"></div></div>
    <div class="slot" data-idx="1"><div class="bucket"><div class="entry">apple:1</div></div></div>
    <!-- ... -->
  </div>
</div>
```

**JS**

```js
function insert(map, key, val) {
  const idx = hash(key) % map.capacity;
  const slot = document.querySelector(`.slot[data-idx="${idx}"] .bucket`);
  const entry = document.createElement('div');
  entry.className = 'entry entering';
  entry.textContent = `${key}:${val}`;
  slot.appendChild(entry);
  // 高亮 hash 路径
  highlightHashRoute(key, idx);
  requestAnimationFrame(() => entry.classList.remove('entering'));
}
```

**CSS**

```css
.hashtable { display: flex; gap: 24px; padding: 24px; }
.slots { display: grid; gap: 4px; }
.slot { display: flex; align-items: center; gap: 8px; }
.slot::before {
  content: attr(data-idx);
  width: 28px; height: 28px;
  background: var(--bg-2); color: var(--fg-2);
  border-radius: 4px; font-family: var(--font-mono); font-size: 12px;
  display: inline-flex; align-items: center; justify-content: center;
}
.bucket { display: flex; gap: 4px; min-height: 28px; }
.entry {
  background: var(--accent); color: white;
  padding: 4px 8px; border-radius: 4px;
  font-family: var(--font-mono); font-size: 12px;
  transition: opacity var(--t-base), transform var(--t-base);
}
.entry.entering { opacity: 0; transform: scale(0.8); }
.slot.collision::before { background: var(--viz-error); color: white; }
```

**Resize 动画**：扩容时所有 entry 飞回顶部"哈希函数"位置，重新分配。用两阶段 transition 实现。

---

## 模式 9：代码联动高亮（最重要）

每一步动画对应代码的某一行 / 几行高亮。让用户看到"算法跑到哪了"。

**用 `controls.js` 的 Player**：

```js
const code = `
function quicksort(arr, lo, hi) {  // 1
  if (lo < hi) {                    // 2
    const p = partition(arr,lo,hi); // 3
    quicksort(arr, lo, p - 1);      // 4
    quicksort(arr, p + 1, hi);      // 5
  }                                 // 6
}                                   // 7
`.trim();

renderCode('code', code);

const steps = [
  { type: 'enter', range: [0, 8] },
  { type: 'compare', i: 0, j: 7 },
  // ... 每个 step 描述这一步发生什么
];
const codeLines = [1, 2, 3, 3, 4, 4, 5, 5, 6, 7]; // 每个 step 对应高亮哪一行

const player = new Player({
  steps,
  codeLines,
  onStep(step, idx) {
    // 这里根据 step 更新 SVG 舞台
    if (step.type === 'compare') {
      renderBars(currentArr, { i: step.i, j: step.j });
      showAnnotation(`比较 arr[${step.i}] 和 arr[${step.j}]`);
    }
    // ...
  },
});
```

**双向联动（hover 代码行也高亮 SVG）**：

```js
document.querySelectorAll('.code-panel .line').forEach(line => {
  line.addEventListener('mouseenter', () => {
    const lineNum = +line.dataset.line;
    document.querySelectorAll('.bar').forEach(b => b.classList.toggle('preview', isInvolvedAtLine(b, lineNum)));
  });
  line.addEventListener('mouseleave', () => {
    document.querySelectorAll('.bar.preview').forEach(b => b.classList.remove('preview'));
  });
});
```

---

## 通用坑速查

| 症状 | 原因 | 修法 |
|---|---|---|
| 元素直接跳到新位置 | 改的是 attr (x/y/cx) 而非 transform | 用 `<g transform>` 套层，改 `transform` |
| 入场没动画 | 加 class 后立即去 | `requestAnimationFrame` 后再去 |
| 出场没动画 | 直接 `remove()` | 先加 `.leaving`，等 `transitionend` |
| 一帧内多次 transform 合并 | 浏览器 batch 渲染 | 拆成多个 step，间隔 ≥ 16ms |
| 重新渲染后引用断了 | innerHTML 整片替换 | 用 enter/update/exit，已存在节点保留 |
| 移动端布局炸 | SVG / 网格固定 px | viewBox + max-width 100%，重要内容横向滚动而非压缩 |
