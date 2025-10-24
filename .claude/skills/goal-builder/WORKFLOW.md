# Goal Builder Detailed Workflow

This document covers two main workflows:
1. **Creating New Goals from GitHub Issues**
2. **Editing Existing Draft Goals in Linear**

---

## WORKFLOW A: Creating New Goals from GitHub Issues

### Phase 1: Discovery and Analysis

### Step 1: Assess Current Issues
```bash
# List all open issues (shows 200-char previews for discovery)
python .claude/scripts/goal-builder/list_issues.py

# Load specific issue's FULL content when selected
python .claude/scripts/goal-builder/load_issue.py --issue-number 11
```

**What to look for:**
- Natural groupings by feature area
- Dependencies between issues
- Quick wins vs. complex implementations
- Security or performance critical items

**Note**: `list_issues.py` shows 200-char previews for browsing. Once you select an issue to work with, use `load_issue.py` to see the complete content.

### Step 2: Suggest Groupings

Present logical groupings to the user:

```
Based on your open issues, I see three potential goals:

**Authentication System** (High Priority)
- #12: Add login form (UI)
- #15: JWT implementation (Backend)
- #18: Password reset (Feature)
These form a complete auth solution.

**Performance Optimization** (Medium Priority)
- #23: Database query optimization
- #27: Caching layer
These work together to improve response times.

**UI Improvements** (Lower Priority)
- #31: Dashboard redesign
- #33: Mobile responsiveness
Stand-alone UI enhancements.

Which would you like to tackle first?
```

## Phase 2: Interactive Drafting

### Step 1: Initial Draft

Start with a meaningful draft based on the selected issues:

```markdown
Here's my initial draft for the Authentication System goal:

# User Authentication System

Build a secure, modern authentication system that provides seamless user access management with industry-standard security practices.

## Requirements

- **User Registration**: Email-based signup with validation
- **Secure Login**: JWT-based authentication with refresh tokens
- **Session Management**: Persistent sessions with configurable timeout
- **Password Recovery**: Email-based reset flow with secure tokens
- **Security Features**: Rate limiting, CSRF protection, secure password hashing

[Continue with full draft...]

What would you like me to adjust?
```

**IMPORTANT: Consider Examples Section**
For goals involving user interaction, APIs, voice commands, conversational interfaces, or workflows, ALWAYS include an "Examples" section with 2-10 concrete scenarios showing expected behavior. This dramatically improves clarity for plan builders and module builders.

### Step 2: Iterative Refinement with Version Management

**Common refinement requests:**

- "Can you add MFA to the requirements?"
- "Let's specify the JWT expiration times"
- "Include migration from the old system"
- "Add performance requirements"

**Response approach with version tracking:**
```bash
# Before editing: Get current version
VERSION=$(cat .tmp/goal-version.txt)
NEXT=$((VERSION + 1))

# Make the edit to .tmp/goal-draft.md
Edit(.tmp/goal-draft.md) - Add MFA requirement

# After editing: Save version and CREATE DIFF FILE AUTOMATICALLY
cp .tmp/goal-draft.md .tmp/goal-draft-v${NEXT}.md
echo "$NEXT" > .tmp/goal-version.txt

# 🔴 CRITICAL: ALWAYS create diff file between consecutive versions
# This MUST happen for ALL version changes, whether:
# - User-requested (user asks for changes)
# - Agent-initiated (you fix formatting, YAML issues, spelling, etc.)
# IT DOESN'T MATTER WHO INITIATED THE CHANGE - ALWAYS CREATE THE DIFF!
diff -u .tmp/goal-draft-v${VERSION}.md .tmp/goal-draft-v${NEXT}.md > .tmp/goal-draft-v${VERSION}-to-v${NEXT}.diff

# Display what changed
echo "📝 Changes from v${VERSION} to v${NEXT}:"
echo "📄 Diff saved to: .tmp/goal-draft-v${VERSION}-to-v${NEXT}.diff"
cat .tmp/goal-draft-v${VERSION}-to-v${NEXT}.diff
```

**Why Version Management with Automatic Diffs:**
- ✅ User sees EXACT changes after each edit
- ✅ Full history in `.tmp/goal-draft-v1.md`, `v2.md`, `v3.md`...
- ✅ **Automatic diff files**: `.tmp/goal-draft-v1-to-v2.diff`, `v2-to-v3.diff`...
- ✅ Diffs created for ALL changes (user-requested OR agent-initiated)
- ✅ Can request specific version diffs on demand: `diff -u .tmp/goal-draft-v2.md .tmp/goal-draft-v5.md > .tmp/goal-draft-v2-to-v5.diff`
- ✅ Complete observability during iteration
- ✅ All diffs saved for review at any time

