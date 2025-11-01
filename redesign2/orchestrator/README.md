# Orchestrator Agent

<!-- PURPOSE: User guide for orchestrator - how to coordinate builder agents -->
<!-- AUDIENCE: Users and developers using the orchestrator -->

The command center for coordinating all Mixer builder agents.

## What is This?

The Orchestrator is your main interface to the Mixer system. It coordinates three specialized builder agents that work together to transform GitHub issues into working code:

```
GitHub Issues → [Goal Builder] → Linear Goals
               ↓
Linear Goals → [Plan Builder] → Implementation Plans
              ↓
Plans → [Module Builder] → Feature Code
```

**You talk to the Orchestrator. The Orchestrator talks to the builders.**

## Quick Start

```bash
# 1. Launch the orchestrator
./run.sh

# 2. Initialize context (REQUIRED!)
/prime

# 3. Start working
# The orchestrator will guide you through the workflow
```

## The Orchestrator's Job

The orchestrator is **NOT a builder** - it's a **coordinator**. It:

1. **Understands** your intent
2. **Knows** which builder agent to use
3. **Launches** the appropriate agent via tmux
4. **Translates** your requests into agent commands
5. **Relays** messages between you and the agent
6. **Monitors** progress
7. **Reports** results

**It NEVER builds anything itself.** It coordinates those who do.

## Available Commands

| Command | Purpose |
|---------|---------|
| `/prime` | Load all orchestrator context (RUN THIS FIRST!) |
| `/load-agent-context [agent]` | Load specific agent's documentation |

The orchestrator also uses standard tools (Bash, tmux, Read) to coordinate agents.

## The Three Builder Agents

### Goal Builder
- **Input**: GitHub issues
- **Output**: Linear goal tickets (draft status)
- **Purpose**: Transform raw ideas into structured goals

### Plan Builder
- **Input**: Linear goals (todo status)
- **Output**: Linear plan tickets
- **Purpose**: Design implementation approach

### Module Builder
- **Input**: Linear plans (todo status)
- **Output**: Feature code in modules/
- **Purpose**: Build the actual implementation

## How It Works

### Example: Creating a Goal

```
You: "Create a goal from GitHub issue #11"

Orchestrator:
1. Runs /load-agent-context goal-builder
2. Learns goal-builder's commands and workflow
3. Launches goal-builder via tmux
4. Sends: /create-goal 11
5. Relays agent's questions to you
6. Relays your answers to agent
7. Reports when goal is created

Result: Goal created in Linear, issue closed in GitHub
```

### Example: Full Pipeline

```
You: "Take issue #11 all the way to code"

Orchestrator:
1. Creates goal from issue #11 (goal-builder)
2. Waits for you to approve goal in Linear
3. Creates plan from goal (plan-builder)
4. Implements plan (module-builder)
5. Marks everything as done

Result: Working feature module in modules/
```

## Critical Rules

The orchestrator follows these strict rules:

### NEVER:
- ❌ Run builder scripts directly
- ❌ Access GitHub/Linear APIs itself
- ❌ Create goals/plans/modules
- ❌ Send generic text when commands exist
- ❌ Make decisions without confirming with you

### ALWAYS:
- ✅ Launch builders via tmux
- ✅ Use builder slash commands (e.g., `/show-issues` when in goal-builder)
- ✅ Two-step command sending (text, then Enter separately)
- ✅ Translate your intent into proper commands
- ✅ Detect auto-update patterns
- ✅ Confirm at decision points

## Command Translation

The orchestrator automatically translates your natural language into builder commands:

| You Say | Orchestrator Sends (to goal-builder) |
|---------|-------------------|
| "show me the issues" | `/show-issues` |
| "create a goal from issue 11" | `/create-goal 11` |
| "edit draft SYS-10" | `/edit-draft SYS-10` |

| You Say | Orchestrator Sends (to plan-builder) |
|---------|-------------------|
| "show goals" | `/show-goals` |
| "create plan for SYS-10" | `/create-plan SYS-10` |

**You never need to remember the exact command syntax!**

## Auto-Update Detection

The orchestrator detects when you want to skip approval prompts:

