# Mixer System V3 - Migration to Isolated Workspaces

## Overview

The Mixer System has been restructured from a shared workspace model to isolated agent workspaces. Each agent now operates in its own self-contained environment with only the resources it needs.

## What Changed

### Before (V2)
```
hey-mixer/
├── CLAUDE.md               # Single shared instructions (all agents)
├── .claude/
│   ├── commands/          # All commands visible to all agents
│   ├── scripts/           # All scripts accessible to all agents
│   └── skills/            # All skills shared
├── agents/                # Agent definitions
├── config.yaml
└── .env
```

**Problems:**
- All agents saw all commands (confusion)
- Single CLAUDE.md became bloated
- Cross-contamination of context
- Difficult to maintain and update individual agents

### After (V3)
```
redesign/
├── orchestrator/          # Main coordinator agent
│   ├── CLAUDE.md         # Orchestrator-specific instructions
│   ├── .claude/          # Only orchestrator commands
│   ├── config.yaml       # Symlink to shared config
│   └── .env             # Symlink to shared env
│
├── goal-builder/         # Isolated goal-builder workspace
│   ├── CLAUDE.md        # Only goal-builder instructions
│   ├── .claude/          # Only goal-builder resources
│   ├── config.yaml      # Symlink to shared config
│   └── .env            # Symlink to shared env
│
├── plan-builder/        # Isolated plan-builder workspace
│   └── [similar structure]
│
└── module-builder/      # Isolated module-builder workspace
    └── [similar structure]
```

**Benefits:**
- Complete isolation - each agent only sees its own resources
- Focused CLAUDE.md per agent
- No command confusion
- Easy to maintain and update individual agents
- Clear separation of concerns

## How to Use

### Starting the Orchestrator (Main Agent)
```bash
cd redesign
./mixer.sh orchestrator
```
This launches the main Claude Code instance that coordinates all sub-agents.

### Starting Individual Agents (Direct Access)
```bash
cd redesign
./mixer.sh goal-builder    # Work with GitHub issues → Linear goals
./mixer.sh plan-builder    # Transform goals → implementation plans
./mixer.sh module-builder  # Transform plans → working code
```

## Orchestrator Workflow

The orchestrator is your main interface. It:
1. Launches sub-agents in tmux sessions
2. Translates your requests into agent commands
3. Relays responses back to you
4. Never executes agent logic directly

Example interaction:
```
You: "Create a goal from issue #11"
Orchestrator: [Launches goal-builder in tmux]
Orchestrator: [Sends /goal-builder:create-goal 11]
Orchestrator: [Relays agent's draft back to you]
You: "Looks good, create it"
Orchestrator: [Relays approval to agent]
```

## Key Concepts

### Workspace Isolation
Each agent runs in its own directory with:
- Its own CLAUDE.md instructions
- Its own .claude/commands/ directory
- Its own .claude/scripts/{agent}/ directory
- Symlinked access to shared utilities

### Shared Resources
These resources are symlinked to all workspaces:
- `config.yaml` - Configuration file
- `.env` - Environment variables
- `.claude/scripts/shared/` - Shared Python utilities (Linear/GitHub clients)

### Command Translation
The orchestrator ALWAYS translates user intent into slash commands:
- "show issues" → `/goal-builder:show-issues`
- "create goal" → `/goal-builder:create-goal`
- User says "A" (from menu) → Actual command

### Auto-Update Mode
When users want to skip approval prompts:
- Pattern: "Do X and create/update in Linear"
- Pattern: "Don't ask me again"
- Orchestrator adds `--auto-update` flag or sends `SWITCH TO AUTO-UPDATE MODE`

## Critical Rules

### For the Orchestrator
- **YOU ARE NOT THE AGENT** - You're just a relay
- Never run Python scripts directly
- Never access APIs yourself
- Always use agent slash commands
- Always wait for user approval (unless auto-update mode)

### For Sub-Agents
- Work only in your isolated workspace
- Process only your designated ticket types
- Follow your specific workflow rules
- Don't know about other agents

## File Structure Details

### Each Agent Workspace Contains:

```
{agent-name}/
├── CLAUDE.md                          # Agent-specific instructions
├── agents/{agent-name}/
│   ├── run.sh                        # Launch script
│   └── system-prompt.md              # Agent personality
├── .claude/
│   ├── commands/{agent-name}/        # Agent's slash commands
│   ├── scripts/
│   │   ├── {agent-name}/             # Agent's Python scripts
│   │   └── shared/                   # Symlink to shared utilities
│   └── skills/{agent-name}/          # Agent's skill files (if any)
├── config.yaml                        # Symlink to project config
└── .env                              # Symlink to project env
```

## Migration Checklist

If migrating from old structure:

- [x] All agent commands copied to respective workspaces
- [x] All agent scripts copied to respective workspaces
- [x] All agent skills copied to respective workspaces
- [x] CLAUDE.md split into focused versions per agent
- [x] Symlinks created for shared resources
- [x] run.sh scripts updated to use workspace paths
- [x] mixer.sh launcher created for new structure
- [x] Orchestrator workspace created with coordination logic

## Testing

To verify the migration worked:

1. **Test launcher:**
   ```bash
   cd redesign
   ./mixer.sh  # Should show help with all agents
   ```

2. **Test workspace isolation:**
   ```bash
   ls redesign/goal-builder/.claude/commands/
   # Should only show goal-builder commands
   ```

3. **Test symlinks:**
   ```bash
   ls -la redesign/goal-builder/config.yaml
   # Should point to project root config
   ```

4. **Test Python imports:**
   ```bash
   cd redesign/goal-builder
   python3 -c "from .claude.scripts.shared.linear_client import LinearClient"
   # Should import successfully
   ```

## Rollback

If you need to rollback:
1. The original structure is preserved at project root
2. Use `./mixer.sh` (original) instead of `redesign/mixer.sh`
3. All original files remain untouched

## Future Improvements

- Add more agents easily by creating new isolated workspaces
- Update individual agents without affecting others
- Version agent workspaces independently
- Add agent-specific configuration files