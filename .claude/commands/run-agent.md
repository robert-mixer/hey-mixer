---
description: Complete guide for running and interacting with Mixer agents via tmux
argument-hint: [goal-builder|plan-builder|module-builder]
disable-model-invocation: false
---

# Run Agent - Complete Interaction Guide

Comprehensive guide for Claude Code to run and interact with Goal Builder, Plan Builder, or Module Builder agents through tmux sessions.

## Usage
Run with agent name: `goal-builder`, `plan-builder`, or `module-builder`

## 🔴 CRITICAL RULES - NEVER FORGET

### -2. ⚡ CHECK FOR AUTO-UPDATE MODE FIRST (BEFORE ANYTHING ELSE!)

**IMMEDIATELY CHECK: Does the user want to skip approval?**

**🚨 THE MOST COMMON PATTERN: "Do X and create/update/push"**

When user says: "Do X [and/then] [create/update/push to Linear]", they want AUTO-UPDATE MODE!

**Examples that TRIGGER auto-update mode:**
- ❌ **MISSED EXAMPLE:** "Remove the enumeration and push to Linear" → SWITCH TO AUTO-UPDATE
- "Add more details and create the goal" → SWITCH TO AUTO-UPDATE
- "Fix the YAML and update it" → SWITCH TO AUTO-UPDATE
- "Change the title then push it" → SWITCH TO AUTO-UPDATE
- "Let's do X and create/update to Linear" → SWITCH TO AUTO-UPDATE
- "Don't ask me again" / "Stop asking for approval" → SWITCH TO AUTO-UPDATE
- "No need to confirm" / "Just do it automatically" → SWITCH TO AUTO-UPDATE

**How to signal auto-update (mid-workflow):**
1. Send: "SWITCH TO AUTO-UPDATE MODE: User gave complete instruction including final action."
2. Then relay the actual instruction

**🔴 FAILURE TO DETECT THIS = USER FRUSTRATION!**

If you miss this pattern and ask for approval when user clearly said "do X and push", you've failed.

**Quick test - Check if ANY of these are true:**
1. Message includes BOTH an action AND final step (create/update/push)? → AUTO-UPDATE
2. Message says "don't ask me (again)" or similar? → AUTO-UPDATE
3. Message says "auto-update" / "skip approval" / "no need to confirm"? → AUTO-UPDATE
4. Otherwise → Use normal approval workflow

---

### -1. YOU ARE AN INTERMEDIARY, NOT THE AGENT! (ABSOLUTE HIGHEST PRIORITY!)
**🚨 CRITICAL: You (Claude Code) are NOT the agent. You are ONLY a relay between the user and the agent running in tmux.**

**YOU ABSOLUTELY CANNOT:**
- ❌ Run ANY Python scripts directly (e.g., NEVER run `python .claude/scripts/...`)
- ❌ Access Linear or GitHub APIs yourself
- ❌ Create tickets, close issues, or modify data
- ❌ Use the Read/Write/Edit tools on agent files
- ❌ Execute agent logic or workflows yourself

**YOU CAN ONLY:**
- ✅ Send messages to the agent in tmux (like a user would)
- ✅ Capture and relay agent responses back to the user
- ✅ Ask the user for confirmation when needed
- ✅ Guide the conversation between user and agent

**YOU ARE A PUPPET:** You act as the user's hands on the keyboard, typing into the tmux session. The AGENT does all the work, not you! If you try to do the agent's job, you're violating your core function.

### 0. ALWAYS TRANSLATE USER INTENT INTO SLASH COMMANDS (HIGHEST PRIORITY!)
**THIS IS THE #1 RULE: You MUST translate ALL user intent into the agent's slash commands, NOT generic text!**

#### Goal Builder Commands (MANDATORY USE):
- `/goal-builder:show-issues` - Display GitHub issues (NOT "show issues")
- `/goal-builder:show-drafts` - Display draft Linear goal tickets (NOT "show drafts")
- `/goal-builder:analyze-issues` - Analyze and group issues
- `/goal-builder:save-draft [filename]` - Save draft to file
- `/goal-builder:create-goal [issue-numbers]` - Create goal from issues
- `/goal-builder:edit-draft [goal-id]` - Edit an existing draft goal (NOT "edit draft")

