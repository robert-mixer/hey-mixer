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

### Step 2: Iterative Refinement

**Common refinement requests:**

- "Can you add MFA to the requirements?"
- "Let's specify the JWT expiration times"
- "Include migration from the old system"
- "Add performance requirements"

**Response approach:**
```
Great suggestion! I'll add MFA to the requirements. Here's the updated version:

[Show ONLY the changed section initially, then full draft if requested]
```

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
  --draft-file "/tmp/goal-draft.md" \
  --issues "12,15,18" \
  --status "draft"
```

Expected output:
```
✅ Goal ticket created successfully!
📎 Linear URL: https://linear.app/workspace/issue/TEAM-123
🏷️ Labels: goal
📊 Status: draft
🔗 Linked issues: #12, #15, #18
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

### DON'T:
- ❌ Auto-generate generic content
- ❌ Create with status="todo"
- ❌ Skip the review phase
- ❌ Combine unrelated issues
- ❌ Make goals too large or vague

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

#### Step 3: Iterative Refinement

Use the **Edit tool** to make precise changes:
- User provides specific change
- Apply edit to `.tmp/goal-draft.md`
- Show updated section
- Continue until user approves

**Example exchange:**
```
User: "Add OAuth support to requirements"

Agent: "I'll add OAuth to the requirements section:

## Requirements
- User registration with email validation
- JWT-based authentication
- **OAuth 2.0 integration (Google, GitHub)**  ← NEW
- Password reset via email
- Rate limiting

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
```

**Expected output:**
```
✅ Goal SYS-8 updated successfully!
📎 Linear URL: https://linear.app/workspace/issue/SYS-8
📊 Status: Draft (unchanged)
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
| **Save Command** | `create_goal_from_draft.py` | `update_goal.py` |
| **GitHub Action** | Close issues | None |
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