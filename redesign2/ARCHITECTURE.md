# Mixer Multi-Agent System Architecture

## System Overview

The Mixer System is a multi-agent conversational AI architecture that transforms ideas into working code through structured project management. It uses **four specialized Claude agents** working in coordination:

```
          ┌─────────────────┐
          │  Orchestrator   │ ← You talk to this agent
          │   (Coordinator) │
          └────────┬────────┘
                   │
       ┌───────────┼───────────┐
       │           │           │
       ▼           ▼           ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│  Goal    │ │  Plan    │ │  Module  │
│ Builder  │ │ Builder  │ │ Builder  │
└──────────┘ └──────────┘ └──────────┘
```

**Data Flow:**
```
GitHub Issues → Goal Builder → Linear Goals (draft)
                                     ↓ (user approves: draft→todo)
                            Plan Builder → Linear Plans (draft)
                                                ↓ (user approves: draft→todo)
                                       Module Builder → Feature Code
                                                            ↓
                                                   Mark goal/plan as "done"
```

---

## The Four Agents

### 1. Orchestrator (Your Interface)

**Location**: `redesign2/orchestrator/`

**Role**: Command center and coordinator - NOT a builder!

**Responsibilities**:
- Understand user intent
- Launch appropriate builder agents via tmux
- Translate natural language → slash commands
- Relay messages between user and agents
- Monitor agent progress
- Detect auto-update patterns
- Report results

**What It NEVER Does**:
- ❌ Create goals, plans, or modules itself
- ❌ Access GitHub/Linear APIs directly
- ❌ Run builder scripts
- ❌ Edit files in builder workspaces

**Key Commands**:
- `/prime` - Load all orchestrator context (REQUIRED at startup)
- `/load-agent-context [agent]` - Load specific agent's documentation