#### Plan Builder Commands (MANDATORY USE):
- `/plan-builder:show-goals` - Display Linear goals with status="todo"
- `/plan-builder:analyze-goal [goal-id]` - Analyze a specific goal
- `/plan-builder:create-plan [goal-id]` - Create plan from goal

#### Module Builder Commands (MANDATORY USE):
- `/module-builder:show-plans` - Display Linear plans with status="todo"
- `/module-builder:load-plan [plan-id]` - Load and implement plan
- `/module-builder:mark-complete [plan-id]` - Mark plan/goal as done

**⚠️ CRITICAL ENFORCEMENT - YOU MUST TRANSLATE:**
- When user asks to "create a goal" → Use `/goal-builder:create-goal`
- When user asks to "show issues" → Use `/goal-builder:show-issues`
- When user asks to "show drafts" → Use `/goal-builder:show-drafts`
- When user asks to "edit a draft" → Use `/goal-builder:edit-draft`
- When user asks to "make a plan" → Use `/plan-builder:create-plan`
- **When user says "A" (after agent offered options A/B/C)** → Translate to the actual command!
- **When user says informal text** → Translate to the corresponding slash command!
- NEVER send generic text when a command exists for that action!

**🚨 TRANSLATION EXAMPLES - MANDATORY TO FOLLOW:**
```
Scenario 1: Agent offers "A) Create goal B) Read issue C) Create more issues"
User says: "A"
YOU MUST SEND: /goal-builder:create-goal 11 (NOT "A")

Scenario 2: User says "show me the issues"
YOU MUST SEND: /goal-builder:show-issues (NOT "show me the issues")

Scenario 3: User says "let's edit that draft goal"
YOU MUST SEND: /goal-builder:edit-draft SYS-123 (NOT "let's edit that draft goal")

Scenario 4: User says "yes, approved" (after draft shown)
YOU CAN SEND: "approved" (no slash command exists for approval)
```

**The rule is simple: IF a slash command exists for the user's intent, YOU MUST USE IT. ALWAYS.**

### 1. TWO-STEP COMMAND SENDING (CRITICAL!)
Claude agents require TWO SEPARATE tmux operations:
1. First: Send the prompt text WITHOUT C-m
2. Second: Send C-m in a SEPARATE command

```bash
# WRONG - Sending text and Enter together WILL NOT WORK
tmux send-keys -t session "Show me the issues" C-m

# CORRECT - Must be TWO SEPARATE COMMANDS
tmux send-keys -t session "Show me the issues"    # Step 1: Send text
tmux send-keys -t session C-m                      # Step 2: Send Enter

# Or if you prefer one line (but still two operations):
tmux send-keys -t session "Show me the issues" && tmux send-keys -t session C-m
```

**⚠️ CRITICAL: Claude agents wait for the FULL prompt before executing. If you send text+C-m together, the agent won't process it correctly!**

If agent seems stuck after sending a command, send C-m separately:
```bash
tmux send-keys -t session C-m
```

### 2. User Confirmation is MANDATORY
**ALWAYS confirm with user before proceeding at key points:**

#### For Goal Builder:
- After showing issues: "These are the issues found. Which one(s) should we create goals for?"
- Before drafting: "I'll draft a goal for issue #X. Any specific requirements?"
- After draft: "Here's what the agent drafted. Should we proceed or modify?"
- Before creating: "Ready to create this goal in Linear?"

#### For Plan Builder:
- After showing goals: "These goals are ready for planning. Which should we work on?"
- After analyzing: "The agent analyzed goal X. Should we create this plan?"
- Before finalizing: "Plan looks like [summary]. Create it?"

#### For Module Builder:
- After showing plans: "These plans are ready for implementation. Which one?"
- Before coding: "Agent will implement [feature]. Proceed?"
- After implementation: "Module created. Mark as complete?"

### 3. "ultrathink" Usage Rules

**✅ USE ultrathink for CREATIVE tasks:**
- Creating goals from issues
- Drafting implementation plans
- Designing solutions or architecture
- Writing comprehensive content
- Solving complex problems

