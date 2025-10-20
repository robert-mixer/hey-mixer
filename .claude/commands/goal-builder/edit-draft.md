---
description: Edit an existing draft Linear goal ticket
allowed-tools: Bash(python:.claude/scripts/goal-builder/*), Write, Read, Edit
argument-hint: [goal-id]
disable-model-invocation: false
---

# Edit Draft Goal

Work with the user to modify an existing draft Linear goal ticket.

## 🚨 CRITICAL RULE - WRITE DIRECTLY TO FILE 🚨

**THIS IS THE #1 RULE: You MUST write drafts DIRECTLY to file WITHOUT showing them in chat first!**

### ✅ CORRECT WAY (ALWAYS DO THIS):
1. ✅ Fetch the current goal content from Linear
2. ✅ IMMEDIATELY use Write tool to save to `.tmp/goal-draft.md`
3. ✅ Use Read tool to show the file to user
4. ✅ Use Edit tool to refine based on feedback
5. ✅ Only update in Linear after explicit approval

## Process

This is an INTERACTIVE process where you UPDATE THE TICKET CONTENT WITH THE USER.

### 1. Load Current Draft from Linear

First, get the list of draft goals and the specific goal to edit:

```bash
python .claude/scripts/goal-builder/list_drafts.py
```

If a goal-id is provided in arguments, fetch that specific goal. Otherwise, show all drafts and ask which one to edit.

### 2. Load Full Goal Content and Write to Draft File

**IMPORTANT**: Use the `load_goal.py` script to fetch the complete goal description from Linear:

```bash
# Create project temp directory if it doesn't exist
mkdir -p .tmp

# Load the full goal content directly to the draft file
python .claude/scripts/goal-builder/load_goal.py \
  --goal-id "SYS-8" \
  --description-only > .tmp/goal-draft.md
```

**Why use load_goal.py:**
- `list_drafts.py` only shows 200-char previews for discovery
- `load_goal.py` fetches the **complete description** from Linear
- The `--description-only` flag outputs just the markdown content (perfect for piping to file)
- This ensures you have the full current content to work with

Then verify the file was created:
```
Read(.tmp/goal-draft.md) to show the current content to the user
```

### 3. Show Current Content and Discuss Changes

Show the user what's currently in the goal and ask what they want to change:

```
Read(.tmp/goal-draft.md)
```

Then ask: "What would you like to change in this goal?"

### 4. Iterative Refinement Process

**CRITICAL WORKFLOW**:
1. Listen to user's requested changes
2. Edit the file directly using Edit tool
3. Show the updated version with Read tool
4. Ask for more feedback
5. Continue until user explicitly says: "approved", "looks good", "update it", or similar
6. DO NOT proceed to Linear until user gives final approval

Example interaction:
- User: "Add more detail about the voice activation system"
- You: Edit `.tmp/goal-draft.md` to add voice activation details
- User: "Change the success criteria to be more specific"
- You: Edit `.tmp/goal-draft.md` to update success criteria
- User: "Perfect, update it in Linear"
- You: NOW proceed to update in Linear

### 5. Update Ticket in Linear (ONLY AFTER APPROVAL)

**ONLY proceed when user explicitly approves (says "approved", "update it", "looks good", etc.)**

```bash
# Update the Linear goal with the new draft content
python .claude/scripts/goal-builder/update_goal.py \
  --goal-id "SYS-8" \
  --draft-file ".tmp/goal-draft.md"
```

### 6. Confirm Success

Tell the user:
- The goal has been updated in Linear
- They should review it
- Next steps (when ready, change status to "todo" for Plan Builder)

## Important

- Load current content from Linear first
- ALWAYS write to `.tmp/goal-draft.md` before showing to user
- Get user approval before updating in Linear
- The ticket will contain EXACTLY what you wrote together
- Explain that this doesn't change the status (stays as "draft")
