---
description: Edit an existing draft Linear goal ticket
argument-hint: [goal-id] [--auto-update]
disable-model-invocation: false
---

# Edit Draft Goal

Work with the user to modify an existing draft Linear goal ticket.

---

## Arguments

**$ARGUMENTS** may contain:
1. **Goal ID** (optional): `SYS-10` - if provided, edit that specific goal
2. **--auto-update flag** (optional): Skip approval prompts

**Examples**:
- `/edit-draft` → List all drafts, user picks one, normal mode
- `/edit-draft SYS-10` → Edit SYS-10, normal mode (requires approval)
- `/edit-draft SYS-10 --auto-update` → Edit SYS-10, auto-update mode (no approval)

---

## Command-Specific Workflow

### Step 1: Parse Arguments

Extract from $ARGUMENTS:
- Goal ID if provided (e.g., "SYS-10")
- `--auto-update` flag presence

### Step 2: Load Existing Draft

**If goal ID was provided**:
- Use `mcp__linear__get_issue` with that ID
- Load complete goal content

**If NO goal ID provided**:
- Use `mcp__linear__list_issues` with filter: labels="goal", state="Draft"
- Show list of draft goals
- Ask user: "Which goal would you like to edit?"
- Wait for user to specify goal ID
- Then use `mcp__linear__get_issue`

### Step 3: Initialize Version Tracking

Check if editing an existing session:
- If `.tmp/goal-version.txt` exists: Read current version number
- If NOT exists: `echo "1" > .tmp/goal-version.txt`

### Step 4: Load Current Content to File

**🚨 CRITICAL**: Write current content DIRECTLY to file WITHOUT showing in chat first!

1. ✅ Take goal content from Linear
2. ✅ **Immediately** use Write tool: `.tmp/goal-draft-v{N}.md`
3. ✅ Use Read tool to show file to user
4. ✅ Tell user: "Here's the current draft. What would you like to change?"

❌ **NEVER** show content in chat before writing to file!

### Step 5: User Requests Changes

User will describe what they want changed. For EACH change request:

1. Increment version: Read `.tmp/goal-version.txt`, increment, save
2. Apply changes with Edit tool to `.tmp/goal-draft-v{N}.md`
3. Generate diff: `.tmp/goal-draft-v{N-1}-to-v{N}.diff`
4. Show diff to user: "Here's what changed:"
5. Use Read tool to show updated file

Repeat until user is satisfied.

### Step 6: Get Approval (Normal Mode) OR Auto-Proceed (Auto-Update Mode)

**If --auto-update flag WAS present**:
- State: "🔥 Auto-update mode. Updating to Linear immediately..."
- Proceed to Step 7 without waiting

**If --auto-update flag was NOT present (normal mode)**:
- Ask: "Should I update this goal in Linear?"
- Wait for approval phrases (you know these from system.md)
- Only proceed after explicit approval

**If mid-workflow signal received** ("SWITCH TO AUTO-UPDATE MODE: ..."):
- Acknowledge switch
- Apply final changes from signal
- Proceed without approval

### Step 7: Update in Linear

Use `mcp__linear__update_issue` with:
- id: The goal ID (e.g., "SYS-10")
- title: From latest draft version
- description: From latest draft version

### Step 8: Archive Complete History

Move all versions and diffs to archive:
```
.tmp/archives/{GOAL-ID}/{TIMESTAMP}/
  ├── goal-draft-v1.md
  ├── goal-draft-v{N}.md
  ├── goal-draft-v1-to-v2.diff
  ├── goal-draft-v{N-1}-to-v{N}.diff
  └── goal-version.txt
```

Clean up working directory.

### Step 9: Confirm Success

Tell user:
- "✅ Updated goal {GOAL-ID} in Linear"
- "Archived {N} versions to .tmp/archives/{GOAL-ID}/"

---

## Command-Specific Edge Cases

### Goal ID Doesn't Exist
- Error: "Goal {GOAL-ID} not found in Linear"
- Ask user to verify goal ID
- Suggest: Use `/show-drafts` to see available goals
- Don't proceed

### Goal Status Is Not "Draft"
- Error: "Cannot edit goal {GOAL-ID}: status is '{status}', not 'draft'"
- Explain: Only draft goals can be edited via this command
- Suggest: Edit directly in Linear if status is todo/doing/done
- Don't proceed

### No Draft Goals Exist (when no ID provided)
- Message: "No draft goals found. Create one with `/create-goal`"
- Don't proceed

### User Says "Never Mind" Mid-Edit
- Don't update to Linear
- Don't archive
- Clean up `.tmp/goal-draft*.md` and `.tmp/goal-version.txt`
- Message: "Edit cancelled. No changes made to Linear."

---

## Notes

**Everything else you need is already in context from /prime**:
- Approval policy → system.md
- Version management details → system.md
- Archive system details → system.md
- MCP tool complete syntax → developer.md
- Goal template structure → TEMPLATES.md
- General workflow patterns → WORKFLOW.md

This file contains ONLY edit-draft command-specific details.
