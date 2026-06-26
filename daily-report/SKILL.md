---
name: daily-report
description: Generates a daily work summary for UE5/Lua programmers by analyzing conversation logs from today. Extracts the top 3 most valuable technical insights, solutions, and implementations related to Unreal Engine and Lua development. Trigger when the user asks for a daily report, today's summary, work recap, or mentions "日报". Use this to help developers track their daily progress and consolidate learning.
---

# Daily Report Assistant

Automatically generates daily work summaries by analyzing your Claude conversation logs. Extracts the most valuable UE5 and Lua programming insights from your sessions.

## What This Does

This skill scans your conversation history from today across multiple Claude directories, identifies technical content related to Unreal Engine 5 and Lua programming, and presents the top 3 most valuable insights in a structured report.

**Why it's useful**: As a developer working across multiple sessions, it's easy to lose track of solutions, patterns, and insights discovered during the day. This daily summary helps consolidate learning and track progress on core technical work.

## Usage

Invoke this skill by saying:

- "生成今天的日报" / "generate daily report"
- "今天做了什么" / "what did I do today"
- "总结今天的工作" / "summarize today's work"
- "日报" / "daily report"
- "/daily-report"

You can also specify a date:
- "/daily-report 2026-06-25" (generates report for that specific date)

## Output Format

The report includes:

```markdown
# 📋 Daily Report - YYYY-MM-DD

## 🎯 Top 3 Technical Insights

### 1. [Brief Title]
**Category**: UE5/Lua
**Session**: [Session name]
**Time**: HH:MM

**Summary**: Brief description of the insight/solution

**Code**: 
```language
relevant code snippet if applicable
```

**Relevance Score**: X.X

[Repeat for items 2 and 3]

## 📊 Summary
- Conversations analyzed: N files
- Total insights found: N
- UE5-related: X insights
- Lua-related: Y insights
- Time span: HH:MM - HH:MM
```

## How It Works

1. **Scans conversation directories**: 
   - `C:\Users\v_beitma\.claude\projects\`
   - `C:\Users\v_beitma\.claude-internal\projects\`

2. **Filters by date**: Only processes conversations from the target date (default: today)

3. **Identifies relevant content** using keyword matching:
   - **UE5**: Unreal, Blueprint, Actor, Component, UMG, Slate, UPROPERTY, UFUNCTION, etc.
   - **Lua**: require, local, function, table, pairs, metatable, coroutine, etc.

4. **Scores insights** based on:
   - Technical keywords present
   - Code blocks included
   - Problem-solving indicators (fix, implement, optimize, debug)
   - Content depth and completeness

5. **Ranks and formats** the top 3 insights as a readable markdown report

## Implementation

When this skill is invoked:

1. Extract the date parameter (if provided), otherwise use today's date
2. Run the Python extraction script
3. Parse the JSON output
4. Format and present the report to the user

```bash
python scripts/generate_report.py [YYYY-MM-DD]
```

The script handles:
- Large JSONL file parsing (line-by-line, memory-efficient)
- Multiple timestamp formats (ISO 8601, epoch milliseconds)
- Multi-language content (Chinese and English)
- Edge cases (no data, no matches, etc.)

## Examples

**Example invocation:**
```
User: 生成今天的日报
```

**Example output:**
```markdown
# 📋 Daily Report - 2026-06-26

## 🎯 Top 3 Technical Insights

### 1. UE5 Actor Component lifecycle management
**Category**: UE5
**Session**: Working on gameplay systems
**Time**: 14:23

**Summary**: Discussed the proper initialization order for Actor Components in UE5, specifically when to use BeginPlay vs PostInitializeComponents for dependency setup...

**Code**:
```cpp
void UMyComponent::PostInitializeComponents()
{
    Super::PostInitializeComponents();
    // Safe to access other components here
    MyOtherComponent = GetOwner()->FindComponentByClass<UMyOtherComponent>();
}
```

**Relevance Score**: 24.5

### 2. Lua metatable for data validation
**Category**: Lua
**Session**: Lua scripting framework
**Time**: 15:47

**Summary**: Implemented a metatable-based validation system for game configuration tables...

**Relevance Score**: 18.0

### 3. Blueprint-Lua bridge optimization
**Category**: UE5, Lua
**Session**: Performance profiling
**Time**: 16:12

**Summary**: Identified and fixed performance bottleneck in Blueprint-to-Lua function calls by implementing batched updates...

**Relevance Score**: 22.3

## 📊 Summary
- Conversations analyzed: 5 files
- Total insights found: 12
- UE5-related: 8 insights
- Lua-related: 7 insights
- Time span: 09:15 - 17:30
```

## Edge Cases

- **No UE5/Lua content today**: Reports 0 insights gracefully
- **Very active day**: Still selects top 3, preventing information overload
- **Mixed languages**: Handles both Chinese and English content
- **Large files**: Uses streaming parsing to avoid memory issues

## Limitations

- Only analyzes `.jsonl` conversation files from Claude Code
- Does not currently parse `.codex` SQLite databases (different tool)
- Keyword-based filtering (not LLM classification)
- Fixed to top 3 insights (not configurable)
