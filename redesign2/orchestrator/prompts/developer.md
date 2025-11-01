<!-- PURPOSE: Technical reference - CRITICAL technical details ONLY -->
<!-- LOADED BY: /prime command at startup -->
<!-- CONTAINS: TMux patterns, agent paths, session management, wait times -->
<!-- DOES NOT CONTAIN: Workflows (→ WORKFLOW.md), commands (→ settings.json), auto-update logic (→ AGENT-INTERACTION-CRITICAL-RULES.md) -->

# Developer Essentials

## 🔴 CRITICAL: TMux Two-Step Command Sending

**Claude agents require TWO SEPARATE tmux operations:**

```bash
# ❌ WRONG - Will NOT work!
tmux send-keys -t session "text" C-m

# ✅ CORRECT - Must be two separate commands
tmux send-keys -t session "text"    # Step 1: Send text
tmux send-keys -t session C-m        # Step 2: Send Enter
```

**WHY**: Claude agents wait for the FULL prompt before executing. Combining text+C-m breaks this.

**If agent seems stuck**:
```bash
tmux send-keys -t session C-m  # Send C-m again separately
```

---

## Agent Workspace Paths

### From Orchestrator Location

```bash
# Orchestrator is at: /redesign2/orchestrator/

# Agent paths (relative to orchestrator):
../goal-builder/      # Goal Builder workspace
../plan-builder/      # Plan Builder workspace
../module-builder/    # Module Builder workspace

# Shared configuration:
../shared/            # Shared config.yaml and .env

# Orchestrator's own critical files:
.claude/AGENT-INTERACTION-CRITICAL-RULES.md
.claude/commands/run-agent.md
```

### Launch Scripts

```bash
# From orchestrator directory:
cd ../goal-builder && ./run.sh
cd ../plan-builder && ./run.sh
cd ../module-builder && ./run.sh
```

---

## Session Management Patterns

### Create Session

```bash
SESSION_NAME="goal-builder-session"

# Kill old session if exists
tmux kill-session -t $SESSION_NAME 2>/dev/null

# Create new session
tmux new-session -d -s $SESSION_NAME

# Launch agent
tmux send-keys -t $SESSION_NAME "cd /Users/Shyroian/mixer-backend/hey-mixer/redesign2/goal-builder && ./run.sh"
tmux send-keys -t $SESSION_NAME C-m

# Wait for agent to start
sleep 5

# Send agent's prime command (TWO STEPS!)
# All agents use /prime (no prefix)
tmux send-keys -t $SESSION_NAME "/prime"
tmux send-keys -t $SESSION_NAME C-m

# Wait for context loading
sleep 20
```

### Capture Output

```bash
# Full capture
tmux capture-pane -t $SESSION_NAME -p

# Last N lines
tmux capture-pane -t $SESSION_NAME -p | tail -30

# Full history (for saving conversation)
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
tmux capture-pane -t $SESSION_NAME -p -S - > ".tmp/sessions/${SESSION_NAME}-${TIMESTAMP}.txt"
```

### Send Commands

**ALWAYS use agent's slash commands** (from `.claude/settings.json`):

```bash
# Send command (TWO STEPS!)
# Each agent knows its own commands (no prefix needed)
tmux send-keys -t $SESSION_NAME "/show-issues"
tmux send-keys -t $SESSION_NAME C-m

# Wait for response
sleep 10

# Capture result
tmux capture-pane -t $SESSION_NAME -p | tail -50
```

---

## Agent Commands Reference

**See `.claude/settings.json`** for authoritative command list.

Quick reference for common commands:

### Goal Builder (send to goal-builder session)
- `/prime`
- `/show-issues`
- `/show-drafts`
- `/create-goal [numbers] [--auto-update]`
- `/edit-draft [goal-id] [--auto-update]`

### Plan Builder (send to plan-builder session)
- `/prime`
- `/show-goals`
- `/create-plan [goal-id] [--auto-update]`

### Module Builder (send to module-builder session)
- `/prime`
- `/show-plans`
- `/load-plan [plan-id]`

**For complete workflows**: See `.claude/commands/run-agent.md`

---

## Wait Times

```bash
# After sending greeting: 10 seconds
sleep 10

# After /agent:prime: 20 seconds
sleep 20

# After simple command (show-issues): 10 seconds
sleep 10

# After complex command (create-goal): 20 seconds
sleep 20

# After agent thinking deeply: 30+ seconds
sleep 30
```

---

## Error Detection

Check for these patterns in output:

```bash
OUTPUT=$(tmux capture-pane -t session -p)

# Check for errors
if echo "$OUTPUT" | grep -q "error\\|Error\\|ERROR\\|failed\\|Failed"; then
    # Report error to user
fi

# Check for MCP auth failures
if echo "$OUTPUT" | grep -q "authentication\\|unauthorized\\|401"; then
    # Suggest checking .env tokens
fi
```

---

## Session Cleanup

```bash
# List all sessions
tmux ls

# Kill specific session
tmux kill-session -t goal-builder-session

# Kill all mixer sessions
tmux ls | grep -E "(goal|plan|module)-builder-session" | cut -d: -f1 | xargs -I {} tmux kill-session -t {}
```

---

## Configuration Sources

Agents read configuration from:
```bash
# Shared config (all agents in redesign2/)
../shared/config.yaml
../shared/.env

# Agent-specific
../goal-builder/CLAUDE.md
../goal-builder/.claude/skills/
../goal-builder/prompts/
```

---

## Debugging

### Check if session exists
```bash
tmux has-session -t goal-builder-session 2>/dev/null
echo $?  # 0 = exists, 1 = doesn't exist
```

### Attach to session manually
```bash
# User can do this to see live interaction
tmux attach -t goal-builder-session
# Detach: Ctrl+B, then D
```

### View session history
```bash
# Show last 100 lines
tmux capture-pane -t goal-builder-session -p -S -100
```

---

## References

**For complete coordination guide**: See `.claude/commands/run-agent.md`
**For auto-update patterns**: See `.claude/AGENT-INTERACTION-CRITICAL-RULES.md`
**For workflows**: See `.claude/skills/WORKFLOW.md`
