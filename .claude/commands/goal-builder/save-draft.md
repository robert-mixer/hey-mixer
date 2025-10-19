---
description: Save the current goal draft to a file for review
allowed-tools: Write
argument-hint: [filename]
disable-model-invocation: false
---

# Save Goal Draft

Save the current goal draft to a file for review before creating in Linear.

## Instructions

Save the agreed-upon goal content to a temporary file:

```bash
# Default location
cat > /tmp/goal-draft.md << 'EOF'
[INSERT THE EXACT APPROVED GOAL CONTENT HERE]
EOF

# Or to a specific file if provided
cat > /tmp/$ARGUMENTS-draft.md << 'EOF'
[INSERT THE EXACT APPROVED GOAL CONTENT HERE]
EOF
```

After saving:
1. Confirm the file was saved successfully
2. Tell the user where the draft was saved
3. Remind them they can review/edit before creating in Linear
4. Ask if they're ready to create the goal ticket

## Output Format

```
✅ Draft saved successfully to: /tmp/goal-draft.md

You can review or edit the draft before creating the Linear ticket.
When you're ready, I'll create the goal with this exact content.

Ready to proceed with creating the goal in Linear?
```