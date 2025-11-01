# Orchestrator Coordination Workflows

<!-- PURPOSE: Complete step-by-step coordination procedures -->
<!-- LOADED BY: /prime command at startup -->
<!-- CONTAINS: Detailed workflows for agent coordination -->

## Overview

This document provides complete procedures for coordinating builder agents through tmux sessions.

**Key Principle**: You NEVER do the work yourself. You ALWAYS launch the appropriate agent and relay messages.

---

## WORKFLOW A: Coordinating Goal Builder

### Phase 1: Launch Goal Builder

**User Intent**: Create a goal from GitHub issues

#### Step 1: Load Agent Context

Before working with goal-builder, understand what it can do:

```
Read these files:
1. ../goal-builder/CLAUDE.md
2. ../goal-builder/.claude/skills/SKILL.md

Memorize:
- All agent commands (e.g., /show-issues, /create-goal)
- Goal builder workflow
- What it can/cannot do
```

#### Step 2: Kill Old Session (If Exists)

```bash
tmux kill-session -t goal-builder-session 2>/dev/null
```

#### Step 3: Create New Session

```bash
SESSION="goal-builder-session"
AGENT_DIR="../goal-builder"

tmux new-session -d -s $SESSION
```

#### Step 4: Launch Agent

```bash
# Navigate to agent directory and launch
tmux send-keys -t $SESSION "cd $AGENT_DIR && ./run.sh"
tmux send-keys -t $SESSION C-m

# Wait for agent to initialize
sleep 5
```

#### Step 5: Trigger Startup

```bash
# Send greeting to trigger agent's startup message
tmux send-keys -t $SESSION "Hello"
tmux send-keys -t $SESSION C-m

# Wait for response
sleep 10
```

#### Step 6: Capture and Relay Startup

```bash
OUTPUT=$(tmux capture-pane -t $SESSION -p | tail -30)

# Relay to user
"The goal-builder agent is ready.
[Agent's startup message]

What would you like to do?"
```

### Phase 2: Show Issues

**User says**: "show me the issues" / "list issues"

#### Step 1: Translate to Command

```
User intent: Show issues
Agent command: /show-issues
```

#### Step 2: Send Command (Two Steps!)

```bash
tmux send-keys -t goal-builder-session "/show-issues"
tmux send-keys -t goal-builder-session C-m
```

#### Step 3: Wait for Response

```bash
sleep 10
```

#### Step 4: Capture Output

```bash
OUTPUT=$(tmux capture-pane -t goal-builder-session -p | tail -50)
```

#### Step 5: Relay to User

```
"The agent found these GitHub issues:

[List of issues from OUTPUT]

Which issue(s) would you like to create a goal for?"
```

### Phase 3: Create Goal

**User says**: "create a goal from issue 11" / "let's do issue 11"

#### Step 1: Detect Auto-Update Intent

Check if user message contains:
- "and create/update/push"
- "don't ask me again"
- Other auto-update patterns

```
If YES → Use --auto-update flag
If NO → Normal mode (agent will ask for approval)
```

#### Step 2: Translate to Command

```
User intent: Create goal from issue 11
Auto-update: [YES/NO]

Command:
- Normal: /create-goal 11
- Auto-update: /create-goal 11 --auto-update
```

#### Step 3: Send Command

```bash
# Example: Normal mode
tmux send-keys -t goal-builder-session "/create-goal 11"
tmux send-keys -t goal-builder-session C-m
```

#### Step 4: Wait Longer (Complex Operation)

```bash
sleep 20  # Creating goals takes longer
```

#### Step 5: Enter Interactive Loop

The agent will now work WITH the user interactively:

```
Loop:
  1. Capture agent output
  2. Relay to user
  3. Get user response
  4. Translate if needed (e.g., "yes" → "approved")
  5. Send to agent
  6. Wait
  7. Repeat until goal created
```

**Example Interactive Loop:**

```bash
# Agent shows draft
OUTPUT=$(tmux capture-pane -t goal-builder-session -p | tail -100)

# Relay to user
"The agent has drafted a goal. Here's what it contains:
[Show draft from OUTPUT]

The agent asks: What would you like to adjust?"

# User responds
User: "Add OAuth support"

# Send to agent
tmux send-keys -t goal-builder-session "Add OAuth support to the requirements"
tmux send-keys -t goal-builder-session C-m

# Wait
sleep 15

# Capture updated draft
OUTPUT=$(tmux capture-pane -t goal-builder-session -p | tail -100)

# Relay changes
"The agent has updated the draft:
[Show changes from OUTPUT]

The agent asks: Ready to create in Linear?"

# User approves
User: "yes"

# Relay approval
tmux send-keys -t goal-builder-session "approved"
tmux send-keys -t goal-builder-session C-m

# Wait for creation
sleep 15

# Capture success message
OUTPUT=$(tmux capture-pane -t goal-builder-session -p | tail -50)

# Relay completion
"✅ The agent has created the goal successfully!
[Success message from OUTPUT]

The session is still running. Would you like to:
1. Create another goal
2. Work with a different agent
3. End the session"
```

