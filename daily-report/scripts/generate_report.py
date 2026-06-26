#!/usr/bin/env python3
"""
Daily Report Generator for UE5/Lua Programmers
Analyzes Claude conversation logs to extract valuable technical insights.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, date
from typing import List, Dict, Any, Tuple
import re

# Keywords for filtering relevant content
# Broad keywords (scoring only — don't confirm category alone)
UE5_BROAD_KEYWORDS = {
    'unreal', 'ue5', 'ue4', 'blueprint', 'actor', 'component', 'gamemode',
    'playercontroller', 'pawn', 'character', 'hud', 'gameplay',
}

# UE5-specific keywords (at least one required to confirm UE5 category)
UE5_SPECIFIC_KEYWORDS = {
    'uproperty', 'ufunction', 'uclass', 'ustruct', 'uenum', 'subsystem',
    'fstring', 'tarray', 'tmap', 'tset', 'delegate', 'multicast',
    'umg', 'slate', 'niagara', 'montage', 'animinstance',
    'gameplayability', 'gameplayeffect', 'gameplaytag', 'gameplaycue',
    'enhancedinput', 'gasa', 'uparam', 'umeta', 'editdefaultsonly',
    'blueprintreadonly', 'blueprintreadwrite', 'visibleanywhere',
}

# Lua broad keywords (common with JS/Python — scoring only)
LUA_BROAD_KEYWORDS = {
    'lua', 'require', 'function', 'table', 'local',
}

# Lua-specific keywords (at least one required to confirm Lua category)
LUA_SPECIFIC_KEYWORDS = {
    'pairs', 'ipairs', 'coroutine', 'metatable', 'setmetatable',
    'getmetatable', '__index', '__newindex', 'pcall', 'xpcall',
    'loadstring', 'dofile', 'luajit', 'lua_newtable', 'lua_push',
    'tolua', 'unlua', 'slua', 'luastate',
}

PROBLEM_SOLVING_KEYWORDS = {
    'fix', 'solve', 'implement', 'create', 'optimize', 'refactor', 'debug',
    'issue', 'problem', 'solution', 'error', 'bug', 'crash', 'performance'
}

# Negative keywords that indicate meta/skill-building content (penalize score)
NEGATIVE_CONTEXT_KEYWORDS = {
    'daily-report', 'daily report', 'skill.md', 'skills directory',
    'generate_report.py', 'base directory for this skill',
    '日报', 'skill creator', 'skill-creator', 'claude code skill',
    'what can i help you with', 'how can i help you'
}


def parse_timestamp(ts: Any) -> datetime:
    """Parse timestamp from ISO string or epoch milliseconds."""
    if isinstance(ts, str):
        # ISO 8601 format
        return datetime.fromisoformat(ts.replace('Z', '+00:00'))
    elif isinstance(ts, (int, float)):
        # Epoch milliseconds
        return datetime.fromtimestamp(ts / 1000)
    return datetime.now()


def extract_text_content(content: Any) -> str:
    """Extract text from various content formats."""
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        texts = []
        for item in content:
            if isinstance(item, dict):
                if item.get('type') == 'text':
                    texts.append(item.get('text', ''))
                elif item.get('type') == 'tool_use':
                    # Include tool use information
                    tool_name = item.get('name', '')
                    tool_input = item.get('input', {})
                    texts.append(f"Tool: {tool_name}\n{json.dumps(tool_input, indent=2)}")
            elif isinstance(item, str):
                texts.append(item)
        return '\n'.join(texts)
    elif isinstance(content, dict):
        if content.get('type') == 'text':
            return content.get('text', '')
    return ''


def calculate_relevance_score(text: str) -> Tuple[float, set]:
    """Calculate relevance score and identify matching categories."""
    text_lower = text.lower()
    score = 0.0
    categories = set()

    # UE5: broad keywords contribute score, specific keywords confirm category
    ue5_broad = sum(1 for kw in UE5_BROAD_KEYWORDS if kw in text_lower)
    ue5_specific = sum(1 for kw in UE5_SPECIFIC_KEYWORDS if kw in text_lower)
    score += (ue5_broad + ue5_specific) * 2
    # Only add UE5 category if at least one specific keyword matches
    if ue5_specific > 0:
        categories.add('UE5')

    # Lua: broad keywords contribute score, specific keywords confirm category
    lua_broad = sum(1 for kw in LUA_BROAD_KEYWORDS if kw in text_lower)
    lua_specific = sum(1 for kw in LUA_SPECIFIC_KEYWORDS if kw in text_lower)
    score += (lua_broad + lua_specific) * 2
    # Only add Lua category if at least one specific keyword matches
    if lua_specific > 0:
        categories.add('Lua')

    # Check for problem-solving keywords
    problem_matches = sum(1 for kw in PROBLEM_SOLVING_KEYWORDS if kw in text_lower)
    score += problem_matches * 1.5

    # Bonus for code blocks
    code_blocks = len(re.findall(r'```[\s\S]*?```', text))
    score += code_blocks * 5

    # If negative context detected, heavily suppress the score
    # (skill-building meta content is not real development work)
    negative_matches = sum(1 for kw in NEGATIVE_CONTEXT_KEYWORDS if kw in text_lower)
    if negative_matches > 0:
        score *= 0.2  # Reduce to 20% when meta content detected

    # Bonus for substantial content
    if len(text) > 500:
        score += 2
    if len(text) > 1500:
        score += 3

    return score, categories


# Paths to exclude from scanning (case-insensitive match)
EXCLUDED_PATH_PATTERNS = ['skills', 'plans', 'memory']


def is_excluded_path(file_path: Path) -> bool:
    """Check if the file path contains any excluded directory pattern."""
    path_lower = str(file_path).lower()
    for pattern in EXCLUDED_PATH_PATTERNS:
        if f'/{pattern}/' in path_lower or f'\\{pattern}\\' in path_lower or path_lower.endswith(f'/{pattern}') or path_lower.endswith(f'\\{pattern}'):
            return True
    return False


def is_raw_content_tool_only(content: Any) -> bool:
    """Check raw message content — if it's only tool_use blocks, skip it."""
    if isinstance(content, list):
        if not content:
            return True
        tool_blocks = sum(1 for item in content
                         if isinstance(item, dict) and item.get('type') == 'tool_use')
        return tool_blocks / len(content) > 0.5
    return False