### Step 3: Final Approval

```
Here's the final version of our goal ticket:

[Show complete, formatted draft]

This looks perfect to me! Should I create this goal ticket in Linear now?
```

## Phase 3: Creation and Cleanup

### Step 1: Save Draft

```bash
# Save the exact content to a temporary file
cat > /tmp/goal-draft.md << 'EOF'
[Paste the EXACT markdown content that was approved]
EOF

echo "✅ Draft saved to /tmp/goal-draft.md"
```

### Step 2: Create Linear Ticket

```bash
python .claude/scripts/goal-builder/create_goal_from_draft.py \
  --draft-file ".tmp/goal-draft.md" \
  --issues "12,15,18" \
  --status "draft"

# After successful creation, clean up all draft files
if [ $? -eq 0 ]; then
  rm -f .tmp/goal-draft*.md .tmp/goal-draft*.diff .tmp/goal-version.txt
  echo "✅ Cleaned up draft versions, diffs, and version tracker"
fi
```

Expected output:
```
✅ Goal ticket created successfully!
📎 Linear URL: https://linear.app/workspace/issue/TEAM-123
🏷️ Labels: goal
📊 Status: draft
🔗 Linked issues: #12, #15, #18
✅ Cleaned up draft versions
```

### Step 3: Close GitHub Issues

```bash
python .claude/scripts/goal-builder/close_issues.py --issues "12,15,18" \
  --comment "Incorporated into Linear goal: User Authentication System (TEAM-123)"
```

### Step 4: Explain Next Steps

```
Perfect! Your goal has been created successfully. Here's what happens next:

✅ **Created**: "User Authentication System" goal in Linear (status: draft)
✅ **Archived**: GitHub issues #12, #15, #18 have been closed
📝 **Your Action**: Review the goal in Linear
🎯 **When Ready**: Change status from "draft" to "todo"
🚀 **Next Phase**: Plan Builder will create implementation plan when status is "todo"

The goal is currently in DRAFT status, giving you time to:
- Review and edit in Linear if needed
- Add any additional context
- Attach relevant documents
- Set priority and estimates

When you're satisfied, change the status to "todo" and the Plan Builder can create a detailed implementation plan.
```

## Phase 4: Handoff Points

### To Plan Builder
When goal status changes to "todo", the Plan Builder will:
1. Read the goal requirements
2. Create detailed implementation plan
3. Break down into concrete tasks
4. Define module structure

### Status Transitions
```
draft → todo: User is ready for planning (manual)
todo → doing: Plan created, implementation starting (automatic)
doing → done: Module implemented and tested (automatic)
```

## Best Practices

