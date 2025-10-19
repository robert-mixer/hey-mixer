---
description: Display all open GitHub issues from the configured repository
allowed-tools: Bash(python:.claude/scripts/goal-builder/list_issues.py)
disable-model-invocation: false
---

# Show GitHub Issues

Display all open GitHub issues from the configured repository to start the goal creation workflow.

## Instructions

Run the list_issues.py script to fetch and display all open issues:

```bash
python .claude/scripts/goal-builder/list_issues.py
```

After displaying issues:
1. Analyze the issues for logical groupings
2. Suggest which issues could be combined into goals
3. Ask the user what they'd like to work on
