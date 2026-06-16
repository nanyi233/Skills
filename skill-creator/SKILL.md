---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
---

# Skill Creator

A skill for creating new skills and iteratively improving them.

At a high level, the process goes: decide what you want → write a draft → create test prompts and run them → evaluate qualitatively and quantitatively → rewrite based on feedback → repeat.

## Capturing Intent

Understand what the user wants the skill to do, when it should trigger, expected output format, and whether to set up test cases.

## Writing the SKILL.md

Components:
- **name**: Skill identifier
- **description**: When to trigger, what it does (make it slightly "pushy" to combat undertriggering)
- **Body**: Markdown instructions with progressive disclosure

## Skill Anatomy

```
skill-name/
├── SKILL.md (required, frontmatter + instructions)
└── Bundled Resources (optional)
    ├── scripts/    - Executable code
    ├── references/ - Docs loaded into context
    └── assets/     - Templates, icons
```

### Progressive Disclosure

1. Metadata (name + description) - Always in context (~100 words)
2. SKILL.md body - In context when triggers (<500 lines ideal)
3. Bundled resources - Loaded as needed

### Writing Patterns

- Use imperative form
- Define output formats with templates
- Include examples in Input/Output format
- Explain WHY things matter rather than heavy-handed MUSTs

## Test Cases

After writing draft, create 2-3 realistic test prompts. Save to `evals/evals.json`.

## Running and Evaluating

### Step 1: Spawn runs in parallel

For each test case, spawn subagents - one with skill, one baseline. Launch everything at once.

### Step 2: Draft assertions while runs execute

Good assertions are objectively verifiable with descriptive names.

### Step 3: Capture timing data

When each subagent completes, save timing data immediately.

### Step 4: Grade and view

Grade each run against assertions, aggregate benchmark, launch viewer:

```bash
python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
python eval-viewer/generate_review.py <workspace>/iteration-N --skill-name "name" --benchmark <workspace>/iteration-N/benchmark.json
```

### Step 5: Read feedback and iterate

Read feedback.json, improve the skill, rerun, repeat.

## Description Optimization

After the skill is stable, optimize the description for better triggering:

1. Generate 20 eval queries (should-trigger and should-not-trigger)
2. Review with user using eval_review.html template
3. Run optimization loop:
   ```bash
   python -m scripts.run_loop --eval-set <path> --skill-path <path> --model <model-id> --max-iterations 5
   ```
4. Apply best_description to SKILL.md frontmatter

## Reference Files

- `agents/grader.md` - Evaluating assertions
- `agents/comparator.md` - Blind A/B comparison
- `agents/analyzer.md` - Analyzing benchmark results
- `references/schemas.md` - JSON schemas
