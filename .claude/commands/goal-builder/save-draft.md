---
description: Save the current goal draft to a file for review
allowed-tools: Write
argument-hint: [filename]
disable-model-invocation: false
---

# Save Goal Draft

Save the current goal draft to a file for review before creating in Linear.

## Instructions

**WRITE the goal content DIRECTLY to a file** in the PROJECT'S temp folder using the Write tool:

1. Create temp directory if needed:
```bash
mkdir -p .tmp
```

2. **Use Write tool to create the file directly**:
```
# Default location
Write(.tmp/goal-draft.md) with the complete goal content

# Or to a specific file if argument provided
Write(.tmp/$ARGUMENTS-draft.md) with the complete goal content
```

3. After writing, show the file:
```
Read(.tmp/goal-draft.md)
```

**IMPORTANT**:
- DO NOT show draft in chat then copy to file
- DO NOT use cat, echo, or heredoc commands
- DO use the Write tool to create the file directly
- DO use the Read tool to show what was written

After saving:
1. Confirm the file was saved successfully
2. Tell the user where the draft was saved
3. Remind them they can review/edit before creating in Linear
4. Ask if they're ready to create the goal ticket

## Output Format

```
✅ Draft saved successfully to: .tmp/goal-draft.md

You can review or edit the draft before creating the Linear ticket.
When you're ready, I'll create the goal with this exact content.

Ready to proceed with creating the goal in Linear?
```