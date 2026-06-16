# Examples · 5 个完整主题的页面规划

每个示例展示：可视化设计（Step 1）→ 页面选择（Step 2）→ 关键模式调用。
拿来当模板，按相同思路展开你的主题。

---

## 例 1：快速排序

**目标**：让用户看到 pivot 怎么把数组分两半，递归怎么展开。

### 可视化设计

- **核心变化**：数组中元素位置 + `i` `j` `pivot` 三个指针
- **看不见的状态**：递归调用栈（每层的 `[lo, hi]` 区间 + 返回后的 pivot 位置）
- **能玩什么**：拖拽改输入数组 + 选 pivot 策略（首/末/随机/中位数）+ 调速

### 页面（6 页）

| 页 | 演示什么 | 用的模式 |
|---|---|---|
| `index.html` | hero：乱序 → 有序的 4 帧动画 + 卡片网格 | hero + 模式 1（精简版） |
| `animation.html` | 单步动画：分区过程 + i/j 指针滑动 + 代码联动 | 模式 1 + 模式 9 |
| `internals.html` | 主图分区 + 右侧"递归调用栈"实时显示每层区间 | 模式 1 + 模式 2（栈） |
| `playground.html` | 用户拖拽柱子 / 输入数组 / 选 pivot 策略 | 模式 1 + 输入控件 |
| `compare.html` | 三列：冒泡 / 快排 / 归并 同输入并行跑 | 模式 1 ×3 + 节拍器 |
| `complexity.html` | 实测 n=100 / 1000 / 10000 三种 pivot 策略的 ms 曲线 | 折线图（SVG line） |

### 关键 step 列表（animation 页）

```js
const steps = [
  { type: 'enter', range: [0, 7] },           // 进入 quicksort([0..7])
  { type: 'pickPivot', idx: 7 },              // 选 arr[7] 为 pivot
  { type: 'compare', i: 0, j: 0 },            // 比较 arr[0] 和 pivot
  { type: 'noop' },                            // arr[0] < pivot, i 前进
  { type: 'compare', i: 0, j: 1 },
  { type: 'swap', a: 0, b: 1 },               // 交换
  // ... ~30 步走完一次 partition
  { type: 'placePivot', from: 7, to: 4 },     // 把 pivot 放到正确位置
  { type: 'recurse', range: [0, 3] },         // 左半递归
  { type: 'recurse', range: [5, 7] },         // 右半递归
];
const codeLines = [1, 3, 4, 5, 4, 5, /*...*/, 6, 7, 8];
```

---

## 例 2：TCP 三次握手 + 数据传输

**目标**：理解为什么 3 次握手而不是 2 次，看到 seq/ack 怎么计算。

### 可视化设计

- **核心变化**：客户端和服务器的状态机 + 网络中飞行的包
- **看不见的状态**：seq/ack 号、窗口大小、状态机标签（CLOSED/SYN_SENT/ESTABLISHED）
- **能玩什么**：模拟丢包、调延迟、看重传

### 页面（5 页）

| 页 | 演示什么 | 用的模式 |
|---|---|---|
| `index.html` | hero：3 个包来回飞的 loop 动画 | 模式 5（精简） |
| `animation.html` | 单步播 SYN → SYN-ACK → ACK，包飞 + 状态切 | 模式 5 + 模式 6 |
| `flow.html` | TCP 完整状态机图（11 个状态 + 转移），点节点看说明 | 模式 6 |
| `timeline.html` | 横向时序图：客户端 / 服务器双 swimlane，标 seq/ack | 模式 7 |
| `playground.html` | 用户切丢包率 slider + 看重传 / 超时 | 模式 5 + 控件 |

### 关键 step（animation 页）

```js
const steps = [
  { type: 'state', actor: 'client', state: 'CLOSED' },
  { type: 'state', actor: 'server', state: 'LISTEN' },
  { type: 'send', from: 'client', to: 'server', label: 'SYN seq=100', flags: ['SYN'] },
  { type: 'state', actor: 'client', state: 'SYN_SENT' },
  { type: 'recv', actor: 'server' },
  { type: 'state', actor: 'server', state: 'SYN_RECEIVED' },
  { type: 'send', from: 'server', to: 'client', label: 'SYN-ACK seq=300 ack=101', flags: ['SYN', 'ACK'] },
  // ...
  { type: 'state', actor: 'both', state: 'ESTABLISHED' },
];
```