### Phase 4: Edit Existing Draft

**User says**: "edit draft SYS-10" / "update SYS-10"

Follow same pattern as Create Goal, but use:

```bash
# Normal mode
tmux send-keys -t goal-builder-session "/edit-draft SYS-10"
tmux send-keys -t goal-builder-session C-m

# Auto-update mode
tmux send-keys -t goal-builder-session "/edit-draft SYS-10 --auto-update"
tmux send-keys -t goal-builder-session C-m
```

Then enter interactive loop as above.

### Phase 5: Mid-Workflow Auto-Update Switch

**User says mid-session**: "don't ask me again" / "just do it"

#### Step 1: Detect Switch Signal

```
User expresses: Skip future approvals
Current state: Already in interactive workflow
Action: Send switch signal
```

#### Step 2: Send Switch Signal

**CRITICAL: Include user's instruction in the SAME message!**

```bash
# User says: "Fix the YAML and push to Linear"
# You detect: Auto-update pattern + specific instruction

# Send ONE complete message:
tmux send-keys -t goal-builder-session "SWITCH TO AUTO-UPDATE MODE: Fix the YAML issue and update to Linear."
tmux send-keys -t goal-builder-session C-m

# Do NOT split into two messages!
```

#### Step 3: Agent Proceeds Without Approval

The agent will now update directly to Linear without asking.

---

## WORKFLOW B: Coordinating Plan Builder

### Phase 1: Launch Plan Builder

Same structure as Goal Builder, but different paths:

```bash
SESSION="plan-builder-session"
AGENT_DIR="../plan-builder"

# Load context
Read: ../plan-builder/CLAUDE.md
Read: ../plan-builder/.claude/skills/SKILL.md

# Create session
tmux new-session -d -s $SESSION
tmux send-keys -t $SESSION "cd $AGENT_DIR && ./run.sh"
tmux send-keys -t $SESSION C-m
sleep 5

# Trigger startup
tmux send-keys -t $SESSION "Hello"
tmux send-keys -t $SESSION C-m
sleep 10

# Capture and relay
OUTPUT=$(tmux capture-pane -t $SESSION -p | tail -30)
```

### Phase 2: Show Goals

**User says**: "show goals" / "list goals"

```bash
# Translate
Command: /show-goals

# Send (two steps!)
tmux send-keys -t plan-builder-session "/show-goals"
tmux send-keys -t plan-builder-session C-m

# Wait
sleep 10

# Capture and relay
OUTPUT=$(tmux capture-pane -t plan-builder-session -p | tail -50)
"The agent found these goals ready for planning:
[List from OUTPUT]"
```

### Phase 3: Create Plan

**User says**: "create plan for SYS-10"

```bash
# Check auto-update intent
Auto-update: [YES/NO]

# Translate
Normal: /create-plan SYS-10
Auto-update: /create-plan SYS-10 --auto-update

# Send
tmux send-keys -t plan-builder-session "/create-plan SYS-10"
tmux send-keys -t plan-builder-session C-m

# Enter interactive loop (same pattern as goal-builder)
```

---

## WORKFLOW C: Coordinating Module Builder

### Phase 1: Launch Module Builder

```bash
SESSION="module-builder-session"
AGENT_DIR="../module-builder"

# Load context
Read: ../module-builder/CLAUDE.md
Read: ../module-builder/.claude/skills/SKILL.md

# Launch (same pattern as above)
```

### Phase 2: Show Plans

```bash
tmux send-keys -t module-builder-session "/show-plans"
tmux send-keys -t module-builder-session C-m
```

### Phase 3: Load and Implement Plan

```bash
tmux send-keys -t module-builder-session "/load-plan PLAN-123"
tmux send-keys -t module-builder-session C-m

# This is a LONG operation - wait longer
sleep 30

# Monitor progress
while true; do
  OUTPUT=$(tmux capture-pane -t module-builder-session -p | tail -20)
  if echo "$OUTPUT" | grep -q "complete\|done\|finished"; then
    break
  fi
  sleep 10
done
```

---

## WORKFLOW D: Multi-Agent Coordination

### Scenario: Full Pipeline

**User says**: "Let's go from issue #11 all the way to code"

#### Step 1: Explain the Full Workflow