**Why Orchestrator is Simpler**:
The orchestrator has fewer files than builder agents because it's a **coordinator, not a builder**:
- No MCP integrations (uses tmux to talk to agents)
- No content templates (doesn't create tickets)
- No adapters (doesn't transform data)
- Simpler workflows (relay messages, don't process them)

This intentional simplicity keeps the orchestrator focused on its single job: coordination.

**Files**:
```
orchestrator/
├── CLAUDE.md                    # Bootstrap (auto-loaded)
├── README.md                    # User guide
├── .claude/
│   ├── AGENT-INTERACTION-CRITICAL-RULES.md  # Relay rules
│   ├── commands/
│   │   ├── prime.md             # Context loader
│   │   ├── load-agent-context.md # Agent doc loader
│   │   └── run-agent.md         # TMux coordination guide
│   ├── skills/
│   │   ├── SKILL.md             # Quick reference
│   │   └── WORKFLOW.md          # Coordination procedures
│   └── settings.json
├── prompts/
│   ├── system.md                # Guardrails
│   ├── developer.md             # TMux patterns, paths
│   └── user.md                  # Conversation templates
└── .tmp/                        # Working directory
```

---

### 2. Goal Builder (GitHub → Linear Goals)

**Location**: `redesign2/goal-builder/`

**Input**: GitHub issues (raw ideas), existing Linear goal drafts

**Output**: Linear goal tickets (status="draft")

**Purpose**: Transform GitHub issues into well-defined goals, edit/refine existing goal drafts, combine multiple issues into unified goals, and innovate on requirements.

**What It Does**:
- ✅ Create new goals from single or multiple GitHub issues
- ✅ Edit and refine existing goal drafts in Linear
- ✅ Analyze issues and suggest logical groupings
- ✅ Combine related issues into one comprehensive goal
- ✅ Innovate on existing goals with new requirements
- ✅ Maintain complete version history with automatic diffs

**Workflow**:
1. Show open GitHub issues OR existing goal drafts
2. Analyze and suggest groupings (optional)
3. Interactively draft or edit goal content WITH user
4. Create version history (v1, v2, v3...) with automatic diffs
5. Save to Linear as "draft" status (or update existing draft)
6. Close source GitHub issues (when creating new goals)

**Key Commands**:
- `/show-issues` - List GitHub issues
- `/show-drafts` - List draft goals
- `/analyze-issues` - Suggest groupings
- `/create-goal [numbers]` - Create goal from issues
- `/edit-draft [goal-id]` - Edit existing draft
- `/save-draft [filename]` - Save to file

**Unique Features**:
- **Version Management**: Automatic v1, v2, v3... with diff generation
- **Archive System**: Complete audit trail in `.tmp/archives/{GOAL-ID}/{TIMESTAMP}/`
- **Auto-Update Mode**: Skip approval prompts when user requests (via `--auto-update` flag)

**Files**:
```
goal-builder/
├── CLAUDE.md                    # Bootstrap
├── README.md                    # Complete guide
├── .claude/
│   ├── commands/
│   │   ├── prime.md
│   │   ├── show-issues.md
│   │   ├── show-drafts.md
│   │   ├── create-goal.md
│   │   └── edit-draft.md
│   ├── skills/
│   │   ├── SKILL.md             # Quick reference
│   │   └── WORKFLOW.md          # Detailed procedures
│   └── settings.json
├── prompts/
│   ├── system.md                # Behavior and guardrails
│   ├── developer.md             # Technical critical info
│   └── user.md                  # Conversation patterns
└── .tmp/                        # Draft workspace
```

---

### 3. Plan Builder (Goals → Implementation Plans)

**Location**: `redesign2/plan-builder/`

**Input**: Linear goals (status="todo"), existing Linear plan drafts

**Output**: Linear plan tickets (status="draft")

**Purpose**: Transform goals into detailed implementation plans, refine/iterate on plan drafts, and design technical approaches with task breakdowns and architecture decisions.

**What It Does**:
- ✅ Create new plans from Linear goals
- ✅ Edit and refine existing plan drafts
- ✅ Analyze goals and suggest implementation approaches
- ✅ Break down goals into concrete technical tasks
- ✅ Update plans based on changing requirements
- ✅ Design architecture and technical specifications

**Workflow**:
1. Show goals with status="todo" OR existing plan drafts
2. Analyze selected goal/plan (optional)
3. Interactively draft or edit plan WITH user
4. Create in Linear as "draft" status (or update existing draft)
5. Link plan to parent goal (when creating new plans)
6. Update goal status to "doing" (when creating new plans)

**Key Commands**:
- `/show-goals` - List todo goals
- `/analyze-goal [goal-id]` - Analyze goal
- `/create-plan [goal-id]` - Create plan

**Files**:
```
plan-builder/
├── CLAUDE.md
├── README.md
├── .claude/
│   ├── commands/
│   │   ├── prime.md
│   │   ├── show-goals.md
│   │   ├── analyze-goal.md
│   │   └── create-plan.md
│   ├── skills/
│   │   ├── SKILL.md
│   │   └── WORKFLOW.md
│   └── settings.json
├── prompts/
│   ├── system.md
│   ├── developer.md
│   └── user.md
└── .tmp/
```

---

### 4. Module Builder (Plans → Feature Code)

**Location**: `redesign2/module-builder/`

**Input**: Linear plans (status="todo"), existing code modules

**Output**: Feature code in `modules/` directory

**Purpose**: Implement code based on plan specifications, update/refine existing modules, and create self-contained feature modules.

**What It Does**:
- ✅ Implement new features from Linear plans
- ✅ Update and refine existing code modules
- ✅ Fix bugs in implemented modules
- ✅ Refactor modules based on new requirements
- ✅ Mark plans and parent goals as complete
- ✅ Ensure module quality and testing

**Workflow**:
1. Show plans with status="todo" OR existing modules
2. Load selected plan
3. Implement or update feature module
4. Test and verify implementation
5. Update plan status to "done"
6. Update parent goal status to "done"

**Key Commands**:
- `/show-plans` - List todo plans
- `/load-plan [plan-id]` - Load and implement
- `/mark-complete [plan-id]` - Mark done

**Files**:
```
module-builder/
├── CLAUDE.md
├── README.md
├── .claude/
│   ├── commands/
│   │   ├── prime.md
│   │   ├── show-plans.md
│   │   ├── load-plan.md
│   │   └── mark-complete.md
│   ├── skills/
│   │   ├── SKILL.md
│   │   └── WORKFLOW.md
│   └── settings.json
├── prompts/
│   ├── system.md
│   ├── developer.md
│   └── user.md
└── .tmp/
```

---

## Orchestrator Coordination Model

### The Relay Pattern

The orchestrator operates as a **relay agent**, not a builder:

```
User Request: "Create a goal from issue #11"
       ↓
Orchestrator:
  1. Loads goal-builder context (/load-agent-context goal-builder)
  2. Learns all goal-builder commands and workflows
  3. Launches goal-builder via tmux
  4. Translates request → /create-goal 11
  5. Sends command to agent in tmux
  6. Monitors agent output via tmux capture-pane
  7. Relays agent questions/responses to user
  8. Relays user answers to agent
  9. Reports final result
```

### Command Translation

The orchestrator **automatically translates** natural language to slash commands:

| User Says | Orchestrator Sends (to agent session) |
|-----------|-------------------|
| "show me the issues" | `/show-issues` |
| "create goal from issue 11" | `/create-goal 11` |
| "edit draft SYS-10" | `/edit-draft SYS-10` |
| "show goals" | `/show-goals` |
| "create plan for SYS-10" | `/create-plan SYS-10` |

**You never need to remember exact command syntax!**

### Auto-Update Pattern Detection

The orchestrator detects when users want to skip approval prompts:

**Patterns Recognized**:
- "do X and create/update/push"
- "do X then create/update"
- "fix X and push to Linear"
- "don't ask me again"
- "auto-update" / "skip approval"

**Action**: Adds `--auto-update` flag to commands OR sends mid-workflow switch signal.

**Example**:
```
User: "Fix the YAML and push to Linear"
Orchestrator detects: "and push" = complete instruction
Orchestrator sends: "SWITCH TO AUTO-UPDATE MODE: Fix YAML and push to Linear."
Agent: Updates immediately without asking
```

### TMux Two-Step Command Sending (CRITICAL)

**Claude agents require TWO SEPARATE tmux operations:**

```bash
# ❌ WRONG - Will NOT work!
tmux send-keys -t session "text" C-m

# ✅ CORRECT - Must be two separate commands
tmux send-keys -t session "text"    # Step 1: Send text
tmux send-keys -t session C-m        # Step 2: Send Enter
```

**Why**: Claude agents wait for the FULL prompt before executing. Combining breaks this.

---

## Workflow Progression

### Complete Pipeline Example

```
1. User: "I want to build user authentication"
   ↓
2. User creates GitHub issue #45: "Implement user authentication"
   ↓
3. User (via orchestrator): "Create a goal from issue #45"
   ↓
4. Orchestrator launches goal-builder
   Goal Builder: Shows issue #45
   Goal Builder: Interactively drafts goal WITH user
   Goal Builder: Creates Linear goal SYS-10 (status="draft")
   Goal Builder: Closes GitHub issue #45
   ↓
5. User reviews SYS-10 in Linear
   User manually changes: draft → todo
   ↓
6. User (via orchestrator): "Create a plan for SYS-10"
   ↓
7. Orchestrator launches plan-builder
   Plan Builder: Loads goal SYS-10
   Plan Builder: Analyzes requirements
   Plan Builder: Interactively drafts plan WITH user
   Plan Builder: Creates Linear plan PLAN-25 (status="draft")
   Plan Builder: Links PLAN-25 → SYS-10 (parent)
   Plan Builder: Updates SYS-10 status to "doing"
   ↓
8. User reviews PLAN-25 in Linear
   User manually changes: draft → todo
   ↓
9. User (via orchestrator): "Implement PLAN-25"
   ↓
10. Orchestrator launches module-builder
    Module Builder: Loads plan PLAN-25
    Module Builder: Implements feature in modules/auth/
    Module Builder: Updates PLAN-25 status to "done"
    Module Builder: Updates SYS-10 status to "done"
    ↓
11. Result: Working authentication module in modules/auth/
```

### Status Transitions

```
Goals:  draft → [user] → todo → [plan created] → doing → [module complete] → done
Plans:  draft → [user] → todo → [module complete] → done
```

**Key Rule**: Only **users** manually transition draft→todo. All other transitions are automatic.

---

## Workspace Isolation Architecture

### The Problem Solved

Traditional monolithic agent systems suffer from:
- Context pollution (one agent knows too much)
- Role confusion (agent tries to do everything)
- Brittle workflows (changes affect entire system)
- Poor modularity (can't replace one component)

### The Solution: Self-Contained Workspaces

Each agent is **completely isolated**:

```
goal-builder/          ← Self-contained workspace
├── CLAUDE.md          ← Agent's identity
├── README.md          ← Agent's documentation
├── .claude/           ← Agent's commands and skills
├── prompts/           ← Agent's behavior
├── .tmp/              ← Agent's working directory
└── run.sh             ← Agent's launcher (in parent, not shown)

plan-builder/          ← Separate self-contained workspace
├── CLAUDE.md
├── ...                (same structure)

module-builder/        ← Separate self-contained workspace
├── CLAUDE.md
├── ...                (same structure)

orchestrator/          ← Coordinator workspace
├── CLAUDE.md
├── ...                (same structure, plus coordination files)
```

**Benefits**:
- ✅ **Clear Boundaries**: Each agent knows its role and nothing more
- ✅ **Independent Evolution**: Change one agent without affecting others
- ✅ **Parallel Development**: Multiple agents can be improved simultaneously
- ✅ **Easy Testing**: Test each agent in isolation
- ✅ **Simple Debugging**: Problems are localized to one agent
- ✅ **Replaceable Components**: Swap out agents without system-wide changes

### Shared Resources

While agents are isolated, they share:
- Configuration: `../shared/config.yaml`
- Credentials: `../shared/.env`
- Nothing else!

---

## Context Loading Patterns

### The /prime Pattern (Bulletproof Loading)

Every agent has a `/prime` command that **explicitly loads all context**:

```markdown
## Read

Read these files in order:

1. `prompts/system.md` - Core behavior and guardrails
2. `prompts/developer.md` - Technical details
3. `prompts/user.md` - Conversation patterns
4. `.claude/skills/SKILL.md` - Quick reference
5. `.claude/skills/WORKFLOW.md` - Complete procedures
```

**Why Explicit?**
- ❌ **Implicit loading** (relying on auto-discovery) = brittle
- ✅ **Explicit loading** (list exact files) = bulletproof
- Guarantees context is loaded correctly every time
- Easy to verify (check if /prime was run)
- Clear audit trail (see exactly what was loaded)

### Progressive Disclosure Hierarchy

```
Session Start
    ↓
CLAUDE.md (auto-loaded)
    ↓ (tells agent to run /prime)
/prime (loads all core context)
    ↓
Agent ready for basic operations
    ↓
User requests specific action
    ↓
Agent uses appropriate command
    ↓
Command loads additional context if needed
```

### Orchestrator Dynamic Context Loading

The orchestrator uses **on-demand agent context loading**:

```
User: "Create a goal from issue #11"
    ↓
Orchestrator: /load-agent-context goal-builder
    ↓
Reads:
  - ../goal-builder/CLAUDE.md
  - ../goal-builder/.claude/skills/SKILL.md
  - ../goal-builder/.claude/skills/WORKFLOW.md
    ↓
Learns all goal-builder commands, arguments, workflows
    ↓
Now ready to coordinate goal-builder effectively
```

**Why Dynamic?**
- Orchestrator doesn't need to know ALL agents upfront
- Agent context loaded only when needed
- Reduces orchestrator's initial context footprint
- Allows adding new agents without updating orchestrator

---

## File Organization Principles

### Why This Structure?

**1. CLAUDE.md (Bootstrap)**
- Auto-loaded by Claude Code at session start
- Minimal (< 100 lines)
- Says: "You are [role]. Run /prime first."
- Provides quick identity reference

**2. README.md (User Documentation)**
- For humans reading the workspace
- Explains agent's purpose, commands, workflows
- Quick start guide
- Not loaded by agent (too verbose)

**3. prompts/ (Behavior Files)**
- `system.md` - What agent can/cannot do, core rules
- `developer.md` - Technical details (API patterns, file paths, critical gotchas)
- `user.md` - Conversation templates, how to talk to users

**4. .claude/commands/ (Slash Commands)**
- Each command = one markdown file
- Defines arguments, workflow, error handling
- Commands coordinate multiple tools/scripts

**5. .claude/skills/ (Knowledge Base)**
- `SKILL.md` - Quick reference (commands, patterns, rules)
- `WORKFLOW.md` - Detailed step-by-step procedures
- Loaded by /prime for deep knowledge

**6. .claude/settings.json (Configuration)**
- Maps command names to files
- Defines skill paths
- MCP server configuration
- Metadata for commands

**7. .tmp/ (Working Directory)**
- Drafts, diffs, version files
- Temporary computation artifacts
- Cleaned up after success
- May have subdirectories (archives/, contexts/, sessions/)

### Design Principles

**Separation of Concerns**:
- Identity (CLAUDE.md) ≠ Behavior (prompts/) ≠ Operations (commands/)

**Single Source of Truth**:
- No information duplication across files
- Each file has one clear purpose

**Progressive Disclosure**:
- Start minimal, load more as needed
- Don't overwhelm with everything at once

**Explicit Over Implicit**:
- List exact files to read in /prime
- Don't rely on auto-discovery patterns

**Human-Readable Documentation**:
- README.md for people
- CLAUDE.md for bootstrapping
- prompts/ and .claude/ for deep agent knowledge

---

## Shared Resources Strategy

### What's Shared

```
redesign2/shared/
├── config.yaml        # GitHub repo, Linear workspace, team ID, labels
├── .env              # GITHUB_TOKEN, LINEAR_API_KEY
└── README.md         # Documentation on shared resources
```

### Why Shared?

**Configuration (config.yaml)**:
- All agents work with same GitHub repo
- All agents work with same Linear workspace
- Label conventions must be consistent
- Centralized = single point of update

**Credentials (.env)**:
- Same GitHub token for all agents
- Same Linear API key for all agents
- Security = one place to rotate tokens

### What's NOT Shared

- Agent identities (CLAUDE.md)
- Agent behaviors (prompts/)
- Agent commands (.claude/commands/)
- Agent skills (.claude/skills/)
- Agent working directories (.tmp/)

**Why Not Shared?**
- Maintains workspace isolation
- Allows independent evolution
- Prevents context pollution
- Enables parallel development

---

## TMux Interaction Architecture

### Why TMux?

**Problem**: Orchestrator needs to coordinate other Claude agents running in separate sessions.

**Solution**: Each builder agent runs in its own tmux session:

```bash
# Orchestrator launches goal-builder
tmux new-session -d -s goal-builder-session
tmux send-keys -t goal-builder-session "cd ../goal-builder && ./run.sh"
tmux send-keys -t goal-builder-session C-m
```

**Communication**:
- Send commands: `tmux send-keys -t goal-builder-session "/show-issues"`
- Capture output: `tmux capture-pane -t goal-builder-session -p`
- Monitor progress: Periodically capture and check output

**Benefits**:
- ✅ True multi-agent coordination
- ✅ Each agent has separate context
- ✅ No context bleeding between agents
- ✅ Can run multiple agents simultaneously
- ✅ User can attach to see live interaction

### Session Management

```bash
# Launch
tmux new-session -d -s goal-builder-session

# Send command (TWO STEPS!)
tmux send-keys -t goal-builder-session "text"
tmux send-keys -t goal-builder-session C-m

# Capture output
tmux capture-pane -t goal-builder-session -p

# Capture full history
tmux capture-pane -t goal-builder-session -p -S - > file.txt

# Kill when done
tmux kill-session -t goal-builder-session
```

---

## Directory Structure

### Complete View

```
redesign2/
├── shared/                      # Shared configuration
│   ├── config.yaml             # Repository and workspace settings
│   ├── .env                    # API tokens (GITHUB_TOKEN, LINEAR_API_KEY)
│   └── README.md               # Documentation
│
├── orchestrator/               # Multi-agent coordinator
│   ├── CLAUDE.md              # Bootstrap
│   ├── README.md              # User guide
│   ├── .claude/
│   │   ├── AGENT-INTERACTION-CRITICAL-RULES.md
│   │   ├── commands/
│   │   │   ├── prime.md
│   │   │   ├── load-agent-context.md
│   │   │   └── run-agent.md
│   │   ├── skills/
│   │   │   ├── SKILL.md
│   │   │   └── WORKFLOW.md
│   │   └── settings.json
│   ├── prompts/
│   │   ├── system.md
│   │   ├── developer.md
│   │   └── user.md
│   └── .tmp/
│
├── goal-builder/               # GitHub issues → Linear goals
│   ├── CLAUDE.md
│   ├── README.md
│   ├── .claude/
│   │   ├── commands/
│   │   │   ├── prime.md
│   │   │   ├── show-issues.md
│   │   │   ├── show-drafts.md
│   │   │   ├── analyze-issues.md
│   │   │   ├── create-goal.md
│   │   │   ├── edit-draft.md
│   │   │   └── save-draft.md
│   │   ├── skills/
│   │   │   ├── SKILL.md
│   │   │   └── WORKFLOW.md
│   │   └── settings.json
│   ├── prompts/
│   │   ├── system.md
│   │   ├── developer.md
│   │   └── user.md
│   └── .tmp/
│
├── plan-builder/               # Linear goals → Implementation plans
│   └── (Same structure as goal-builder)
│
├── module-builder/             # Plans → Code modules
│   └── (Same structure as goal-builder)
│
└── ARCHITECTURE.md             # This file
```

---

## Future: Migration to Root

### Current State (During Development)

```
mixer-backend/hey-mixer/
├── [old structure outside redesign2/]  ← Will be deleted
└── redesign2/                          ← New structure (this!)
    ├── orchestrator/
    ├── goal-builder/
    ├── plan-builder/
    ├── module-builder/
    ├── shared/
    └── ARCHITECTURE.md (this file)
```

### Future State (After Testing)

```
mixer-backend/hey-mixer/             ← redesign2/ becomes root
├── orchestrator/
├── goal-builder/
├── plan-builder/
├── module-builder/
├── shared/
└── ARCHITECTURE.md
```

**Migration Path**:
1. Complete development in `redesign2/`
2. Test entire system thoroughly
3. Verify all workflows work end-to-end
4. Delete old structure outside `redesign2/`
5. Move `redesign2/` contents to root
6. Update any absolute paths if needed
7. Verify everything still works

**No Root CLAUDE.md**:
- User will primarily talk to orchestrator
- Orchestrator coordinates all other agents
- No need for a "main project overview" CLAUDE.md
- This ARCHITECTURE.md serves as system-wide documentation

---

## Best Practices

### For Users

**DO**:
- ✅ Always talk to orchestrator (don't interact with builders directly)
- ✅ Let orchestrator translate your requests into commands
- ✅ Provide clear intent ("create goal from issue 11")
- ✅ Review draft tickets in Linear before transitioning to "todo"
- ✅ Wait for orchestrator confirmation before next step

**DON'T**:
- ❌ Try to run builder agents yourself
- ❌ Work with builders directly (go through orchestrator)
- ❌ Skip /prime at orchestrator startup
- ❌ Forget to manually transition draft→todo in Linear

### For Orchestrator

**DO**:
- ✅ Run `/prime` at every session start
- ✅ Load agent context before coordinating (`/load-agent-context [agent]`)
- ✅ Use two-step tmux command sending (text, then C-m)
- ✅ Detect auto-update patterns in user requests
- ✅ Translate natural language to slash commands
- ✅ Confirm at decision points

**DON'T**:
- ❌ Try to be a builder (you're a coordinator!)
- ❌ Run builder scripts directly
- ❌ Access GitHub/Linear APIs yourself
- ❌ Send generic text when commands exist
- ❌ Forget two-step command sending

### For Builders

**DO**:
- ✅ Run `/prime` immediately at startup
- ✅ Create tickets with status="draft"
- ✅ Write content interactively WITH user
- ✅ Use version management for observability
- ✅ Respect auto-update mode when flagged

**DON'T**:
- ❌ Create tickets with status="todo" (user decides)
- ❌ Auto-generate templates (write real content)
- ❌ Proceed without approval (unless auto-update mode)
- ❌ Forget to close source GitHub issues

---

## Troubleshooting

### Orchestrator Not Responding

**Symptoms**: Commands to orchestrator don't work

**Solutions**:
1. Run `/prime` first (REQUIRED!)
2. Verify orchestrator workspace files exist
3. Check settings.json for command mappings

### Agent Not Responding in TMux

**Symptoms**: Agent doesn't respond to commands

**Solutions**:
1. Wait 10-20 seconds (agents need time to process)
2. Send C-m again (might have missed it)
3. Check if agent is stuck (capture-pane to see output)
4. Verify two-step sending (text first, THEN C-m)

### Commands Not Recognized

**Symptoms**: "Command not found" or similar

**Solutions**:
1. Check if agent's context is loaded
2. For orchestrator: Run `/load-agent-context [agent]`
3. Verify command exists in agent's settings.json
4. Check command file exists in .claude/commands/

### Context Not Loaded

**Symptoms**: Agent doesn't know what to do

**Solutions**:
1. Run `/prime` (this is MANDATORY at session start)
2. Verify all files referenced in prime.md exist
3. Check for errors in prime command execution

---

## Summary

**The Mixer System** is a multi-agent architecture built on:

1. **Workspace Isolation** - Each agent is self-contained
2. **Orchestrator Coordination** - Central command center
3. **Bulletproof Context Loading** - Explicit /prime pattern
4. **TMux Multi-Agent Communication** - True agent separation
5. **Progressive Disclosure** - Load context as needed
6. **Clear Data Flow** - GitHub → Goals → Plans → Code

**Key Innovation**: Treating agent coordination as a relay pattern, not a monolithic system. The orchestrator doesn't "do" work - it coordinates specialists who do.

**Result**: Scalable, maintainable, testable multi-agent system where each component can evolve independently while working together seamlessly.

---

**Ready to start?** Launch orchestrator with `cd orchestrator && ./run.sh` and type `/prime` 🚀