**Patterns it recognizes:**
- "do X and create/update/push"
- "fix X then update"
- "don't ask me again"
- "auto-update"
- "skip approval"

**What it does:**
Adds `--auto-update` flag to commands OR sends mid-workflow switch signal.

**Example:**
```
You: "Fix the YAML and push to Linear"
Orchestrator detects: "and push" = complete instruction
Orchestrator sends: "SWITCH TO AUTO-UPDATE MODE: Fix YAML and push to Linear"
Agent: Updates immediately without asking
```

## Architecture

```
orchestrator/
├── CLAUDE.md                    # Bootstrap (auto-loaded)
├── README.md                    # This file
├── .claude/
│   ├── AGENT-INTERACTION-CRITICAL-RULES.md  # How to relay to agents
│   ├── commands/
│   │   ├── prime.md             # Context loader
│   │   ├── load-agent-context.md # Agent doc loader
│   │   └── run-agent.md         # TMux coordination guide
│   ├── skills/
│   │   ├── SKILL.md             # Quick reference
│   │   └── WORKFLOW.md          # Detailed procedures
│   └── settings.json            # Configuration
├── prompts/
│   ├── system.md                # Guardrails
│   ├── developer.md             # Technical details (tmux, paths)
│   └── user.md                  # Conversation patterns
└── out/.tmp/                    # Working directory
```

## Workflow

### Typical Session

```
1. You launch orchestrator: ./run.sh
2. Orchestrator runs: /prime (loads all context)
3. You say: "Create a goal from issue #11"
4. Orchestrator loads: goal-builder context
5. Orchestrator launches: goal-builder via tmux
6. Orchestrator coordinates: Interactive goal creation
7. You approve: "looks good"
8. Orchestrator confirms: Goal created!
```

### Multi-Agent Coordination

The orchestrator can run multiple agents in sequence:

```
Phase 1: goal-builder creates goal SYS-10
  ↓
Phase 2: plan-builder creates plan PLAN-45 for SYS-10
  ↓
Phase 3: module-builder implements PLAN-45
  ↓
Result: Feature complete!
```

## Troubleshooting

### "Context not loaded"
**Solution**: Run `/prime` first - this is REQUIRED at session start

### "Agent session failed"
**Solution**:
- Check if agent directory exists (`../goal-builder/`)
- Verify .env has GITHUB_TOKEN and LINEAR_API_KEY
- Check agent run.sh script exists

### "Commands not recognized"
**Solution**: Load agent context first: `/load-agent-context goal-builder`

### "Agent not responding"
**Solution**:
- Wait 10-20 seconds (agents take time to process)
- Send C-m again via tmux
- Check tmux session output for errors

## Best Practices

### DO:
- ✅ Run `/prime` at every session start
- ✅ Load agent context before working with it
- ✅ Let orchestrator translate commands for you
- ✅ Provide clear intent ("create goal from issue 11")
- ✅ Wait for orchestrator confirmation before next step

### DON'T:
- ❌ Skip `/prime` at startup
- ❌ Try to run builder scripts yourself
- ❌ Work with builders directly (go through orchestrator)
- ❌ Use generic requests when you want specific actions

## Related Documentation

- **ARCHITECTURE.md** (in ../): Complete multi-agent system design
- **.claude/AGENT-INTERACTION-CRITICAL-RULES.md**: How relaying works
- **.claude/commands/run-agent.md**: TMux coordination details
- **prompts/system.md**: Orchestrator guardrails
- **.claude/skills/WORKFLOW.md**: Complete coordination procedures

## Integration with Builders

The orchestrator integrates with:

- **goal-builder** at `../goal-builder/`
- **plan-builder** at `../plan-builder/`
- **module-builder** at `../module-builder/`

Each builder is a self-contained workspace with its own commands, skills, and workflows.

## Remember

**The orchestrator is your interface to the entire Mixer system.**

You don't need to know:
- Exact command syntax for each builder
- How tmux sessions work
- How to coordinate multiple agents
- When to detect auto-update patterns

**The orchestrator handles all of that for you.**

Just tell it what you want to accomplish, and it coordinates the rest.

---

**Ready to start?** Run `./run.sh` and type `/prime` 🚀
