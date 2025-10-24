---
description: Interactively create a Linear goal ticket from selected GitHub issues
allowed-tools: Bash(python:.claude/scripts/goal-builder/*), Write, Read
argument-hint: [issue-numbers] [--auto-update]
disable-model-invocation: false
---

# Create Goal Ticket

Work with the user to create a Linear goal ticket from GitHub issues.

## 🔥 Arguments Received

**Arguments:** $ARGUMENTS

**AUTO-UPDATE MODE DETECTION:**

Check if the arguments contain the `--auto-update` flag:

- **If `--auto-update` IS present:** You are in AUTO-UPDATE MODE
  - ✅ Skip approval prompts and create in Linear immediately (99% of cases)
  - ✅ Still show what you're doing for transparency
  - ✅ State: "🔥 Auto-update mode detected. Creating in Linear immediately..."
  - ✅ Exception: If you detect inconsistency/confusion, ask for clarification

- **If `--auto-update` is NOT present (default):** Follow normal approval workflow
  - ✅ Draft the goal interactively
  - ✅ Ask "Should I create this in Linear?" and wait for user approval
  - ✅ Only create after explicit approval

**Command Examples:**
```
/goal-builder:create-goal 11 --auto-update          (auto-update mode)
/goal-builder:create-goal 11,12,15 --auto-update    (auto-update mode)
/goal-builder:create-goal 11                        (normal mode - requires approval)
```

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

# Initialize version tracking (version 1 will be the initial draft)
echo "1" > .tmp/goal-version.txt
```

Then use the **Write tool** to create the file:
```
Write(.tmp/goal-draft.md) with the complete draft content
```

**After writing the initial draft, save it as version 1:**
```bash
cp .tmp/goal-draft.md .tmp/goal-draft-v1.md
```

**DO NOT**:
- Show draft in chat then save it
- Use cat or echo commands
- Copy/paste content to file

**DO**:
- Write directly to `.tmp/goal-draft.md` using the Write tool
- Show the file after writing it
- Edit the file based on feedback

### 4. Iterative Refinement Process with Version Management

**CRITICAL WORKFLOW**:
1. Show the saved draft to the user
2. Ask: "Would you like to make any changes to this draft?"
3. If user provides feedback:
   - **BEFORE editing**: Get current version number
   - Edit the file directly using Edit tool
   - **AFTER editing**: Save new version and show diff
4. Continue until user explicitly says: "approved", "looks good", "create it", or similar
5. DO NOT proceed to Linear until user gives final approval

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
- User: "Add more detail about error handling"
- You: Edit `.tmp/goal-draft.md` to add error handling details
- You: Show diff from v1 to v2
- User: "Change the module name to mixer-assistant"
- You: Edit `.tmp/goal-draft.md` to update module name
- You: Show diff from v2 to v3
- User: "Perfect, create it"
- You: NOW proceed to create in Linear

### 5. Create Ticket with Exact Draft Content (ONLY AFTER APPROVAL)

**🚨 CRITICAL: APPROVAL WORKFLOW 🚨**

**Check the arguments you received at the top of this command:**
- If `--auto-update` flag IS present → AUTO-UPDATE MODE (skip to creation)
- If `--auto-update` flag is NOT present → NORMAL MODE (get approval first)

**NORMAL MODE (no --auto-update flag):**

Wait for explicit user approval with phrases like:
- "approved"
- "create it"
- "looks good"
- "yes"
- "go ahead"
- "create in Linear"

**NEVER push to Linear if:**
- You think the user "probably wants" it created
- You're making "final tweaks"
- You assume approval based on context

**You CAN make edits proactively:**
- ✅ Make changes to `.tmp/goal-draft.md` if you think they're needed
- ✅ Create new versions and diffs to show what changed
- ✅ Explain what you changed and why
- ❌ But NEVER push to Linear until user explicitly approves

**THE RULE (NORMAL MODE ONLY)**: Wait for the ACTUAL USER to say approval words before pushing to Linear. NO EXCEPTIONS.

**⚠️ IMPORTANT: The above strict approval rules apply to NORMAL MODE only.**

In AUTO-UPDATE MODE (when user explicitly requests it), proceeding without approval is the INTENDED behavior.

**AUTO-UPDATE MODE (--auto-update flag present):**

Proceed to create in Linear immediately (99% of cases):
- ✅ Still show what you're about to do for transparency
- ✅ State: "🔥 Auto-update mode detected. Creating in Linear immediately..."
- ✅ Skip waiting for approval
- ✅ Archive system still preserves all versions/diffs

**However, even in AUTO-UPDATE MODE:**
- If you detect inconsistency/confusion in the request, you MAY still ask for clarification
- Example: "The request asks to create goal from issue #11, but issue #11 doesn't exist. Should I use issue #12 instead?"
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

```bash
# Create the Linear goal ticket with the draft content
python .claude/scripts/goal-builder/create_goal_from_draft.py \
  --draft-file ".tmp/goal-draft.md" \
  --issues "12,15,18" \
  --status "draft"

# After successful creation, archive all draft files for audit trail
if [ $? -eq 0 ]; then
  TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
  GOAL_ID=$(grep -oP 'TEAM-\d+|SYS-\d+' <<< "$OUTPUT" | head -1)  # Extract goal ID from output
  ARCHIVE_DIR=".tmp/archives/${GOAL_ID}/${TIMESTAMP}"

  mkdir -p "$ARCHIVE_DIR"
  mv .tmp/goal-draft*.md .tmp/goal-draft*.diff .tmp/goal-version.txt "$ARCHIVE_DIR/" 2>/dev/null || true

  echo "✅ Created goal in Linear"
  echo "📦 Session archived to: $ARCHIVE_DIR"
  echo "📄 Review changes: ls -la $ARCHIVE_DIR"
  echo "📊 View diffs: cat $ARCHIVE_DIR/*.diff"
fi
```

**Archive System Benefits:**
- ✅ Complete audit trail of all changes
- ✅ Works for both normal and auto-create workflows
- ✅ Organized by goal ID and timestamp
- ✅ Can review any past session
- ✅ Diffs and versions never lost

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

## Code Block Formatting

**When writing example interactions in goal tickets, you MUST use ```text language specifier:**

```text
User: "Example command"
System: "Example response"
```

**WHY**: Code blocks with `Key: value` patterns (User:, API:, Response:) trigger YAML auto-detection in Linear without explicit language specifiers. Using ```text prevents this and ensures proper "copy as markdown" functionality. **This is the proven solution.**
