---
description: Initialize Orchestrator (load all context)
disable-model-invocation: false
---

# Prime - Load Orchestrator Context

## Purpose

This command loads ALL essential context needed for the orchestrator to coordinate builder agents effectively.

**🔴 CRITICAL: Run this FIRST in every session!**

---

## Read

Read these files in order to load complete orchestrator context:

### 1. System Guardrails

```
prompts/system.md
```

Contains:
- Core responsibility (coordinate, don't execute)
- Absolute rules (never act as builder)
- Command translation patterns
- Two-step tmux sending (MANDATORY)
- Auto-update detection
- Confirmation requirements

### 2. Technical Details

```
prompts/developer.md
```

Contains:
- TMux two-step command sending (CRITICAL!)
- Agent workspace paths
- Session management patterns
- Agent command reference
- Auto-update pattern detection
- Wait times and error detection

### 3. User Interaction

```
prompts/user.md
```

Contains:
- Greeting templates
- Common user intents
- Mid-workflow interactions
- Error handling messages
- Completion messages

### 4. Skills Quick Reference

```
.claude/skills/SKILL.md
```

Contains:
- Core job summary
- The three agents overview
- Agent commands you MUST use
- Command translation examples
- Two-step rule reminder
- Critical rules checklist

### 5. Coordination Workflows

```
.claude/skills/WORKFLOW.md
```

Contains:
- Complete workflow for Goal Builder coordination
- Complete workflow for Plan Builder coordination
- Complete workflow for Module Builder coordination
- Multi-agent coordination
- Error handling procedures
- Session management

### 6. Agent Interaction Critical Rules

```
.claude/AGENT-INTERACTION-CRITICAL-RULES.md
```

Contains:
- Absolute rule: You are NOT the agent
- Forbidden actions
- Allowed actions
- Role explanation
- Red flags
- Mental models
- Real incident examples

### 7. Run Agent Guide

```
.claude/commands/run-agent.md
```

Contains:
- Complete tmux interaction guide
- Phase-by-phase workflows
- Agent-specific procedures
- Troubleshooting
- Quick examples

---

## Report

After reading all files, confirm initialization:

```
✅ Orchestrator context loaded successfully!

Loaded:
- System guardrails (prompts/system.md)
- Technical details (prompts/developer.md)
- User interaction patterns (prompts/user.md)
- Skills quick reference (.claude/skills/SKILL.md)
- Coordination workflows (.claude/skills/WORKFLOW.md)
- Agent interaction rules (.claude/AGENT-INTERACTION-CRITICAL-RULES.md)
- Run agent guide (.claude/commands/run-agent.md)

I'm ready to coordinate builder agents:
- Goal Builder (GitHub issues → Linear goals)
- Plan Builder (Linear goals → Implementation plans)
- Module Builder (Plans → Feature modules)

Key capabilities confirmed:
✅ Know how to launch agents via tmux
✅ Know all agent slash commands
✅ Know two-step command sending (text, then C-m)
✅ Know auto-update pattern detection
✅ Know command translation (user intent → slash commands)
✅ Know when to load agent-specific context

What would you like to do?
1. Create a goal from GitHub issues
2. Create a plan from an existing goal
3. Build a module from an existing plan
4. Explain the full workflow
```

---

## What This Loads

### Universal Orchestrator Knowledge

- **Role**: Relay/coordinator, NOT a builder
- **Method**: TMux sessions with builder agents
- **Pattern**: ALWAYS use agent slash commands
- **Rule**: NEVER run scripts or access APIs directly
- **Technique**: Two-step tmux command sending
- **Skill**: Auto-update pattern detection
- **Approach**: Confirm at decision points

### Agent Command Catalogs

**Goal Builder** (when in goal-builder session):
- `/prime`
- `/show-issues`
- `/show-drafts`
- `/analyze-issues`
- `/create-goal [numbers] [--auto-update]`
- `/edit-draft [goal-id] [--auto-update]`
- `/save-draft [filename]`

**Plan Builder** (when in plan-builder session):
- `/prime`
- `/show-goals`
- `/analyze-goal [goal-id]`
- `/create-plan [goal-id] [--auto-update]`

**Module Builder** (when in module-builder session):
- `/prime`
- `/show-plans`
- `/load-plan [plan-id]`
- `/mark-complete [plan-id]`

### Critical Patterns

**Two-Step Command Sending:**
```bash
tmux send-keys -t session "text"    # Step 1
tmux send-keys -t session C-m        # Step 2
```

**Auto-Update Detection:**
- "do X and create/update/push"
- "do X then create/update"
- "don't ask me again"
- "no need to confirm"

**Command Translation:**
- See AGENT-INTERACTION-CRITICAL-RULES.md for complete translation patterns and examples

---

## After Prime

### Immediately Available

You can now:
- Launch any builder agent via tmux
- Translate user intent to agent commands
- Detect auto-update patterns
- Coordinate multi-agent workflows
- Handle errors appropriately

### When Working With a Specific Agent

Before sending commands to an agent, load its specific context using the Read tool:

```
Read:
- ../goal-builder/CLAUDE.md
- ../goal-builder/.claude/skills/SKILL.md
- ../goal-builder/.claude/skills/WORKFLOW.md
```

This ensures you know:
- Agent's complete command set
- Agent's workflow details
- Agent's capabilities and limitations

---

## Error Prevention

### Common Mistakes to Avoid

❌ **Sending commands before loading context**
```
User: "create a goal"
You: [Try to do it yourself without loading context]
WRONG! Run /prime first!
```

✅ **Correct approach:**
```
Session starts
You: Run /prime immediately
You: Load universal orchestrator context
You: Ready to coordinate agents
User: "create a goal"
You: Load goal-builder context
You: Launch goal-builder via tmux
You: Send /create-goal to goal-builder session
```

❌ **Forgetting two-step command sending**
```bash
tmux send-keys -t session "text" C-m  # WRONG!
```

✅ **Correct:**
```bash
tmux send-keys -t session "text"
tmux send-keys -t session C-m
```

❌ **Missing auto-update patterns**
```
User: "Fix this and push to Linear"
You: Send normal command [agent will ask for approval]
WRONG! Should detect auto-update pattern!
```

✅ **Correct:**
```
User: "Fix this and push to Linear"
You: Detect "and push" = complete instruction = AUTO-UPDATE
You: Send with --auto-update flag OR switch signal
```

---

## Remember

**/prime is your foundation. Without it, you're flying blind.**

Run it FIRST, EVERY session. No exceptions.