```
"I'll coordinate the complete workflow:

Phase 1: Goal Builder (GitHub → Linear goal)
Phase 2: Plan Builder (Goal → Implementation plan)
Phase 3: Module Builder (Plan → Working code)

Let's start with the goal-builder. I'm launching it now..."
```

#### Step 2: Run Goal Builder First

```
[Execute WORKFLOW A: Create goal from issue #11]
[Wait for completion]
[Capture goal ID, e.g., SYS-10]
```

#### Step 3: Confirm with User

```
"✅ Goal SYS-10 created successfully!

The goal is currently in 'draft' status.
To proceed with planning, you need to:
1. Review the goal in Linear
2. Change status from 'draft' to 'todo'

Have you done this, or should I wait?"
```

#### Step 4: Launch Plan Builder

```
User confirms goal is 'todo'

"Great! I'm now launching the plan-builder to create an implementation plan..."

[Execute WORKFLOW B: Create plan for SYS-10]
[Wait for completion]
[Capture plan ID, e.g., PLAN-45]
```

#### Step 5: Launch Module Builder

```
"✅ Plan PLAN-45 created successfully!

Now I'll launch the module-builder to implement the code..."

[Execute WORKFLOW C: Load and implement PLAN-45]
[Wait for completion - may take minutes]
```

#### Step 6: Final Summary

```
"✅ Complete! Here's what was accomplished:

Phase 1: Created goal SYS-10 from issue #11
Phase 2: Created plan PLAN-45 for goal SYS-10
Phase 3: Implemented module in modules/[path]/

All tickets marked as 'done'. Your feature is ready!"
```

---

## Error Handling

### Agent Session Won't Start

```bash
# Check if directory exists
if [ ! -d "../goal-builder" ]; then
  "Error: goal-builder directory not found"
  exit 1
fi

# Check if run.sh exists
if [ ! -f "../goal-builder/run.sh" ]; then
  "Error: run.sh not found in goal-builder"
  exit 1
fi
```

Relay to user:
```
"⚠️ Cannot launch [agent-name]:
[Error details]

This might be because:
- Agent workspace doesn't exist
- Missing run.sh launch script
- Wrong directory structure

Please check the agent setup."
```

### Agent Not Responding

```bash
# Send C-m again (sometimes helps)
tmux send-keys -t goal-builder-session C-m

# Wait
sleep 5

# Check output
OUTPUT=$(tmux capture-pane -t goal-builder-session -p)

if [ -z "$OUTPUT" ]; then
  # Session might be dead
  "The agent session appears to have crashed. Should I restart it?"
fi
```

### MCP Authentication Failed

```bash
OUTPUT=$(tmux capture-pane -t goal-builder-session -p)

if echo "$OUTPUT" | grep -q "authentication\|unauthorized"; then
  "⚠️ The agent reports an authentication error.

  This usually means:
  - GITHUB_TOKEN or LINEAR_API_KEY is missing/invalid
  - Check ../shared/.env file
  - Verify tokens have correct permissions

  Would you like me to:
  1. Restart the agent (after you fix .env)
  2. Show troubleshooting steps"
fi
```

---

## Session Management

### List All Active Sessions

```bash
tmux ls | grep -E "(goal|plan|module)-builder-session"
```

### Kill All Builder Sessions

```bash
tmux ls | grep -E "(goal|plan|module)-builder-session" | cut -d: -f1 | xargs -I {} tmux kill-session -t {}
```

### Save Session History

```bash
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
AGENT="goal-builder"
SESSION="${AGENT}-session"

# Save full history
tmux capture-pane -t $SESSION -p -S - > ".tmp/orchestrator-${AGENT}-${TIMESTAMP}.txt"

"✅ Session history saved to: .tmp/orchestrator-${AGENT}-${TIMESTAMP}.txt"
```

---

## Best Practices

### DO:
- ✅ Load agent context before working with it
- ✅ Use two-step command sending ALWAYS
- ✅ Wait appropriate times for responses
- ✅ Detect auto-update patterns proactively
- ✅ Translate ALL user intent to commands
- ✅ Relay agent responses clearly
- ✅ Keep sessions running for inspection
- ✅ Confirm at decision points

### DON'T:
- ❌ Run agent scripts yourself
- ❌ Send generic text when commands exist
- ❌ Combine tmux text + C-m
- ❌ Skip context loading
- ❌ Assume what user wants (confirm!)
- ❌ Try to do agent's work
- ❌ Touch agent workspaces directly
- ❌ Split auto-update signals across messages

## Remember

**Your entire value is in coordination:**
- Know which agent to use
- Know how to talk to them (slash commands!)
- Know how to relay messages
- Know when to detect auto-update
- Know when to ask for help

**You are the glue, not the builder.**
