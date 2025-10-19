# 🔴 AGENT COMMAND REFERENCE - MANDATORY USE 🔴

This file contains the COMPLETE mapping of user intents to agent commands.
**CRITICAL**: When coordinating with agents via tmux, you MUST use these exact commands!

## GOAL BUILDER AGENT COMMANDS

### `/goal-builder:show-issues`
**User Intent Triggers (ANY of these = use this command):**
- "show issues"
- "list issues"
- "what issues"
- "display issues"
- "see the issues"
- "view issues"
- "1" (when option 1 is "View all open issues")

**tmux Usage:**
```bash
tmux send-keys -t goal-builder-session "/goal-builder:show-issues"
tmux send-keys -t goal-builder-session C-m
```

### `/goal-builder:analyze-issues`
**User Intent Triggers:**
- "analyze issues"
- "group issues"
- "organize issues"
- "suggest groupings"
- "how should we group"
- "2" (when option 2 is "See suggested groupings")

**tmux Usage:**
```bash
tmux send-keys -t goal-builder-session "/goal-builder:analyze-issues"
tmux send-keys -t goal-builder-session C-m
```

### `/goal-builder:create-goal [issue-numbers]`
**User Intent Triggers:**
- "create goal"
- "make a goal"
- "create goal from issue #X"
- "1" (when context is "Create a goal from this single issue")
- "3" (when option 3 is "Jump straight to creating a goal")
- "yes" (after selecting issues to group)

**CRITICAL WORKFLOW:**
1. This command writes draft to `.tmp/goal-draft.md` FIRST
2. NEVER show draft in chat before file exists
3. The command handles the entire draft/iterate/save workflow

**tmux Usage:**
```bash
# Single issue
tmux send-keys -t goal-builder-session "/goal-builder:create-goal 5"
tmux send-keys -t goal-builder-session C-m

# Multiple issues
tmux send-keys -t goal-builder-session "/goal-builder:create-goal 5,8,12"
tmux send-keys -t goal-builder-session C-m
```

### `/goal-builder:save-draft [filename]`
**User Intent Triggers:**
- "save draft"
- "save this"
- "save the draft"

**tmux Usage:**
```bash
tmux send-keys -t goal-builder-session "/goal-builder:save-draft"
tmux send-keys -t goal-builder-session C-m
```

## PLAN BUILDER AGENT COMMANDS

### `/plan-builder:show-goals`
**User Intent Triggers:**
- "show goals"
- "list goals"
- "what goals"
- "display goals"
- "view Linear goals"

**tmux Usage:**
```bash
tmux send-keys -t plan-builder-session "/plan-builder:show-goals"
tmux send-keys -t plan-builder-session C-m
```

### `/plan-builder:analyze-goal [goal-id]`
**User Intent Triggers:**
- "analyze goal X"
- "look at goal X"
- "examine goal X"
- "understand goal X"

**tmux Usage:**
```bash
tmux send-keys -t plan-builder-session "/plan-builder:analyze-goal AUTH-123"
tmux send-keys -t plan-builder-session C-m
```

### `/plan-builder:create-plan [goal-id]`
**User Intent Triggers:**
- "create plan"
- "make a plan"
- "plan for goal X"
- "implement goal X"

**CRITICAL WORKFLOW:**
1. Writes draft to `.tmp/plan-draft.md` FIRST
2. Iterates with user on file content
3. Creates in Linear only after approval

**tmux Usage:**
```bash
tmux send-keys -t plan-builder-session "/plan-builder:create-plan AUTH-123"
tmux send-keys -t plan-builder-session C-m
```

## MODULE BUILDER AGENT COMMANDS

### `/module-builder:show-plans`
**User Intent Triggers:**
- "show plans"
- "list plans"
- "what plans"
- "display plans"
- "view Linear plans"

**tmux Usage:**
```bash
tmux send-keys -t module-builder-session "/module-builder:show-plans"
tmux send-keys -t module-builder-session C-m
```

### `/module-builder:load-plan [plan-id]`
**User Intent Triggers:**
- "load plan X"
- "implement plan X"
- "start with plan X"
- "work on plan X"

**tmux Usage:**
```bash
tmux send-keys -t module-builder-session "/module-builder:load-plan PLAN-456"
tmux send-keys -t module-builder-session C-m
```

### `/module-builder:mark-complete [plan-id]`
**User Intent Triggers:**
- "mark complete"
- "mark as done"
- "complete the plan"
- "finish plan X"

**tmux Usage:**
```bash
tmux send-keys -t module-builder-session "/module-builder:mark-complete PLAN-456"
tmux send-keys -t module-builder-session C-m
```

## VERIFICATION CHECKLIST

After sending ANY command to an agent, verify:

### For Goal Builder:
- [ ] `/goal-builder:show-issues` → Agent displays GitHub issues list
- [ ] `/goal-builder:create-goal` → File created at `.tmp/goal-draft.md`
- [ ] Draft workflow → Agent uses Read/Write/Edit on `.tmp/goal-draft.md`

### For Plan Builder:
- [ ] `/plan-builder:show-goals` → Agent displays Linear goals
- [ ] `/plan-builder:create-plan` → File created at `.tmp/plan-draft.md`
- [ ] Draft workflow → Agent uses Read/Write/Edit on `.tmp/plan-draft.md`

### For Module Builder:
- [ ] `/module-builder:show-plans` → Agent displays Linear plans
- [ ] `/module-builder:load-plan` → Agent loads and starts implementation
- [ ] `/module-builder:mark-complete` → Updates Linear status

## COMMON MISTAKES TO AVOID

### ❌ NEVER DO THIS:
```bash
# Generic text instead of command
tmux send-keys -t session "Show me the issues"  # WRONG!
tmux send-keys -t session "Create a goal"       # WRONG!
tmux send-keys -t session "Analyze this"        # WRONG!
```

### ✅ ALWAYS DO THIS:
```bash
# Use exact slash commands
tmux send-keys -t session "/goal-builder:show-issues"      # CORRECT!
tmux send-keys -t session "/goal-builder:create-goal 5"    # CORRECT!
tmux send-keys -t session "/goal-builder:analyze-issues"   # CORRECT!
```

## ENFORCEMENT RULES

1. **Automatic Invocation**: When user intent matches, invoke command IMMEDIATELY
2. **No Waiting**: Don't wait for user to type the exact command
3. **Verification**: Always check that expected files/outputs are created
4. **Correction**: If agent doesn't auto-invoke, you MUST send the command explicitly

## REMEMBER

**Your #1 Priority**: ALWAYS use agent commands, NEVER generic text!

This reference is NON-NEGOTIABLE. Failure to use these commands is a CRITICAL ERROR that breaks the entire workflow system.