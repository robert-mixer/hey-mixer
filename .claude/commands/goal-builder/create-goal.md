---
description: Interactively create a Linear goal ticket from selected GitHub issues
allowed-tools: Bash(python:.claude/scripts/goal-builder/*), Write, Read
argument-hint: [issue-numbers]
disable-model-invocation: false
---

# Create Goal Ticket

Work with the user to create a Linear goal ticket from GitHub issues.

## 🚨 CRITICAL RULE - NEVER SHOW DRAFTS IN CHAT 🚨

**THIS IS THE #1 RULE: You MUST write drafts DIRECTLY to file WITHOUT showing them in chat first!**

### ❌ WRONG WAY (NEVER DO THIS):
1. ❌ Draft content in your response
2. ❌ Show the draft to the user in chat
3. ❌ Ask "What do you think of this draft?"
4. ❌ Then save it to a file

### ✅ CORRECT WAY (ALWAYS DO THIS):
1. ✅ Think about the content internally
2. ✅ IMMEDIATELY use Write tool to save to `.tmp/goal-draft.md`
3. ✅ Use Read tool to show the file to user
4. ✅ Use Edit tool to refine based on feedback
5. ✅ Only create in Linear after explicit approval

**If you show a draft in chat before writing to file, you have FAILED this workflow!**

## Process

This is an INTERACTIVE process where you WRITE THE TICKET CONTENT WITH THE USER.

### 1. Load GitHub Issues

First, get the list of open issues:

```bash
python .claude/scripts/goal-builder/list_issues.py
```

### 1.5 Load Full Issue Content (if issue number provided as argument)

**IMPORTANT**: If an issue number was provided as an argument to this command (e.g., `/goal-builder:create-goal 11`), you MUST load the full issue content before drafting:

```bash
python .claude/scripts/goal-builder/load_issue.py --issue-number 11
```

This displays the **FULL issue body** (not just the 200-char preview). You need this complete context to draft a comprehensive goal ticket that accurately captures all the requirements from the GitHub issue.

**Why this is critical:**
- `list_issues.py` only shows 200-char previews for discovery
- The full issue body contains all the detailed requirements
- Without loading the full content, you're drafting from incomplete information

### 2. CONTINUOUSLY Write and Update Draft File During Discussion

**FROM THE VERY FIRST MESSAGE: Start writing to `.tmp/goal-draft.md` IMMEDIATELY!**

- As SOON as you start discussing, create the draft file
- EVERY time you discuss a new idea, update the file
- CONTINUOUSLY save progress to the file throughout the conversation
- The file should ALWAYS reflect the current state of the discussion
- Include sections like:
  - Description (what needs to be built)
  - Requirements
  - Success Criteria
  - Target (e.g., `modules/auth/`)
  - Related GitHub Issues

**The draft file is your LIVE WORKING DOCUMENT - update it constantly!**
- Don't wait until "the end" to create the file
- Don't accumulate ideas then write - write AS you discuss
- User should be able to check `.tmp/goal-draft.md` at ANY point and see current progress

### 3. File Operations During Discussion

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