### DO:
- ✅ Write actual content, not templates
- ✅ Include all context in the goal
- ✅ Get explicit approval before creating
- ✅ Explain the workflow clearly
- ✅ Keep goals achievable (1-2 sprints)
- ✅ **Include "Examples" section for interactive features** - Voice commands, APIs, chatbots, CLI tools, workflows, or any system where concrete examples clarify behavior
- ✅ Show 2-10 realistic interaction scenarios in Examples section
- ✅ **Use ```text language specifier for ALL example code blocks** - This prevents Linear from misinterpreting content as YAML (proven solution)
- ✅ **ALWAYS wait for explicit user approval before updating Linear/GitHub (NORMAL MODE)** - Even for small fixes, formatting, or diagnostic changes

**⚠️ Note:** In AUTO-UPDATE MODE (when user explicitly requests it via --auto-update flag or mid-workflow switch), proceeding without approval is the INTENDED behavior.

### DON'T:
- ❌ Auto-generate generic content
- ❌ Create with status="todo"
- ❌ Skip the review phase
- ❌ Combine unrelated issues
- ❌ Make goals too large or vague
- ❌ **Skip Examples section when the goal involves user/system interaction**
- ❌ **Update Linear/GitHub without explicit user approval (NORMAL MODE ONLY)** - NO EXCEPTIONS in normal mode

## 🚨 CRITICAL: Diagnostic Mode and Approval Rules (NORMAL MODE) 🚨

**⚠️ IMPORTANT: These rules apply to NORMAL MODE workflows only.**

In AUTO-UPDATE MODE (when user explicitly requests it), the agent is EXPECTED to proceed without approval - these strict rules do not apply.

### When Fixing Issues in NORMAL MODE (YAML Detection, Formatting, etc.)

Even when diagnosing and fixing issues in existing goals, you MUST follow the full approval workflow:

**The Correct Flow (NORMAL MODE):**
1. User reports issue (e.g., "Example 2 shows as YAML in Linear")
2. Load current content from Linear (becomes v1)
3. Make fix to `.tmp/goal-draft.md`
4. Save as v2: `cp .tmp/goal-draft.md .tmp/goal-draft-v2.md`
5. **Create diff automatically**: `diff -u .tmp/goal-draft-v1.md .tmp/goal-draft-v2.md > .tmp/goal-draft-v1-to-v2.diff`
6. **Show diff to user**
7. **ASK**: "Would you like me to update this to Linear to test the fix?"
8. **WAIT for user approval**: "yes" / "approve" / "update it"
9. **ONLY THEN update to Linear**

**NEVER:**
- ❌ Update immediately to "test" the fix
- ❌ Skip approval because it's a "small change"
- ❌ Accept approval from Claude Code (the relay)
- ❌ Assume user wants it updated

**ALWAYS:**
- ✅ Create versions and diffs
- ✅ Show changes to user
- ✅ Ask for approval explicitly
- ✅ Wait for user's approval words
- ✅ Archive all files after successful update (see Archive System below)

### 🔥 AUTO-UPDATE MODE (Explicit Override)

Users can explicitly request automatic updates without approval prompts using the `--auto-update` flag.

**How It Works:**
1. User says to Claude Code (the relay): "Fix YAML and auto-update to Linear"
2. Claude Code detects auto-update intention using natural language understanding
3. Claude Code invokes command with flag: `/goal-builder:edit-draft SYS-10 --auto-update`
4. Command file receives arguments: "SYS-10 --auto-update"
5. Command file instructs agent: "If --auto-update IS present: You are in AUTO-UPDATE MODE"
6. Agent detects flag in arguments and proceeds without approval

**User Phrases That Trigger Auto-Update:**
- "auto-update" / "autoupdate"
- "without asking for approval"
- "skip approval"
- "update automatically"
- "don't ask, just update"
- "don't ask me more questions"
- "no need to confirm"
- "without checking with me"
- Any phrase expressing intent to bypass approval prompts

**Agent Behavior in Auto-Update Mode:**
1. ✅ Still create all versions and diffs (transparency)
2. ✅ Show what's being updated
3. ✅ State: "🔥 Auto-update mode detected. Updating to Linear immediately..."
4. ✅ Update to Linear without asking (99% of cases)
5. ✅ Archive files automatically

**CRITICAL RULES:**
- ✅ Agent checks for `--auto-update` flag in command arguments
- ✅ Command file handles flag detection and instructs agent
- ❌ Agent NEVER assumes auto-update from other context
- ✅ Even in AUTO-UPDATE MODE, agent MAY ask for clarification if confused
- ✅ Default is ALWAYS to ask for approval (when no flag present)

### 📦 Archive System (Complete Audit Trail)

**ALL successful Linear updates are automatically archived** - regardless of workflow mode.

**Archive Structure:**
```
.tmp/archives/
  └── SYS-10/
      ├── 20251022-143022/
      │   ├── goal-draft-v1.md
      │   ├── goal-draft-v2.md
      │   ├── goal-draft-v1-to-v2.diff
      │   └── goal-version.txt
      ├── 20251022-151530/
      │   ├── goal-draft-v1.md
      │   ├── goal-draft-v2.md
      │   ├── goal-draft-v3.md
      │   ├── goal-draft-v1-to-v2.diff
      │   ├── goal-draft-v2-to-v3.diff
      │   └── goal-version.txt
      └── ...
```

**Benefits:**
- ✅ Never lose any change history
- ✅ Review what happened in any session
- ✅ Compare versions across sessions
- ✅ Audit trail for all updates
- ✅ Works for both normal and auto-update modes

**Review Archives:**
```bash
# List all sessions for a goal
ls -la .tmp/archives/SYS-10/

# Review specific session
ls -la .tmp/archives/SYS-10/20251022-143022/

