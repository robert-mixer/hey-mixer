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

### 1. ALWAYS Press Enter (C-m)
```bash
# WRONG - Command won't execute, agent appears stuck
tmux send-keys -t session "command"

# CORRECT - Command will execute
tmux send-keys -t session "command" C-m
```
**Without C-m, commands WILL NOT execute!** If agent seems stuck, send C-m.

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
# Creative - USE ultrathink
tmux send-keys -t session "Draft a comprehensive goal for this authentication system. Include all technical requirements. ultrathink" C-m

# Simple - NO ultrathink
tmux send-keys -t session "Show me the GitHub issues" C-m
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
# Send greeting to trigger startup message
tmux send-keys -t $ARGUMENTS-session "Hello" C-m

# Wait for response
sleep 10

# Capture output
tmux capture-pane -t $ARGUMENTS-session -p | tail -30
```

### Phase 3: Agent-Specific Workflows

#### GOAL BUILDER Workflow
```bash
# 1. Show issues (no ultrathink)
tmux send-keys -t goal-builder-session "Show me all GitHub issues" C-m
sleep 10

# 2. CHECK WITH USER
"I found these issues: [list]
Which ones should we create goals for?
Should we combine any of them?"

# 3. After user selects issue(s)
tmux send-keys -t goal-builder-session "Let's create a goal for issue #X. Draft something comprehensive. ultrathink" C-m
sleep 20

# 4. CHECK WITH USER
"The agent drafted: [summary]
Any changes needed? Should we add anything?"

# 5. If approved
tmux send-keys -t goal-builder-session "Perfect! Save this draft first" C-m
sleep 10

# 6. Create goal
tmux send-keys -t goal-builder-session "Now create the goal in Linear" C-m
sleep 15

# 7. Confirm completion
"Goal created successfully! Issue #X has been closed."
```

#### PLAN BUILDER Workflow
```bash
# 1. Show available goals
tmux send-keys -t plan-builder-session "Show goals with todo status" C-m
sleep 10

# 2. CHECK WITH USER
"Found these goals ready for planning: [list]
Which one should we create a plan for?"

# 3. Analyze selected goal
tmux send-keys -t plan-builder-session "Analyze goal AUTH-123" C-m
sleep 15

# 4. Draft plan (creative task)
tmux send-keys -t plan-builder-session "Create a detailed implementation plan. Break it into clear steps. ultrathink" C-m
sleep 20

# 5. CHECK WITH USER
"Plan includes: [summary of steps]
Look good? Any technical preferences?"

# 6. Create plan
tmux send-keys -t plan-builder-session "Create this plan in Linear" C-m
```

#### MODULE BUILDER Workflow
```bash
# 1. Show ready plans
tmux send-keys -t module-builder-session "Show plans with todo status" C-m

# 2. CHECK WITH USER
"These plans are ready: [list]
Which should we implement?"

# 3. Start implementation
tmux send-keys -t module-builder-session "Implement plan PLAN-123. Create the complete module. ultrathink" C-m

# 4. Monitor progress
# Module builder may take longer, keep checking

# 5. CHECK WITH USER
"Module implemented with: [summary]
Should we mark as complete?"
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
# Send command (ALWAYS with C-m!)
tmux send-keys -t session "text" C-m

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

# You: Check issue first
tmux send-keys -t session "Show issues" C-m
# Confirm: "Issue #5 is about auth. Create goal for this?"

# User: "Yes"
tmux send-keys -t session "Create comprehensive goal for issue #5 about authentication. ultrathink" C-m
# Show draft: "Agent drafted [summary]. Proceed?"

# User: "Yes"
tmux send-keys -t session "Save and create goal" C-m
```

### Bad Interaction (DON'T DO THIS)
```bash
# User: "Create a goal from issue #5"

# DON'T: Jump straight to creation without confirming
# DON'T: Add features not in issue without asking
# DON'T: Forget C-m and wonder why it's stuck
# DON'T: Use ultrathink for "show issues"
```

## 🏁 FINAL STEPS

Always leave session running for user inspection:
```bash
echo "Session '$ARGUMENTS-session' is running"
echo "User can attach with: tmux attach -t $ARGUMENTS-session"
echo "To detach: Ctrl+B, then D"
```

## 🔴 NEVER FORGET

1. **C-m after EVERY command** - Or it won't run!
2. **Confirm with user** - At every decision point!
3. **ultrathink for creative only** - Not for simple tasks!
4. **Stay in scope** - Don't invent content!
5. **User is boss** - Ask when uncertain!

This guide ensures successful agent interactions every time!