**❌ DON'T use ultrathink for SIMPLE tasks:**
- Showing issues/goals/plans (just list/display)
- Running basic commands
- Status checks
- Simple queries
- Navigation

Example:
```bash
# Creative - USE ultrathink (TWO STEPS!)
tmux send-keys -t session "Draft a comprehensive goal for this authentication system. Include all technical requirements. ultrathink"
tmux send-keys -t session C-m

# Simple - NO ultrathink (TWO STEPS!)
tmux send-keys -t session "Show me the GitHub issues"
tmux send-keys -t session C-m
```

### 4. Strict Scope Management

**You CANNOT:**
- ❌ Create goals unrelated to GitHub issues
- ❌ Add major features not in the original issue
- ❌ Change the core purpose of any ticket
- ❌ Innovate without user permission

**You MUST:**
- ✅ Base all content on actual GitHub issues
- ✅ Stay within the defined scope
- ✅ Ask user before ANY deviation
- ✅ Maintain traceability to source

## 📋 STEP-BY-STEP WORKFLOW

### Phase 1: Setup Session
```bash
# Kill any existing session with same name
tmux kill-session -t $ARGUMENTS-session 2>/dev/null

# Create new session
tmux new-session -d -s $ARGUMENTS-session

# Launch the agent
tmux send-keys -t $ARGUMENTS-session "./mixer.sh $ARGUMENTS" C-m

# Wait for agent to start
sleep 5
```

### Phase 2: Initial Contact
```bash
# Send greeting to trigger startup message (TWO STEPS!)
tmux send-keys -t $ARGUMENTS-session "Hello"
tmux send-keys -t $ARGUMENTS-session C-m

# Wait for response
sleep 10

# Capture output
tmux capture-pane -t $ARGUMENTS-session -p | tail -30
```

### Phase 3: Agent-Specific Workflows

#### GOAL BUILDER Workflow
```bash
# NEW GOAL FROM GITHUB ISSUES:

# 1. Show issues using COMMAND (no ultrathink) - TWO STEPS!
tmux send-keys -t goal-builder-session "/goal-builder:show-issues"
tmux send-keys -t goal-builder-session C-m
sleep 10

# 2. CHECK WITH USER
"I found these issues: [list]
Which ones should we create goals for?
Should we combine any of them?"

# 3. After user selects issue(s) - USE CREATE-GOAL COMMAND! TWO STEPS!
tmux send-keys -t goal-builder-session "/goal-builder:create-goal X"
tmux send-keys -t goal-builder-session C-m
sleep 20

# 4. CHECK WITH USER
"The agent has written a draft to .tmp/goal-draft.md (v1)
Review the content. Any changes needed?"

# 5. The agent will iterate with you using Edit tool
# Each edit creates new version (v2, v3...) AND automatically creates diff files:
# - v1 → v2 creates .tmp/goal-draft-v1-to-v2.diff
# - v2 → v3 creates .tmp/goal-draft-v2-to-v3.diff
# - Agent displays each diff inline automatically
# If you ask "show diff v1 v4", agent creates that specific diff on demand
# After you approve, it will create in Linear and clean up all versions

# 6. Confirm completion
"Goal created successfully! Issue #X has been closed.
Draft versions, diffs, and version tracker cleaned up."

# EDIT EXISTING DRAFT GOAL:

# 1. Show draft goals using COMMAND - TWO STEPS!
tmux send-keys -t goal-builder-session "/goal-builder:show-drafts"
tmux send-keys -t goal-builder-session C-m
sleep 10

# 2. CHECK WITH USER
"I found these draft goals: [list]
Which one would you like to edit?"

# 3. After user selects goal - USE EDIT-DRAFT COMMAND! TWO STEPS!
tmux send-keys -t goal-builder-session "/goal-builder:edit-draft SYS-X"
tmux send-keys -t goal-builder-session C-m
sleep 15

# 4. The agent will load current content and save to .tmp/goal-draft.md (v1)
# CHECK WITH USER
"Here's the current content. What would you like to change?"

# 5. The agent will iterate with you using Edit tool
# Each edit creates new version (v2, v3...) AND automatically creates diff files:
# - v1 → v2 creates .tmp/goal-draft-v1-to-v2.diff
# - v2 → v3 creates .tmp/goal-draft-v2-to-v3.diff
# - Agent displays each diff inline automatically
# If you ask "show diff v1 v4", agent creates that specific diff on demand
# After you approve, it will update in Linear and clean up all versions

# 6. Confirm completion
"Goal updated successfully in Linear!
Draft versions, diffs, and version tracker cleaned up."
```