# View diffs from a session
cat .tmp/archives/SYS-10/20251022-143022/*.diff

# Compare versions
diff .tmp/archives/SYS-10/20251022-143022/goal-draft-v1.md \
     .tmp/archives/SYS-10/20251022-151530/goal-draft-v1.md
```

## Troubleshooting

### Issue: "Goal too large"
**Solution**: Split into multiple smaller goals with clear boundaries

### Issue: "Missing context"
**Solution**: Add Technical Considerations or Dependencies sections

### Issue: "Unclear requirements"
**Solution**: Make requirements specific and measurable

### Issue: "No module target"
**Solution**: Define where the code will live in the codebase

## Conversation Starters (Creating New Goals)

Use these prompts to guide the conversation:

- "I see you have [N] open issues. Would you like me to suggest some logical groupings?"
- "These [N] issues seem related to [topic]. Should we create a goal for them?"
- "Let me draft a goal ticket for [feature]. We can refine it together."
- "What aspects of this goal are most important to you?"
- "Should we add any technical constraints or requirements?"
- "How would you like to handle [specific consideration]?"
- "This draft captures what we discussed. What would you like to adjust?"

---

## WORKFLOW B: Editing Existing Draft Goals

### Phase 1: Discovery

#### Step 1: List Draft Goals
```bash
# List all draft goals (shows 200-char previews for discovery)
python .claude/scripts/goal-builder/list_drafts.py
```

**Output shows:**
- Goal identifier (e.g., SYS-8)
- Title
- Current status (always "Draft")
- Linear URL
- Description preview (200 chars)

**Conversation starter:**
```
You currently have [N] draft goals in Linear:

1. **SYS-8**: Voice-Driven Mixer Assistant
   Status: Draft
   Preview: Build a conversational AI assistant...

2. **SYS-9**: Authentication System
   Status: Draft
   Preview: Implement secure user authentication...

Which draft would you like to edit?
```

### Phase 2: Load and Modify Draft

#### Step 1: Load Current Content

When user selects a goal to edit (e.g., "edit SYS-8" or "1"):

```bash
# Create temp directory
mkdir -p .tmp

# Load the FULL goal description from Linear directly to draft file
python .claude/scripts/goal-builder/load_goal.py \
  --goal-id "SYS-8" \
  --description-only > .tmp/goal-draft.md
```

**Why use load_goal.py:**
- `list_drafts.py` only shows 200-char previews
- `load_goal.py` fetches the complete description from Linear
- The `--description-only` flag outputs just the markdown (perfect for piping)
- This gives you the full current content to edit

#### Step 2: Interactive Editing

**Present current content:**
```
Here's the current content of SYS-8:

[Display current markdown content]

What changes would you like to make?
```

**Common modification requests:**
- "Add a new requirement for [feature]"
- "Change the target module to [new-path]"
- "Update the success criteria"
- "Add more detail to [section]"
- "Remove the requirement about [x]"

**Response approach:**
```
I'll update [section] with that change. Here's the modified version:

[Show the updated section]

Would you like any other changes, or is this ready to update in Linear?
```

#### Step 3: Iterative Refinement with Version Management

Use the **Edit tool** to make precise changes with version tracking:

**Process for each edit:**
```bash
# Before editing: Get current version
VERSION=$(cat .tmp/goal-version.txt)
NEXT=$((VERSION + 1))

# Make the edit to .tmp/goal-draft.md
Edit(.tmp/goal-draft.md) - Apply user's requested change

# After editing: Save version and CREATE DIFF FILE AUTOMATICALLY
cp .tmp/goal-draft.md .tmp/goal-draft-v${NEXT}.md
echo "$NEXT" > .tmp/goal-version.txt

# 🔴 CRITICAL: ALWAYS create diff file between consecutive versions
# This MUST happen for ALL version changes, whether:
# - User-requested (user asks for changes)
# - Agent-initiated (you fix formatting, YAML issues, spelling, etc.)
# IT DOESN'T MATTER WHO INITIATED THE CHANGE - ALWAYS CREATE THE DIFF!
diff -u .tmp/goal-draft-v${VERSION}.md .tmp/goal-draft-v${NEXT}.md > .tmp/goal-draft-v${VERSION}-to-v${NEXT}.diff

# Display what changed
echo "📝 Changes from v${VERSION} to v${NEXT}:"
echo "📄 Diff saved to: .tmp/goal-draft-v${VERSION}-to-v${NEXT}.diff"
cat .tmp/goal-draft-v${VERSION}-to-v${NEXT}.diff
```

**Why Version Management with Automatic Diffs:**
- ✅ User sees EXACT changes after each edit
- ✅ Full history in `.tmp/goal-draft-v1.md`, `v2.md`, `v3.md`...
- ✅ **Automatic diff files**: `.tmp/goal-draft-v1-to-v2.diff`, `v2-to-v3.diff`...
- ✅ Diffs created for ALL changes (user-requested OR agent-initiated)
- ✅ Can request specific version diffs on demand
- ✅ Complete observability during iteration
- ✅ All diffs saved for review at any time

**Example exchange:**
```
User: "Add OAuth support to requirements"

Agent: [Edits file, saves v2, shows diff]
"📝 Changes from v1 to v2:
+- **OAuth 2.0 integration (Google, GitHub)**

Anything else?"

User: "Perfect, update it in Linear"
```

### Phase 3: Update in Linear

#### Step 1: Get Final Approval
```
Here's the final updated version:

[Show complete markdown content]

Ready to update SYS-8 in Linear with these changes?
```

#### Step 2: Execute Update
```bash
python .claude/scripts/goal-builder/update_goal.py \
  --goal-id "SYS-8" \
  --draft-file ".tmp/goal-draft.md"

# After successful update, clean up all draft files
if [ $? -eq 0 ]; then
  rm -f .tmp/goal-draft*.md .tmp/goal-draft*.diff .tmp/goal-version.txt
  echo "✅ Cleaned up draft versions, diffs, and version tracker"
fi
```

**Expected output:**
```
✅ Goal SYS-8 updated successfully!
📎 Linear URL: https://linear.app/workspace/issue/SYS-8
📊 Status: Draft (unchanged)
✅ Cleaned up draft versions
```

#### Step 3: Explain Status
```
Perfect! Your goal has been updated in Linear.

✅ **Updated**: SYS-8 with your latest changes
📝 **Status**: Still in "Draft" (you can review and adjust)
🎯 **When Ready**: Change status from "draft" to "todo"
🚀 **Next Phase**: Plan Builder creates implementation plan when status is "todo"

The goal remains in DRAFT status, so you can:
- Continue editing if needed
- Review in Linear one more time
- Make additional adjustments
- Set priority and estimates

When you're completely satisfied, change the status to "todo" and the Plan Builder will create a detailed implementation plan.
```

### Phase 4: Multiple Edits

Users can edit the same draft multiple times:

```
Would you like to:
1. Edit another draft goal
2. Make more changes to SYS-8
3. Create a new goal from GitHub issues
```

### Workflow Comparison

| Aspect | Creating New Goal | Editing Draft Goal |
|--------|------------------|-------------------|
| **Starting Point** | GitHub issues | Linear draft goals |
| **List Command** | `list_issues.py` (200-char preview) | `list_drafts.py` (200-char preview) |
| **Load Command** | `load_issue.py` (full body) | `load_goal.py` (full description) |
| **Source Content** | Draft from full issue | Load from Linear |
| **Working File** | `.tmp/goal-draft.md` | `.tmp/goal-draft.md` |
| **Version Files** | `.tmp/goal-draft-v1.md`, `v2.md`... | `.tmp/goal-draft-v1.md`, `v2.md`... |
| **Version Tracker** | `.tmp/goal-version.txt` | `.tmp/goal-version.txt` |
| **Save Command** | `create_goal_from_draft.py` | `update_goal.py` |
| **GitHub Action** | Close issues | None |
| **Cleanup** | After creation success | After update success |
| **Final Status** | Draft | Draft (unchanged) |

### Best Practices (Editing)

#### DO:
- ✅ Show current content before asking for changes
- ✅ Use Edit tool for precise modifications
- ✅ Confirm changes before updating Linear
- ✅ Preserve goal status as "draft"
- ✅ Allow multiple edit rounds

#### DON'T:
- ❌ Change status automatically
- ❌ Make assumptions about desired changes
- ❌ Skip showing the current content
- ❌ Update without explicit approval
- ❌ Edit goals that are not in "draft" status

### Troubleshooting (Editing)

**Issue: "Goal not found"**
**Solution**: Verify the goal ID is correct and the goal exists in Linear

**Issue: "Goal is not a draft"**
**Solution**: Only draft goals can be edited through this workflow. Goals in "todo", "doing", or "done" should be edited directly in Linear.

**Issue: "Lost changes"**
**Solution**: Working file is `.tmp/goal-draft.md` - can always review before updating

**Issue: "Want to revert changes"**
**Solution**: Can re-run edit command to reload original content from Linear

### Conversation Starters (Editing Drafts)

- "You have [N] draft goals. Would you like to see them?"
- "Which draft would you like to edit?"
- "Here's the current content of [GOAL-ID]. What changes should we make?"
- "I've updated [section]. Does this look right?"
- "Would you like to make any other changes before updating Linear?"
- "The goal has been updated in Linear. Want to edit another draft or make more changes to this one?"