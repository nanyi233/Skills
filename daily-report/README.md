# Daily Report Assistant for UE5/Lua Programmers

自动生成每日工作总结的技能，通过分析 Claude 对话记录提取最有价值的 UE5 和 Lua 技术洞察。

## 功能特性

- 📊 自动扫描当天的对话记录
- 🎯 识别 UE5 和 Lua 相关的技术内容
- 🏆 智能评分并提取最有价值的 Top 3 见解
- 📝 生成结构化的 Markdown 日报

## 使用方法

### 基础用法

直接对 Claude 说：

```
生成今天的日报
```

或者：

```
/daily-report
```

### 查询历史日期

```
/daily-report 2026-06-24
```

### 其他触发方式

- "今天做了什么"
- "总结今天的工作"
- "日报"
- "generate daily report"
- "what did I do today"

## 示例输出

```markdown
# 📋 Daily Report - 2026-06-24

## 🎯 Top 3 Technical Insights

### 1. GAS Attribute Set 实现和UI绑定
**Category**: UE5
**Session**: gas-attributes-ui-setup
**Time**: 08:40

**Summary**: 实现了基于 Gameplay Ability System 的属性系统...

**Relevance Score**: 150.0

### 2. Mermaid 流程图展示蓝图逻辑
**Category**: UE5
**Session**: gas-attributes-ui-setup
**Time**: 07:08

**Summary**: 用 Mermaid 详细展示 WBP_PlayerHUD 的蓝图逻辑流程...

**Relevance Score**: 60.0

### 3. GAS 属性系统设计理念
**Category**: UE5
**Session**: gas-attributes-ui-setup
**Time**: 07:55

**Summary**: 解释了 Health 和 MaxHealth 的设计区别...

**Relevance Score**: 51.0

## 📊 Summary
- Conversations analyzed: 26 files
- Total insights found: 42
- UE5-related: 40 insights
- Lua-related: 14 insights
- Time span: 03:05 - 09:44
```

## 技术实现

### 数据源

扫描以下目录的对话记录：
- `C:\Users\v_beitma\.claude\projects\**\*.jsonl`
- `C:\Users\v_beitma\.claude-internal\projects\**\*.jsonl`

### 关键词识别

**UE5 关键词**:
- unreal, ue5, ue4, blueprint, actor, component
- gamemode, playercontroller, widget, umg, slate
- uproperty, ufunction, uclass, ustruct
- subsystem, pawn, character, animation, niagara

**Lua 关键词**:
- lua, require, local, function, table
- pairs, ipairs, coroutine, metatable
- pcall, xpcall, loadstring

### 评分算法

根据以下因素计算相关性分数：
- 关键词匹配数量 (×2 分)
- 问题解决关键词 (fix, implement, optimize 等, ×1.5 分)
- 代码块数量 (×5 分/块)
- 内容深度 (500+ 字符 +2 分, 1500+ 字符 +3 分)

## 文件结构

```
daily-report/
├── README.md                    # 本文件
├── SKILL.md                     # 技能定义
└── scripts/
    └── generate_report.py       # Python 提取脚本
```

## 系统要求

- Python 3.6+
- 标准库：json, pathlib, datetime, re
- 无需额外依赖

## 限制和注意事项

- 仅分析 `.jsonl` 格式的对话记录
- 不支持 `.codex` SQLite 数据库（不同工具）
- 基于关键词过滤（非 LLM 分类）
- 固定返回 Top 3（不可配置数量）
- 大文件使用流式解析（内存友好）

## 故障排查

### 没有找到对话记录

检查目标日期是否有对话文件：
```bash
ls -lt C:\Users\v_beitma\.claude\projects\C--Users-v-beitma\*.jsonl
```

### Unicode 编码错误

脚本已处理 Windows GBK 编码问题，会自动设置 UTF-8 输出。

### 识别不到 UE5/Lua 内容

确认对话中包含相关关键词。可以查看评分逻辑调整阈值。

## 未来改进方向

- [ ] 支持自定义关键词配置
- [ ] 可配置返回数量（不限 Top 3）
- [ ] 添加 .codex SQLite 支持
- [ ] LLM 分类替代关键词过滤
- [ ] 导出为 PDF/HTML 格式
- [ ] 周报/月报聚合功能

## 版本历史

- **v1.0** (2026-06-26): 初始版本
  - 支持 .jsonl 对话记录分析
  - UE5/Lua 关键词识别
  - Top 3 智能评分和排序
  - Markdown 格式输出