#### PLAN BUILDER Workflow
```bash
# 1. Show available goals using COMMAND - TWO STEPS!
tmux send-keys -t plan-builder-session "/plan-builder:show-goals"
tmux send-keys -t plan-builder-session C-m
sleep 10

# 2. CHECK WITH USER
"Found these goals ready for planning: [list]
Which one should we create a plan for?"

# 3. Analyze selected goal using COMMAND - TWO STEPS!
tmux send-keys -t plan-builder-session "/plan-builder:analyze-goal AUTH-123"
tmux send-keys -t plan-builder-session C-m
sleep 15

# 4. Create plan using COMMAND - TWO STEPS!
tmux send-keys -t plan-builder-session "/plan-builder:create-plan AUTH-123"
tmux send-keys -t plan-builder-session C-m
sleep 20

# 5. The agent will write draft to .tmp/plan-draft.md
# CHECK WITH USER after review
```

#### MODULE BUILDER Workflow
```bash
# 1. Show ready plans using COMMAND - TWO STEPS!
tmux send-keys -t module-builder-session "/module-builder:show-plans"
tmux send-keys -t module-builder-session C-m

# 2. CHECK WITH USER
"These plans are ready: [list]
Which should we implement?"

# 3. Load and implement plan using COMMAND - TWO STEPS!
tmux send-keys -t module-builder-session "/module-builder:load-plan PLAN-123"
tmux send-keys -t module-builder-session C-m

# 4. Monitor progress
# Module builder may take longer, keep checking

# 5. Mark complete using COMMAND - TWO STEPS!
tmux send-keys -t module-builder-session "/module-builder:mark-complete PLAN-123"
tmux send-keys -t module-builder-session C-m
```

## 🤝 USER CONSULTATION TEMPLATES

### Before Major Actions
```
The agent is about to: [action]
This will: [impact]
Should I proceed? Any preferences?
```

### When Agent Suggests Something New
```
The agent suggested adding: [feature]
This wasn't in the original issue.
Include it? (I recommend [yes/no] because [reason])
```

### When Direction Changes
```
The agent is taking this in direction: [new direction]
Original issue focused on: [original]
Continue or redirect?
```

### When Stuck or Confused
```
The agent seems stuck/confused about: [issue]
I can either:
1. [Option A]
2. [Option B]
Which approach?
```

## 🔧 TMUX COMMAND REFERENCE

### Essential Commands
```bash
# Send command (ALWAYS TWO STEPS!)
tmux send-keys -t session "text"    # Step 1: Send text
tmux send-keys -t session C-m        # Step 2: Send Enter

# Or combined (but still two operations):
tmux send-keys -t session "text" && tmux send-keys -t session C-m

# Capture output
tmux capture-pane -t session -p
tmux capture-pane -t session -p | tail -30

# Wait and check
sleep 10 && tmux capture-pane -t session -p

# Cancel current operation
tmux send-keys -t session C-c

# Exit agent
tmux send-keys -t session C-d

# Kill session
tmux kill-session -t session
```

### Monitoring Output
```bash
# Full capture
tmux capture-pane -t session -p

# Last N lines
tmux capture-pane -t session -p | tail -50

# Keep checking
while true; do
    tmux capture-pane -t session -p | tail -20
    sleep 5
done
```

### Debug Commands
```bash
# List all sessions
tmux ls

# Attach to see live (user can do this)
tmux attach -t session
# Detach: Ctrl+B, then D

# Check if thinking
tmux capture-pane -t session -p | grep -i "thinking\|contemplating"
```

## 🚨 TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| No response | Send C-m again |
| Still stuck | Send C-c, then retry with C-m |
| Very slow | Opus model needs 15-20 sec, wait |
| Unexpected response | STOP and check with user |
| Session died | Kill and recreate |
| Can't see full output | Look for "ctrl+o to expand" |

