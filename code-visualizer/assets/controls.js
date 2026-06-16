/* code-visualizer · controls.js
 * 通用 step-by-step 动画播放器 + 代码高亮工具。
 *
 * 用法：
 *   const player = new Player({
 *     steps: [...],                       // 任意形状的步骤数组
 *     onStep: (step, idx, prev) => {...}, // 进入每一步时调用，由你更新 SVG/DOM
 *     codeLines: [1, 2, 3, 5, 5, 6, ...], // 可选：每步对应的代码行号
 *     stepDuration: 800                   // 自动播放时每步毫秒数（会被 speed slider 缩放）
 *   });
 *
 * HTML 控件约定（base.css 已样式化）：
 *   <button data-act="rewind|prev|play|next|end">
 *   <input  data-act="speed" type="range">
 *   <input  class="scrubber" type="range">
 *   <span   class="step-counter">
 *   <span   class="speed-readout">
 */

class Player {
  constructor({ steps, onStep, codeLines = [], stepDuration = 800, root = document }) {
    this.steps = steps;
    this.onStep = onStep;
    this.codeLines = codeLines;
    this.stepDuration = stepDuration;
    this.root = root;
    this.idx = 0;
    this.playing = false;
    this.speed = 1;
    this.timer = null;
    this._bind();
    this._goto(0, /*emit*/ true);
  }

  _bind() {
    const $ = sel => this.root.querySelector(sel);
    $('[data-act="play"]')?.addEventListener('click', () => this.toggle());
    $('[data-act="prev"]')?.addEventListener('click', () => this.prev());
    $('[data-act="next"]')?.addEventListener('click', () => this.next());
    $('[data-act="rewind"]')?.addEventListener('click', () => this.rewind());
    $('[data-act="end"]')?.addEventListener('click', () => this._goto(this.steps.length - 1, true));

    const scrubber = $('.scrubber');
    if (scrubber) {
      scrubber.min = 0;
      scrubber.max = this.steps.length - 1;
      scrubber.addEventListener('input', e => {
        this.pause();
        this._goto(+e.target.value, true);
      });
    }

    const speedInput = $('[data-act="speed"]');
    if (speedInput) {
      speedInput.addEventListener('input', e => {
        this.speed = +e.target.value;
        const out = $('.speed-readout');
        if (out) out.textContent = `${this.speed}x`;
      });
    }

    document.addEventListener('keydown', e => {
      if (e.target.matches('input, textarea, select')) return;
      if (e.key === ' ') { e.preventDefault(); this.toggle(); }
      else if (e.key === 'ArrowLeft') this.prev();
      else if (e.key === 'ArrowRight') this.next();
      else if (e.key === 'Home') this.rewind();
      else if (e.key === 'End') this._goto(this.steps.length - 1, true);
    });
  }

  _goto(idx, emit) {
    idx = Math.max(0, Math.min(this.steps.length - 1, idx));
    const prev = this.idx;
    this.idx = idx;
    this._render();
    if (emit) this.onStep?.(this.steps[idx], idx, this.steps[prev]);
  }

  next() {
    if (this.idx >= this.steps.length - 1) { this.pause(); return; }
    this._goto(this.idx + 1, true);
  }
  prev() {
    if (this.idx <= 0) return;
    this._goto(this.idx - 1, true);
  }
  rewind() { this.pause(); this._goto(0, true); }

  toggle() { this.playing ? this.pause() : this.play(); }

  play() {
    if (this.idx >= this.steps.length - 1) {
      this._goto(0, true);
    }
    this.playing = true;
    this._render();
    this._tick();
  }

  pause() {
    this.playing = false;
    clearTimeout(this.timer);
    this._render();
  }

  _tick() {
    if (!this.playing) return;
    if (this.idx >= this.steps.length - 1) {
      this.pause();
      return;
    }
    this._goto(this.idx + 1, true);
    this.timer = setTimeout(() => this._tick(), this.stepDuration / this.speed);
  }

