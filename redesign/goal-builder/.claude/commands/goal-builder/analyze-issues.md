---
description: Analyze GitHub issues and suggest logical groupings for goals
allowed-tools: Bash(python:.claude/scripts/goal-builder/list_issues.py), Read
disable-model-invocation: false
---

# Analyze Issues for Goal Groupings

Fetch GitHub issues and provide intelligent grouping suggestions.

## Instructions

1. Get the list of open issues:
```bash
python .claude/scripts/goal-builder/list_issues.py
```

2. Analyze the issues for:
   - Feature areas (authentication, UI, data, etc.)
   - Technical dependencies
   - Implementation complexity
   - Business priorities

3. Present grouping suggestions:
   - Group related issues that form complete features
   - Identify dependencies between issues
   - Suggest priority order
   - Estimate complexity for each group

4. Format output as:
```
**[Group Name]** ([Priority])
- #[number]: [title] ([complexity])
- #[number]: [title] ([complexity])
Rationale: [Why these belong together]

Estimated effort: [small/medium/large]
Dependencies: [any prerequisites]
```

5. Ask the user which grouping they'd like to convert into a goal