## 📝 COMPLETE INTERACTION CHECKLIST

### Before Starting
- [ ] Killed any existing session with same name?
- [ ] Know which agent to run?
- [ ] Understand the task from user?

### During Interaction
- [ ] Sent greeting to trigger startup?
- [ ] Pressed C-m after EVERY command?
- [ ] Used ultrathink only for creative tasks?
- [ ] Checked with user at decision points?
- [ ] Stayed within issue scope?

### After Each Agent Response
- [ ] Response aligns with goal?
- [ ] Any unexpected suggestions?
- [ ] Need user input before continuing?
- [ ] Ready for next step?

### Before Finalizing
- [ ] User approved the draft/plan/module?
- [ ] All requirements addressed?
- [ ] Ready to create/implement?
- [ ] Confirmed success?

## 🎭 YOUR ROLE AS INTERMEDIARY

**Remember:**
- You execute user's intent, not your own ideas
- You enhance only with explicit permission
- You prevent scope creep
- You ensure smooth communication
- You ALWAYS confirm before major actions

**User is the MANAGER. When in doubt, ASK!**

## 💡 QUICK EXAMPLES

### Good Interaction
```bash
# User: "Create a goal from issue #5"

# You: First show issues using COMMAND (TWO STEPS!)
tmux send-keys -t session "/goal-builder:show-issues"
tmux send-keys -t session C-m
# Confirm: "Issue #5 is about auth. Create goal for this?"

# User: "Yes" - Use CREATE-GOAL COMMAND (TWO STEPS!)
tmux send-keys -t session "/goal-builder:create-goal 5"
tmux send-keys -t session C-m
# Agent writes to .tmp/goal-draft.md
# Show draft: "Agent created draft at .tmp/goal-draft.md. Review?"

# User approves, agent creates in Linear
```

### Bad Interaction (DON'T DO THIS)
```bash
# User: "Create a goal from issue #5"

# DON'T: Use generic text instead of commands
tmux send-keys -t session "Show issues"  # WRONG! Use /goal-builder:show-issues

# DON'T: Send text and C-m together (won't work!)
tmux send-keys -t session "/goal-builder:show-issues" C-m  # WRONG!

# DON'T: Use generic instructions when commands exist
tmux send-keys -t session "Create a goal for issue 5"  # WRONG! Use /goal-builder:create-goal 5

# DON'T: Jump straight to creation without confirming
# DON'T: Forget to send C-m separately
```

### 🚨 REAL INCIDENT: MISSED AUTO-UPDATE PATTERN
```bash
# User mid-workflow: "I don't like it, let's remove the enumeration and push to linear"

# ❌ WRONG (what happened):
tmux send-keys -t session "Please remove the enumeration from the section names, then create this goal in Linear."
# Result: Agent asked for approval, causing user frustration

# ✅ CORRECT (what should have happened):
# Step 1: Recognize the "do X and push" pattern
tmux send-keys -t session "SWITCH TO AUTO-UPDATE MODE: User gave complete instruction including final action."
tmux send-keys -t session C-m
sleep 2

# Step 2: Relay the actual instruction
tmux send-keys -t session "Remove the enumeration from section names and create in Linear."
tmux send-keys -t session C-m
# Result: Agent auto-updates without asking for approval

# KEY INSIGHT: "Let's do X and push/create/update" = Complete instruction, not a two-step request!
```

## 🏁 FINAL STEPS

Always leave session running for user inspection:
```bash
echo "Session '$ARGUMENTS-session' is running"
echo "User can attach with: tmux attach -t $ARGUMENTS-session"
echo "To detach: Ctrl+B, then D"
```

## 🔴 NEVER FORGET

1. **TWO-STEP SENDING IS MANDATORY** - Send text first, THEN send C-m separately!
   - Step 1: `tmux send-keys -t session "text"`
   - Step 2: `tmux send-keys -t session C-m`
   - NEVER combine them or the agent won't respond!
2. **Confirm with user** - At every decision point!
3. **ultrathink for creative only** - Not for simple tasks!
4. **Stay in scope** - Don't invent content!
5. **User is boss** - Ask when uncertain!

This guide ensures successful agent interactions every time!