def is_tool_call_only(content: str) -> bool:
    """Check if the content is predominantly tool calls, not real conversation."""
    if not content.strip():
        return True
    # If content starts with "Tool:" and has very little non-tool text, skip it
    lines = content.strip().split('\n')
    tool_lines = sum(1 for line in lines if line.strip().startswith('Tool:'))
    # If more than 50% of non-empty lines are tool lines, it's tool-heavy
    non_empty = [l for l in lines if l.strip()]
    if not non_empty:
        return True
    return tool_lines / len(non_empty) > 0.5


def find_conversation_files(target_date: date) -> List[Path]:
    """Find all conversation files modified on the target date."""
    base_paths = [
        Path.home() / '.claude' / 'projects',
        Path.home() / '.claude-internal' / 'projects',
    ]

    files = []
    for base_path in base_paths:
        if not base_path.exists():
            continue

        # Recursively find all .jsonl files
        for jsonl_file in base_path.rglob('*.jsonl'):
            # Skip excluded paths (skills, plans, memory, etc.)
            if is_excluded_path(jsonl_file):
                continue

            # Check modification time
            mtime = datetime.fromtimestamp(jsonl_file.stat().st_mtime)
            if mtime.date() == target_date:
                files.append(jsonl_file)

    return files


def extract_insights(files: List[Path]) -> List[Dict[str, Any]]:
    """Extract and rank insights from conversation files."""
    insights = []

    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                conversation = []
                session_title = "Unknown Session"

                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    # Capture session title
                    if entry.get('type') == 'ai-title':
                        session_title = entry.get('aiTitle', session_title)

                    # Extract user and assistant messages
                    if entry.get('type') in ['user', 'assistant']:
                        message = entry.get('message', {})
                        role = message.get('role')
                        content = message.get('content', '')
                        timestamp = entry.get('timestamp')

                        if role and content:
                            # Skip messages that are purely tool calls (no real conversation)
                            if is_raw_content_tool_only(content):
                                continue

                            text_content = extract_text_content(content)

                            # Double check: also skip if extracted text is empty or tool-only
                            if not text_content.strip() or is_tool_call_only(text_content):
                                continue

                            conversation.append({
                                'role': role,
                                'content': text_content,
                                'timestamp': parse_timestamp(timestamp) if timestamp else None,
                                'session_title': session_title,
                                'file': file_path.name
                            })

                # Analyze conversation for insights
                for i, msg in enumerate(conversation):
                    if msg['role'] == 'assistant' and msg['content']:
                        # Skip messages that are purely tool calls
                        if is_tool_call_only(msg['content']):
                            continue

                        # Get context from previous user message
                        user_context = ''
                        if i > 0 and conversation[i-1]['role'] == 'user':
                            user_context = conversation[i-1]['content']

                        score, categories = calculate_relevance_score(
                            user_context + '\n' + msg['content']
                        )

                        if score > 15 and categories:  # Higher threshold after filtering improvements
                            insights.append({
                                'score': score,
                                'categories': categories,
                                'user_prompt': user_context[:500],  # Truncate for context
                                'assistant_response': msg['content'],
                                'timestamp': msg['timestamp'],
                                'session_title': msg['session_title'],
                                'file': msg['file']
                            })

        except Exception as e:
            print(f"Warning: Error processing {file_path}: {e}", file=sys.stderr)

    # Sort by score (descending)
    insights.sort(key=lambda x: x['score'], reverse=True)

    return insights