---

## 例 3：Promise 微任务 vs 宏任务

**目标**：理解 `setTimeout(0)` 为什么慢于 `Promise.resolve().then()`。

### 可视化设计

- **核心变化**：调用栈、微任务队列、宏任务队列三者交替
- **看不见的状态**：当前在哪个队列里、事件循环 tick 的边界
- **能玩什么**：让用户写一段代码，看每行进入哪个队列

### 页面（5 页）

| 页 | 演示什么 | 用的模式 |
|---|---|---|
| `index.html` | hero：三个队列在不同节奏弹出任务 | 模式 2（精简） |
| `animation.html` | 经典代码 `console.log(1); setTimeout(...); Promise.then(...); console.log(2);` 单步演示 | 模式 2 + 模式 9 |
| `internals.html` | 三栏：调用栈 / 微任务队列 / 宏任务队列，事件循环 tick 用脉冲表示 | 模式 2 ×3 |
| `timeline.html` | 横向时间轴，三条 swimlane（call stack / micro / macro），标 tick 边界 | 模式 7 |
| `quiz.html` | 8 道"猜输出顺序"题 | 模式 9 |

---

## 例 4：闭包 / 词法环境

**目标**：让"栈帧弹走但变量还在"这句话变成可看见的画面。

### 可视化设计

- **核心变化**：函数调用 → 栈帧创建 → 函数返回 → 栈帧弹出 → 但被引用的环境对象留在堆里
- **看不见的状态**：栈区 / 堆区分离、引用箭头
- **能玩什么**：用户写闭包代码，看栈和堆同步变化

### 页面（4 页 — 主题精炼，不凑数）

| 页 | 演示什么 | 用的模式 |
|---|---|---|
| `index.html` | hero：栈帧弹出，但堆里的环境对象被外部 fn 引用，不被 GC | 内存模式精简 |
| `memory.html` | 经典 `function makeCounter() { ... return () => count++ }` 单步演示 | 内存模式（栈 + 堆 + 箭头） |
| `playground.html` | 用户在编辑器写代码，每行执行后看栈/堆快照 | 内存模式 + textarea |
| `quiz.html` | 经典闭包陷阱 5 题（for 循环 var vs let、IIFE、共享 vs 独立） | 模式 9 |

---

## 例 5：LRU 缓存

**目标**：理解为什么 LRU 用 HashMap + 双向链表，怎么 O(1) 实现 get/put。

### 可视化设计

- **核心变化**：HashMap 槽位 + 双向链表节点位置（最近用的在头部）
- **看不见的状态**：HashMap 的 key→node 指针、被淘汰节点的瞬间
- **能玩什么**：调容量 + 输入 get/put 序列

### 页面（6 页）

| 页 | 演示什么 | 用的模式 |
|---|---|---|
| `index.html` | hero：节点在链表里被反复"提到最前" + 容量满时淘汰 | 模式 4（精简） |
| `animation.html` | 经典操作序列单步演示：put A,B,C → get A → put D（淘汰 B） | 模式 4 + 模式 8 + 模式 9 |
| `internals.html` | 双面板：左 HashMap 槽位（指向链表节点）+ 右双向链表 | 模式 4 + 模式 8 |
| `playground.html` | 用户调 capacity，输入 `put(k,v) / get(k)` 序列，看动画 | 模式 4 + 输入 |
| `build.html` | 5 步从零写出 LRU：节点结构 → 链表操作 → HashMap → get/put → 淘汰 | 模式 10 |
| `apply.html` | Redis allkeys-lru、Linux page cache、Caffeine（Java）、libcache 的真实代码 | 卡片列表 |

---

## 通用经验

1. **`internals.html` 是真正的杀手页**：把不可见的状态画出来，是用户"啊原来是这样"的瞬间
2. **`animation.html` 的 step 序列要扎实**：宁可 30 步细一点，不要 10 步跳着讲
3. **`playground.html` 必须给 3-5 个预设输入**：给一个空白页用户会干瞪眼
4. **`compare.html` 节拍器要严格同步**：所有列同时跑同一步，差异才一眼看见
5. **`apply.html` 必须有真实链接**：避免凭口说"XX 也用了" —— 要么给源码链接，要么不写

不要为了凑 8 页加无关页。**4 页扎实 &gt; 8 页凑数。**