  _render() {
    const $ = sel => this.root.querySelector(sel);
    const playBtn = $('[data-act="play"]');
    if (playBtn) playBtn.textContent = this.playing ? '❚❚' : '▶';
    const counter = $('.step-counter');
    if (counter) counter.textContent = `${this.idx + 1} / ${this.steps.length}`;
    const scrubber = $('.scrubber');
    if (scrubber && +scrubber.value !== this.idx) scrubber.value = this.idx;
    const prevBtn = $('[data-act="prev"]');
    if (prevBtn) prevBtn.disabled = this.idx === 0;
    const nextBtn = $('[data-act="next"]');
    if (nextBtn) nextBtn.disabled = this.idx === this.steps.length - 1;

    const lineNum = this.codeLines[this.idx];
    if (lineNum !== undefined) {
      this.root.querySelectorAll('.code-panel .line.current').forEach(el => el.classList.remove('current'));
      const line = this.root.querySelector(`.code-panel .line[data-line="${lineNum}"]`);
      if (line) {
        line.classList.add('current');
        line.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      }
    }
  }
}

/* ============ 代码渲染 ============ */
/* renderCode(elementId, sourceCode) — 把代码 split 成 .line spans 并加 token 高亮。
 * 例：renderCode('code', `function quicksort(arr) { ... }`);
 *
 * highlightCode 是给 JS / TypeScript / Java 类语法的简易着色，覆盖 80% 主题需求。
 * 如果主题用 Python / Rust，自己改 KW 列表即可。
 */
function escapeHtml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

const _KW = /\b(function|const|let|var|return|if|else|for|while|do|break|continue|switch|case|class|new|this|null|undefined|true|false|async|await|yield|throw|try|catch|finally|import|export|default|from|as|of|in|typeof|instanceof|void|delete)\b/.source;
const _COMMENT = /\/\*[\s\S]*?\*\/|\/\/[^\n]*/.source;
const _STRING = /"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`/.source;
const _NUMBER = /\b\d+(?:\.\d+)?\b/.source;
const _FN = /\b([A-Za-z_$][\w$]*)(?=\s*\()/.source;
const _TOKEN = new RegExp(`(${_COMMENT})|(${_STRING})|${_KW}|(${_NUMBER})|${_FN}`, 'g');

function highlightCode(code) {
  // 分组：1=comment, 2=string, 3=keyword（_KW 内部 paren）, 4=number, 5=fn 名
  let out = '', last = 0, m;
  _TOKEN.lastIndex = 0;
  while ((m = _TOKEN.exec(code)) !== null) {
    out += escapeHtml(code.slice(last, m.index));
    const tok = m[0];
    if (m[1]) out += `<span class="tok-cmt">${escapeHtml(tok)}</span>`;
    else if (m[2]) out += `<span class="tok-str">${escapeHtml(tok)}</span>`;
    else if (m[3]) out += `<span class="tok-kw">${escapeHtml(tok)}</span>`;
    else if (m[4]) out += `<span class="tok-num">${escapeHtml(tok)}</span>`;
    else if (m[5]) out += `<span class="tok-fn">${escapeHtml(tok)}</span>`;
    else out += escapeHtml(tok);
    last = m.index + tok.length;
  }
  out += escapeHtml(code.slice(last));
  return out;
}

function renderCode(elementOrId, code) {
  const el = typeof elementOrId === 'string' ? document.getElementById(elementOrId) : elementOrId;
  if (!el) return;
  const lines = code.split('\n').map((line, i) => {
    const html = line.length ? highlightCode(line) : ' ';
    return `<span class="line" data-line="${i + 1}">${html}</span>`;
  }).join('\n');
  el.innerHTML = lines;
}

/* ============ 旁注气泡 ============ */
/* showAnnotation(text)  在 .annotation 里显示一行旁注；text 为空则隐藏。 */
function showAnnotation(text, selector = '.annotation') {
  const el = document.querySelector(selector);
  if (!el) return;
  if (text) {
    el.textContent = text;
    el.dataset.show = 'true';
  } else {
    el.dataset.show = 'false';
  }
}

/* ============ 数字 flash 动画 ============ */
/* 给一个 <b class="metric-value"> 数字短暂高亮，提示"刚刚变了"。 */
function flashNumber(el, newValue) {
  el.textContent = newValue;
  el.classList.add('flash');
  setTimeout(() => el.classList.remove('flash'), 200);
}

/* ============ 暴露给全局（无打包工具时直接 <script> 引用） ============ */
window.Player = Player;
window.renderCode = renderCode;
window.highlightCode = highlightCode;
window.escapeHtml = escapeHtml;
window.showAnnotation = showAnnotation;
window.flashNumber = flashNumber;


