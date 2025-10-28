---
description: Edit an existing draft Linear goal ticket
allowed-tools: Bash(python:.claude/scripts/goal-builder/*), Write, Read, Edit
argument-hint: [goal-id] [--auto-update]
disable-model-invocation: false
---

# Edit Draft Goal

Work with the user to modify an existing draft Linear goal ticket.

## 🔥 Arguments Received

**Arguments:** $ARGUMENTS

**AUTO-UPDATE MODE DETECTION:**

Check if the arguments contain the `--auto-update` flag:

- **If `--auto-update` IS present:** You are in AUTO-UPDATE MODE
  - ✅ Skip approval prompts and update to Linear immediately (99% of cases)
  - ✅ Still show what you're doing for transparency
  - ✅ State: "🔥 Auto-update mode detected. Updating to Linear immediately..."
  - ✅ Exception: If you detect inconsistency/confusion, ask for clarification

- **If `--auto-update` is NOT present (default):** Follow normal approval workflow
  - ✅ Edit the goal interactively
  - ✅ Ask "Should I update this in Linear?" and wait for user approval
  - ✅ Only update after explicit approval

**Command Examples:**
```
/goal-builder:edit-draft SYS-10 --auto-update    (auto-update mode)
/goal-builder:edit-draft SYS-10                  (normal mode - requires approval)
```

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

# Initialize version tracking (current Linear content is version 1)
echo "1" > .tmp/goal-version.txt

# Save the initial loaded content as version 1
cp .tmp/goal-draft.md .tmp/goal-draft-v1.md
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

### 4. Iterative Refinement Process with Version Management

**CRITICAL WORKFLOW**:
1. Listen to user's requested changes
2. **BEFORE editing**: Get current version number
3. Edit the file directly using Edit tool
4. **AFTER editing**: Save new version and show diff
5. Ask for more feedback
6. Continue until user explicitly says: "approved", "looks good", "update it", or similar
7. DO NOT proceed to Linear until user gives final approval

**Version Management During Iteration:**

When user provides feedback for changes:

**🚨 CRITICAL: Use SEPARATE Bash commands, NOT chained commands!**

Chaining all steps with && causes command truncation and the diff step gets lost. Execute as separate Bash tool calls:

```bash
# Step 1: Get current version and create next version file
VERSION=$(cat .tmp/goal-version.txt) && NEXT=$((VERSION + 1)) && cp .tmp/goal-draft.md .tmp/goal-draft-v${NEXT}.md && echo "$NEXT" > .tmp/goal-version.txt && echo "Created version $NEXT"
```

Then IMMEDIATELY run a SEPARATE Bash command:

```bash
# Step 2: 🔴 CRITICAL: Create diff file (MUST be separate command!)
VERSION=$(cat .tmp/goal-version.txt) && PREV=$((VERSION - 1)) && diff -u .tmp/goal-draft-v${PREV}.md .tmp/goal-draft-v${VERSION}.md > .tmp/goal-draft-v${PREV}-to-v${VERSION}.diff && echo "✅ Diff created: goal-draft-v${PREV}-to-v${VERSION}.diff"
```

Then run ANOTHER separate Bash command to show the diff:

```bash
# Step 3: Show what changed
VERSION=$(cat .tmp/goal-version.txt) && PREV=$((VERSION - 1)) && echo "" && echo "📝 Changes from v${PREV} to v${VERSION}:" && echo "📄 Diff saved to: .tmp/goal-draft-v${PREV}-to-v${VERSION}.diff" && echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" && cat .tmp/goal-draft-v${PREV}-to-v${VERSION}.diff && echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

**Why separate commands:**
- Long chained commands get truncated by the Bash tool
- The diff creation step was getting cut off, causing missing diff files
- Three separate Bash calls ensures each step completes successfully

**Workflow:**
1. Edit .tmp/goal-draft.md using Edit tool based on user feedback
2. Run first Bash command to create version file and increment counter
3. Run second Bash command to create diff file (NEVER skip this!)
4. Run third Bash command to display the diff
5. Ask for more feedback or wait for approval

**Why this matters:**
- ✅ User can see EXACTLY what changed after each edit
- ✅ All versions saved in `.tmp/goal-draft-v1.md`, `v2.md`, `v3.md`...
- ✅ **Automatic diff files created**: `.tmp/goal-draft-v1-to-v2.diff`, `v2-to-v3.diff`...
- ✅ Diffs created for ALL changes (user-requested OR agent-initiated)
- ✅ User can request specific version diffs: `diff -u .tmp/goal-draft-v2.md .tmp/goal-draft-v5.md > .tmp/goal-draft-v2-to-v5.diff`
- ✅ Provides full observability during iteration
- ✅ All diffs saved for review at any time

Example interaction:
- User: "Add more detail about the voice activation system"
- You: Edit `.tmp/goal-draft.md` to add voice activation details
- You: Show diff from v1 to v2
- User: "Change the success criteria to be more specific"
- You: Edit `.tmp/goal-draft.md` to update success criteria
- You: Show diff from v2 to v3
- User: "Perfect, update it in Linear"
- You: NOW proceed to update in Linear

### 5. Update Ticket in Linear (ONLY AFTER APPROVAL)

**🚨 CRITICAL: APPROVAL WORKFLOW 🚨**

**Check the arguments you received at the top of this command:**
- If `--auto-update` flag IS present → AUTO-UPDATE MODE (skip to update)
- If `--auto-update` flag is NOT present → NORMAL MODE (get approval first)

**NORMAL MODE (no --auto-update flag):**

Wait for explicit user approval with phrases like:
- "approved"
- "update it"
- "looks good"
- "yes"
- "go ahead"
- "update to Linear"

**NEVER push to Linear if:**
- You think the user "probably wants" the update
- It's a "small fix" or "formatting change"
- You're "testing" if something works
- You're in "diagnostic mode"

**You CAN make edits proactively:**
- ✅ Make changes to `.tmp/goal-draft.md` if you think they're needed (e.g., fixing YAML, formatting, typos)
- ✅ Create new versions and diffs to show what changed
- ✅ Explain what you changed and why
- ❌ But NEVER push to Linear until user explicitly approves

**THE RULE (NORMAL MODE ONLY)**: Wait for the ACTUAL USER to say approval words before pushing to Linear. NO EXCEPTIONS.

**⚠️ IMPORTANT: The above strict approval rules apply to NORMAL MODE only.**

In AUTO-UPDATE MODE (when user explicitly requests it), proceeding without approval is the INTENDED behavior.

**AUTO-UPDATE MODE (--auto-update flag present):**

Proceed to update in Linear immediately (99% of cases):
- ✅ Still show what you're about to do for transparency
- ✅ State: "🔥 Auto-update mode detected. Updating to Linear immediately..."
- ✅ Skip waiting for approval
- ✅ Archive system still preserves all versions/diffs

**However, even in AUTO-UPDATE MODE:**
- If you detect inconsistency/confusion in the request, you MAY still ask for clarification
- Example: "The request asks to add details about OAuth, but there's no mention of authentication in the goal. Should I add an authentication section first?"
- If you ask for clarification, Claude Code will relay the question to the user

**🔄 MID-WORKFLOW SWITCHING:**

Even if you start in NORMAL MODE (no --auto-update flag), you can switch to AUTO-UPDATE MODE mid-session:

**How it works:**
- You start in NORMAL MODE, asking for approval
- User approves a change
- Later, user tells Claude Code: "don't ask me again" or similar
- Claude Code sends: "SWITCH TO AUTO-UPDATE MODE: Skip approval for remaining changes."
- You acknowledge and switch to auto-update mode for rest of session

**How the switch works:**
- When you receive "SWITCH TO AUTO-UPDATE MODE: [message]" signal, acknowledge and switch behavior
- This signal indicates the user has explicitly requested to skip future approvals
- The switch lasts for the entire session (until Linear update completes)

**🚨 CRITICAL: AUTO-UPDATE MODE NEVER DIRECTLY UPDATES WITHOUT ACKNOWLEDGMENT 🚨**

Even in AUTO-UPDATE MODE, you MUST follow this sequence:

**WHY THIS MATTERS:**
After switching to auto-update mode, the user typically provides ONE MORE instruction with final changes (e.g., "add examples section and update in Linear"). You must:
1. ✅ Acknowledge: "🔥 Auto-update mode active. I'll [make changes] and update to Linear immediately."
2. ✅ Make the requested changes to `.tmp/goal-draft.md`
3. ✅ Create new version and show the diff
4. ✅ **THEN** clearly state: "🔥 Auto-update mode active. Updating to Linear immediately..."
5. ✅ **ONLY THEN** execute the `update_goal.py` script

**The acknowledgment-then-execute pattern is MANDATORY because:**
- The final instruction often includes changes to make before updating
- You must complete those changes first
- You must announce the action before executing it
- ❌ NEVER execute the update script without first announcing the action
- ❌ NEVER skip making the requested changes before updating

```bash
# Update the Linear goal with the new draft content
python .claude/scripts/goal-builder/update_goal.py \
  --goal-id "SYS-8" \
  --draft-file ".tmp/goal-draft.md"

# After successful update, archive all draft files for audit trail
if [ $? -eq 0 ]; then
  TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
  GOAL_ID="SYS-8"  # Use actual goal ID from command
  ARCHIVE_DIR=".tmp/archives/${GOAL_ID}/${TIMESTAMP}"

  mkdir -p "$ARCHIVE_DIR"
  mv .tmp/goal-draft*.md .tmp/goal-draft*.diff .tmp/goal-version.txt "$ARCHIVE_DIR/" 2>/dev/null || true

  echo "✅ Updated goal in Linear"
  echo "📦 Session archived to: $ARCHIVE_DIR"
  echo "📄 Review changes: ls -la $ARCHIVE_DIR"
  echo "📊 View diffs: cat $ARCHIVE_DIR/*.diff"
fi
```

**Archive System Benefits:**
- ✅ Complete audit trail of all changes
- ✅ Works for both normal and auto-update workflows
- ✅ Organized by goal ID and timestamp
- ✅ Can review any past session
- ✅ Diffs and versions never lost

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

## Code Block Formatting

**When writing example interactions in goal tickets, you MUST use ```text language specifier:**

```text
User: "Example command"
System: "Example response"
```

**WHY**: Code blocks with `Key: value` patterns (User:, API:, Response:) trigger YAML auto-detection in Linear without explicit language specifiers. Using ```text prevents this and ensures proper "copy as markdown" functionality. **This is the proven solution.**