def extract_code_snippet(text: str, max_lines: int = 20) -> str:
    """Extract first code block or truncate if too long."""
    code_match = re.search(r'```(\w*)\n([\s\S]*?)```', text)
    if code_match:
        lang = code_match.group(1) or 'text'
        code = code_match.group(2)
        lines = code.split('\n')
        if len(lines) > max_lines:
            code = '\n'.join(lines[:max_lines]) + '\n... (truncated)'
        return f"```{lang}\n{code}\n```"
    return ''


def generate_insight_title(user_prompt: str, categories: set) -> str:
    """Generate a brief title for the insight."""
    # Try to extract first meaningful sentence
    sentences = re.split(r'[.!?]\s+', user_prompt)
    if sentences and sentences[0]:
        title = sentences[0][:80]
        if len(sentences[0]) > 80:
            title += '...'
        return title

    # Fallback to categories
    return f"{'/'.join(sorted(categories))} Work"


def format_report(insights: List[Dict[str, Any]], target_date: date, total_files: int) -> str:
    """Format insights as a markdown report."""
    report = [f"# 📋 Daily Report - {target_date.strftime('%Y-%m-%d')}\n"]

    if not insights:
        report.append("## No UE5/Lua technical insights found for today.\n")
        report.append(f"Analyzed {total_files} conversation file(s).\n")
        return '\n'.join(report)

    report.append("## 🎯 Top 3 Technical Insights\n")

    # Show top 3
    for idx, insight in enumerate(insights[:3], 1):
        title = generate_insight_title(insight['user_prompt'], insight['categories'])
        categories_str = ', '.join(sorted(insight['categories']))

        report.append(f"### {idx}. {title}\n")
        report.append(f"**Category**: {categories_str}  ")
        report.append(f"**Session**: {insight['session_title']}  ")

        if insight['timestamp']:
            report.append(f"**Time**: {insight['timestamp'].strftime('%H:%M')}  \n")

        # Extract key content
        response = insight['assistant_response']

        # Try to extract a summary (first paragraph or first 300 chars)
        paragraphs = response.split('\n\n')
        summary = paragraphs[0] if paragraphs else response[:300]
        if len(summary) > 300:
            summary = summary[:300] + '...'

        report.append(f"\n**Summary**: {summary}\n")

        # Include code snippet if available
        code = extract_code_snippet(response)
        if code:
            report.append(f"\n{code}\n")

        report.append(f"**Relevance Score**: {insight['score']:.1f}\n")

    # Summary statistics
    report.append("\n## 📊 Summary\n")
    report.append(f"- **Conversations analyzed**: {total_files} file(s)")
    report.append(f"- **Total insights found**: {len(insights)}")

    ue5_count = sum(1 for i in insights if 'UE5' in i['categories'])
    lua_count = sum(1 for i in insights if 'Lua' in i['categories'])

    report.append(f"- **UE5-related**: {ue5_count} insights")
    report.append(f"- **Lua-related**: {lua_count} insights")

    if insights and insights[0]['timestamp'] and insights[-1]['timestamp']:
        earliest = min(i['timestamp'] for i in insights if i['timestamp'])
        latest = max(i['timestamp'] for i in insights if i['timestamp'])
        report.append(f"- **Time span**: {earliest.strftime('%H:%M')} - {latest.strftime('%H:%M')}")

    return '\n'.join(report)


def main():
    # Set UTF-8 encoding for stdout on Windows
    import io
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    # Parse arguments
    if len(sys.argv) > 1:
        try:
            target_date = datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
        except ValueError:
            print(f"Error: Invalid date format. Use YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)
    else:
        target_date = date.today()

    # Find conversation files
    files = find_conversation_files(target_date)

    if not files:
        print(f"No conversation files found for {target_date}")
        sys.exit(0)

    # Extract insights
    insights = extract_insights(files)

    # Generate report
    report = format_report(insights, target_date, len(files))

    print(report)


if __name__ == '__main__':
    main()
