---
description: Display all draft Linear goal tickets that can be edited
allowed-tools: Bash(python:.claude/scripts/goal-builder/list_drafts.py)
disable-model-invocation: false
---

# Show Draft Goals

Display all Linear goal tickets with status="draft" to review or edit them.

## Instructions

Run the list_drafts.py script to fetch and display all draft goals:

```bash
python .claude/scripts/goal-builder/list_drafts.py
```

After displaying drafts:
1. Show the user which draft goals exist
2. Ask if they want to edit any of them
3. If yes, guide them to use `/goal-builder:edit-draft [goal-id]`

## Example Output

The script will display:
- Goal identifier (e.g., SYS-8)
- Title
- Current status
- URL to view in Linear
- Description preview

## Next Steps

After showing drafts, ask the user:
- "Would you like to edit any of these draft goals?"
- "Or would you like to create a new goal instead?"
