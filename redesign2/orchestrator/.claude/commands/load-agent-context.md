---
description: Load specific agent's documentation and commands
argument-hint: [goal-builder|plan-builder|module-builder]
disable-model-invocation: false
---

# Load Agent Context

Load a specific builder agent's documentation to understand its commands, workflows, and capabilities.

**Use this BEFORE launching and working with an agent.**

---

## Usage

```
/load-agent-context goal-builder
/load-agent-context plan-builder
/load-agent-context module-builder
```

---

## What This Does

For the specified agent, reads these files:

### Core Files (Always Load)

1. **`../{agent}/CLAUDE.md`** - Agent overview and role
2. **`../{agent}/.claude/skills/SKILL.md`** - Quick reference, all commands
3. **`../{agent}/.claude/skills/WORKFLOW.md`** - Step-by-step procedures

From these files, extract and memorize:
- ✅ All slash commands available (e.g., `/show-issues`, `/create-goal`)
- ✅ When to use each command
- ✅ Agent's primary workflows
- ✅ What agent can and cannot do
- ✅ MCP servers agent uses
- ✅ File locations agent works with

### Why Not Load Commands/ Directory?

The agent's `.claude/commands/` directory contains detailed command implementations (200-400 lines each). We DON'T load these because:

1. **Agent Loads Them**: When you send a command to the agent via tmux, the AGENT loads its own command file
2. **Too Much Context**: Loading 6-7 command files = 1200-2800 lines per agent
3. **Already Documented**: SKILL.md lists all commands, WORKFLOW.md shows procedures
4. **settings.json Has Details**: Orchestrator's settings.json documents all agent commands with full syntax

**You only need to know:**
- ✅ WHAT commands exist (from SKILL.md)
- ✅ WHEN to use them (from WORKFLOW.md)
- ✅ HOW to invoke them (from settings.json)

The agent handles the "HOW to execute them" part.

### Optional: Load Specific Commands (Advanced)

If you need detailed information about a specific command:

```
Read: ../{agent}/.claude/commands/{command-name}.md
```

**Example**: If user asks complex question about auto-update mode in goal creation:
```
Read: ../goal-builder/.claude/commands/create-goal.md
```

This gives you the FULL command workflow, but is usually not needed.

---

## Arguments

### If NO arguments provided:

Show available agents:

```
Please specify which agent to load:

/load-agent-context goal-builder
/load-agent-context plan-builder
/load-agent-context module-builder
```

### If agent name provided:

#### Step 1: Validate Agent Exists

Check if agent directory exists:
```bash
Agent: {agent}
Directory: ../{agent}/
```

If directory doesn't exist, show error:
```
❌ Agent '{agent}' not found.

Available agents:
- goal-builder (../goal-builder/)
- plan-builder (../plan-builder/)
- module-builder (../module-builder/)

Please specify a valid agent.
```

#### Step 2: Read Agent Files

Use Read tool to load all three files:

```
Read: ../{agent}/CLAUDE.md
Read: ../{agent}/.claude/skills/SKILL.md
Read: ../{agent}/.claude/skills/WORKFLOW.md
```

If any file is missing, show error:
```
⚠️ Agent '{agent}' is incomplete.

Missing files:
- ../{agent}/CLAUDE.md [FOUND/MISSING]
- ../{agent}/.claude/skills/SKILL.md [FOUND/MISSING]
- ../{agent}/.claude/skills/WORKFLOW.md [FOUND/MISSING]

Please check the agent workspace.
```

#### Step 3: Confirm Success

After successfully reading all files, report:

```
✅ Loaded {agent} context successfully!

Read files:
- {agent}/CLAUDE.md - Agent overview
- {agent}/.claude/skills/SKILL.md - Commands and quick reference
- {agent}/.claude/skills/WORKFLOW.md - Detailed procedures

Key information extracted:
- All available slash commands (e.g., /show-issues, /create-goal)
- Argument requirements
- Workflow procedures
- Capabilities and limitations

I'm now ready to:
✅ Launch {agent} via tmux
✅ Send commands to {agent} (e.g., /show-issues)
✅ Coordinate {agent}'s workflow end-to-end

What would you like the {agent} to do?
```

---

## When to Use

### Before Launching an Agent

```
User: "Create a goal from issue #11"

You:
1. /load-agent-context goal-builder
2. [Read and memorize goal-builder's commands]
3. Launch goal-builder via tmux
4. Send /create-goal 11 to goal-builder session
```

### When Switching Agents

```
Currently: Working with goal-builder
User: "Now create a plan for that goal"

You:
1. /load-agent-context plan-builder
2. [Read and memorize plan-builder's commands]
3. Launch plan-builder via tmux
4. Send /create-plan SYS-10 to plan-builder session
```

### When Uncertain About Commands

```
You: Not sure if goal-builder has a specific command

You:
1. /load-agent-context goal-builder
2. [Read SKILL.md to see all commands]
3. Send the correct command to goal-builder
```

---

## Integration with /prime

**`/prime`** loads universal orchestrator knowledge (how to coordinate any agent).

**`/load-agent-context`** loads specific agent knowledge (what this agent can do).

### Complete Workflow:

```
Session Start
    ↓
/prime (load orchestrator's universal context)
    ↓
User wants to work with goal-builder
    ↓
/load-agent-context goal-builder (load goal-builder specifics)
    ↓
Launch goal-builder via tmux
    ↓
Send commands like /show-issues, /create-goal to goal-builder session
```

---

## Error Handling

### Agent Directory Not Found

```
❌ Agent 'invalid-name' not found at ../invalid-name/

Valid agents are:
- goal-builder
- plan-builder
- module-builder
```

### Agent Files Incomplete

```
⚠️ Agent 'goal-builder' workspace is incomplete.

Expected:
- ../goal-builder/CLAUDE.md ❌ MISSING
- ../goal-builder/.claude/skills/SKILL.md ✅ FOUND
- ../goal-builder/.claude/skills/WORKFLOW.md ✅ FOUND

Cannot load context. Please check agent setup.
```

### Permission Issues

```
⚠️ Cannot read agent files.

Check permissions for:
- ../goal-builder/ directory
```

---

## Best Practices

### DO:
- ✅ Load agent context BEFORE launching the agent
- ✅ Load context when user asks to work with a new agent
- ✅ Re-load if you need to verify available commands

### DON'T:
- ❌ Launch agents without loading their context first
- ❌ Guess at agent commands (always load context!)
- ❌ Assume you remember commands from previous sessions

---

## Remember

**This command ensures you ALWAYS know:**
- Exact command syntax for the agent
- All available features
- Complete workflow steps
- Agent's capabilities and limitations

**Never coordinate an agent blindly. Always load its context first!**
