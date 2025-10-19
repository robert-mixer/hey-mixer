---
description: Interactively create a Linear goal ticket from selected GitHub issues
allowed-tools: Bash(python:.claude/scripts/goal-builder/*), Write, Read
argument-hint: [issue-numbers]
disable-model-invocation: false
---

# Create Goal Ticket

Work with the user to create a Linear goal ticket from GitHub issues.

## CRITICAL WORKFLOW

**⚠️ IMPORTANT: Direct file writing and iterative refinement**
1. Draft content with user directly in `.tmp/`
2. **IMMEDIATELY WRITE to `.tmp/goal-draft.md` using Write tool BEFORE asking for approval**
3. Show the written file to user (use Read tool)
4. If user gives feedback → Edit the file directly (use Edit tool)
5. Keep editing until user explicitly approves
6. ONLY create in Linear after explicit approval ("approved", "create it", "looks good")

**NEVER show draft in chat then save it. ALWAYS write directly to file first!**

## Process

This is an INTERACTIVE process where you WRITE THE TICKET CONTENT WITH THE USER.

### 1. Load GitHub Issues

First, get the list of open issues:

```bash
python .claude/scripts/goal-builder/list_issues.py
```

### 2. Draft Ticket Content Interactively

**CRITICAL**: Don't auto-generate content. WRITE THE ACTUAL TICKET with the user:

- Discuss which issues to include
- Plan the goal ticket structure
- **DO NOT display the full draft in chat**
- **Instead, go directly to step 3 to write it to file**
- Include sections like:
  - Description (what needs to be built)
  - Requirements
  - Success Criteria
  - Target (e.g., `modules/auth/`)
  - Related GitHub Issues

### 3. Write Draft Directly to File IMMEDIATELY

**IMPORTANT**: WRITE the draft DIRECTLY to a file in the PROJECT'S temp folder BEFORE asking for approval:

```bash
# Create project temp directory if it doesn't exist
mkdir -p .tmp
```

Then use the **Write tool** to create the file:
```
Write(.tmp/goal-draft.md) with the complete draft content
```

**DO NOT**:
- Show draft in chat then save it
- Use cat or echo commands
- Copy/paste content to file

**DO**:
- Write directly to `.tmp/goal-draft.md` using the Write tool
- Show the file after writing it
- Edit the file based on feedback

### 4. Iterative Refinement Process

**CRITICAL WORKFLOW**:
1. Show the saved draft to the user
2. Ask: "Would you like to make any changes to this draft?"
3. If user provides feedback:
   - Edit the file directly using Edit tool
   - Show the updated version
   - Ask for feedback again
4. Continue until user explicitly says: "approved", "looks good", "create it", or similar
5. DO NOT proceed to Linear until user gives final approval

Example interaction:
- User: "Add more detail about error handling"
- You: Edit `.tmp/goal-draft.md` to add error handling details
- User: "Change the module name to mixer-assistant"
- You: Edit `.tmp/goal-draft.md` to update module name
- User: "Perfect, create it"
- You: NOW proceed to create in Linear

### 5. Create Ticket with Exact Draft Content (ONLY AFTER APPROVAL)

**ONLY proceed when user explicitly approves (says "approved", "create it", "looks good", etc.)**

```bash
# Create the Linear goal ticket with the draft content
python .claude/scripts/goal-builder/create_goal_from_draft.py \
  --draft-file ".tmp/goal-draft.md" \
  --issues "12,15,18" \
  --status "draft"
```

### 6. Close GitHub Issues

After successfully creating the goal:

```bash
# Close the GitHub issues that were included
python .claude/scripts/goal-builder/close_issues.py --issues "12,15,18"
```

### 7. Explain Next Steps

Tell the user:
- The goal is now in "draft" status
- They should review it in Linear
- When ready, change status to "todo" for Plan Builder

## Important

- ALWAYS create with status="draft"
- Get user approval before creating
- The ticket contains EXACTLY what you wrote together
- Close GitHub issues after creating goal
- Explain the draft→todo transition
