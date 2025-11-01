# Agent Development Guide

**Purpose**: Complete guide for building new agents in the Mixer system
**Audience**: Developers creating plan-builder, module-builder, or future agents
**Prerequisites**: Read ARCHITECTURE.md first for system overview

---

## Table of Contents

1. [Agent Architecture Principles](#agent-architecture-principles)
2. [Required vs Optional Files](#required-vs-optional-files)
3. [File Purposes and Loading Hierarchy](#file-purposes-and-loading-hierarchy)
4. [Bootstrap Pattern (CLAUDE.md)](#bootstrap-pattern-claudemd)
5. [Context Hierarchy (prompts/)](#context-hierarchy-prompts)
6. [/prime Implementation](#prime-implementation)
7. [Command Development](#command-development)
8. [SKILL.md Standard Format](#skillmd-standard-format)
9. [WORKFLOW.md Structure](#workflowmd-structure)
10. [MCP Integration](#mcp-integration)
11. [Orchestrator Integration](#orchestrator-integration)
12. [Testing and Validation Checklist](#testing-and-validation-checklist)

---

## Agent Architecture Principles

### 1. Workspace Isolation

**Rule**: Each agent is completely self-contained.

```
agent-name/
├── CLAUDE.md          # Bootstrap (agent knows its role)
├── README.md          # Human documentation
├── .claude/           # Commands, skills, settings
├── prompts/           # Behavior files
├── config.yaml →      # Symlink to ../shared/config.yaml
├── .env →             # Symlink to ../shared/.env
├── .tmp/              # Working directory
└── run.sh             # Launcher (in parent dir)
```

**Benefits**:
- No cross-contamination
- Independent evolution
- Easy testing
- Replaceable components

---

### 2. Progressive Disclosure

**Rule**: Load context incrementally, not all at once.

```
Session Start
    ↓
CLAUDE.md (auto-loaded, <30 lines)
    ↓
/prime (explicit loading of core context)
    ↓
Ready for basic operations
    ↓
Commands load additional context on-demand
```

**Why**: Efficient context usage, clear loading sequence, easy debugging

---

### 3. Single Source of Truth

**Rule**: Each piece of information lives in ONE authoritative location.

**Example**:
- Policies → `prompts/system.md` (NOT in WORKFLOW.md)
- MCP contracts → `prompts/developer.md` (NOT in commands/)
- Procedures → `.claude/skills/WORKFLOW.md` (NOT in system.md)
- Commands → `.claude/settings.json` (NOT in CLAUDE.md)

**Benefit**: No duplication = easy maintenance

---

### 4. Explicit Over Implicit

**Rule**: List exact files to load, don't rely on auto-discovery.

**Example** (`/prime` command):
```markdown
## Read

Read these files in order:

1. `prompts/system.md`
2. `prompts/developer.md`
3. `prompts/user.md`
4. `.claude/skills/SKILL.md`
5. `.claude/skills/WORKFLOW.md`
```

**Why**: Bulletproof loading, clear audit trail, no surprises

---

### 5. No Command Prefixes

**Rule**: Commands use clean names, agent identity comes from context.

```
✅ CORRECT:  /show-issues, /create-goal, /edit-draft
❌ WRONG:    /show-issues
```

**Rationale**:
- Tmux session name provides agent identity
- Commands can't collide (separate contexts)
- Cleaner syntax, less duplication

See: `redesign2/NO-PREFIX-RATIONALE.md`

---

## Required vs Optional Files

### Required Files (Every Agent Must Have)

| File | Purpose | Max Size |
|------|---------|----------|
| `CLAUDE.md` | Bootstrap instruction | <30 lines |
| `README.md` | Human documentation | Variable |
| `prompts/system.md` | Guardrails and policies | ~100-150 lines |
| `prompts/developer.md` | Technical contracts | ~100-200 lines |
| `prompts/user.md` | Greetings/conversation patterns | ~50-100 lines |
| `.claude/settings.json` | Command mappings, MCP config | Variable |
| `.claude/commands/prime.md` | Context loader | ~50-100 lines |
| `.claude/skills/SKILL.md` | Quick reference | <100 lines |
| `.claude/skills/WORKFLOW.md` | Detailed procedures | ~200-400 lines |
| `config.yaml` | Symlink to ../shared/ | N/A |
| `.env` | Symlink to ../shared/ | N/A |
| `.tmp/` | Working directory | N/A |

---

### Optional Files (Include If Needed)

| File | When to Include | Example Agent |
|------|-----------------|---------------|
| `AGENT.md` | Agent-specific deep docs (will merge into README) | goal-builder |
| `.claude/skills/TEMPLATES.md` | Content templates | goal-builder |
| `adapters/` directory | Data transformations | goal-builder |
| Agent-specific commands | Varies by function | All agents |
| Special rules file | Unique patterns (e.g. relay logic) | orchestrator (AGENT-INTERACTION-CRITICAL-RULES.md) |

---

## File Purposes and Loading Hierarchy

### Auto-Loaded (Claude Code reads at startup)
- **`CLAUDE.md`** - Bootstrap
  - Tells agent its role
  - Instructs to run /prime
  - <30 lines, minimal

---

### Loaded by /prime (Explicit context loading)

**1. `prompts/system.md`** - Policies ONLY
```markdown
<!-- PURPOSE: Non-negotiable guardrails and policies -->
<!-- LOADED BY: /prime command -->
<!-- CONTAINS: What agent can/cannot do, approval rules -->
<!-- DOES NOT CONTAIN: Procedures, technical details -->
```

**Contents**: Policies, rules, boundaries
**NOT**: Step-by-step procedures, MCP usage

---

**2. `prompts/developer.md`** - Technical Contracts ONLY
```markdown
<!-- PURPOSE: Technical reference - CRITICAL details -->
<!-- LOADED BY: /prime command -->
<!-- CONTAINS: MCP contracts, file paths, critical gotchas -->
<!-- DOES NOT CONTAIN: Workflows, policies -->
```

**Contents**: MCP tool contracts, paths, wait times, technical patterns
**NOT**: Policies, workflows

---

**3. `prompts/user.md`** - Conversation Patterns
```markdown
<!-- PURPOSE: User interaction patterns -->
<!-- LOADED BY: /prime command -->
<!-- CONTAINS: Greetings, conversation starters, tone -->
```

**Contents**: How to talk to users, greeting templates
**Size**: Keep small (~50-100 lines)

---

**4. `.claude/skills/SKILL.md`** - Quick Reference
```markdown
# {Agent Name} Skills - Quick Reference

<!-- PURPOSE: Fast lookup for capabilities -->
<!-- LOADED BY: /prime -->
<!-- AUDIENCE: Agent -->
```

**Contents**:
- Core job summary (1-2 sentences)
- Available commands (brief list)
- Critical rules checklist (top 5-7)
- Common patterns (2-3)
- References to detailed docs

**Size**: <100 lines

---

**5. `.claude/skills/WORKFLOW.md`** - Detailed Procedures
```markdown
# {Agent Name} Detailed Workflow

<!-- PURPOSE: Complete procedural workflows -->
<!-- LOADED BY: /prime -->
<!-- CONTAINS: Step-by-step procedures, MCP usage -->
```

**Contents**:
- Complete workflows (step-by-step)
- MCP tool usage examples
- Version management patterns
- Error handling
- Examples and conversation starters

**Size**: 200-600 lines (as needed)

---

### Loaded On-Demand (When invoked)

**Commands** - `.claude/commands/*.md`
- Invoked when user/orchestrator calls the command
- Comprehensive (300-400 lines for major commands)
- Include inline workflows
- Document arguments, error handling

---

### Never Loaded by Agent (Human Docs)

- `README.md` - For humans reading the workspace
- `ARCHITECTURE.md` (system level)
- `VALIDATION.md` (system level)

---

## Bootstrap Pattern (CLAUDE.md)

### Purpose
Minimal file that tells agent its role and to run /prime.

### Template

```markdown
# {Agent Name}

<!-- PURPOSE: Bootstrap instruction - tell agent its role -->
<!-- THIS FILE IS AUTO-LOADED AT STARTUP -->
<!-- AUDIENCE: Agent only -->

You {primary role in one sentence}.

## 🔴 CRITICAL: Initialize First

**Your first action: Run `/prime` to load context.**

Type: `/prime`

This loads all your {workflows/skills/templates/knowledge}.

After /prime completes, you're ready to work.

## Your Role

- {Responsibility 1}
- {Responsibility 2}
- {Responsibility 3}

## Available Commands

See `.claude/settings.json` for complete command list.

Run `/prime` now to get started!
```

### Key Rules

1. **Size**: <30 lines total
2. **No command lists** - Reference settings.json instead
3. **No detailed workflows** - That's for /prime-loaded files
4. **Clear /prime instruction** - Make it obvious
5. **One primary role** - Don't overload this file

### Examples

**Good Example** (goal-builder/CLAUDE.md): 33 lines, pure bootstrap
**Bad Example** (old orchestrator/CLAUDE.md): 121 lines with examples and file lists

---

## Context Hierarchy (prompts/)

### Structure

```
prompts/
├── system.md      # Policies and guardrails
├── developer.md   # Technical contracts
└── user.md        # Conversation patterns
```

---

### prompts/system.md

**Purpose**: Define what agent can/cannot do

**Template**:
```markdown
# {Agent Name} System Guardrails

<!-- PURPOSE: Non-negotiable guardrails and policies -->
<!-- LOADED BY: /prime -->
<!-- CONTAINS: Policies ONLY, NO procedures -->

## Core Responsibility

{What this agent does in 1-2 sentences}

## Absolute Rules

### NEVER Do These
❌ {Thing 1}
❌ {Thing 2}
❌ {Thing 3}

### ALWAYS Do These
✅ {Thing 1}
✅ {Thing 2}
✅ {Thing 3}

## Approval Policy

{When to wait for user approval}

## Write Safety

{Where agent can write files}

## Refusals

{What to say when asked to do forbidden things}
```

**Size**: ~100-150 lines
**Content**: Policies only (no step-by-step procedures)

---

### prompts/developer.md

**Purpose**: Technical reference for critical details

**Template**:
```markdown
# {Agent Name} Developer Essentials

<!-- PURPOSE: Technical reference - CRITICAL details -->
<!-- LOADED BY: /prime -->
<!-- CONTAINS: MCP contracts, paths, gotchas -->

## 🔴 CRITICAL: {Most Important Technical Detail}

{Explanation with examples}

## MCP Tool Contracts

### Tool: mcp__{server}__{function}
**Purpose**: {What it does}
**Parameters**:
- `param1`: {description}
- `param2`: {description}

**Returns**: {What you get back}
**Errors**: {Common error codes}

## File Paths

{Where important files are}

## Wait Times / Gotchas

{Critical technical details that break if ignored}
```

**Size**: ~100-250 lines
**Content**: Technical contracts only (no workflows)

---

### prompts/user.md

**Purpose**: How to interact with users

**Template**:
```markdown
# {Agent Name} User Interaction

<!-- PURPOSE: User interaction patterns -->
<!-- LOADED BY: /prime -->

## Greeting

{How to greet users at session start}

## Tone and Style

- {Guideline 1}
- {Guideline 2}

## Conversation Starters

### When {Scenario}
"{Example phrase}"

### When {Scenario}
"{Example phrase}"
```

**Size**: ~50-100 lines
**Content**: Greetings, tone, common phrases

---

## /prime Implementation

### Purpose
Explicitly load all core context files at session start.

### Location
`.claude/commands/prime.md`

### Template

```markdown
---
description: Initialize {Agent Name} (load all context) - RUN THIS FIRST!
disable-model-invocation: false
---

# Prime {Agent Name}

Load all configuration, workflows, and knowledge into context.

**This command MUST be run at the start of every session.**

---

## Read

Read these files in order:

1. **`prompts/system.md`** - Core behavior and guardrails
2. **`prompts/developer.md`** - Technical details and MCP contracts
3. **`prompts/user.md`** - Conversation patterns
4. **`.claude/skills/SKILL.md`** - Quick reference
5. **`.claude/skills/WORKFLOW.md`** - Complete procedures
{Add agent-specific files if needed}

---

## After Loading

Report to user:

```
✅ You are now fully initialized!

I've loaded:
- Core guardrails and policies
- Technical MCP contracts
- Complete workflows
- {Agent-specific knowledge}

I'm ready to {primary function}.

{Suggest first action}
```

---

## Verification

Confirm all files loaded successfully. If any file is missing or inaccessible, report error clearly.
```

### Key Points

1. **Explicit file list** - No wildcards, no auto-discovery
2. **Order matters** - Load foundational files first
3. **Confirmation message** - Let user know it worked
4. **Error handling** - Report if files missing

---

## Command Development

### Command File Structure

**Location**: `.claude/commands/{command-name}.md`

**Format**:
```markdown
---
description: {Brief description}
argument-hint: {Optional hint like [goal-id] [--flag]}
disable-model-invocation: false
---

# {Command Name}

{What this command does - 1-2 sentences}

---

## Usage

```
/{command-name} {arguments}
/{command-name} {alternative syntax}
```

---

## Arguments

### Required
- `arg1`: {description}

### Optional
- `--flag`: {what it does}

---

## Workflow

### Phase 1: {Step Category}

#### Step 1: {Action}

{Detailed instructions}

**MCP Tool: `mcp__server__function`**
```json
{
  "param": "value"
}
```

#### Step 2: {Action}

{More instructions}

### Phase 2: {Next Category}

{Continue...}

---

## Error Handling

### Error: "{Error message}"
**Solution**: {How to fix}

### Error: "{Error message}"
**Solution**: {How to fix}

---

## Examples

{Common usage examples}
```

### Size Guidelines

- **Simple commands** (show-issues, show-drafts): ~100-150 lines
- **Complex commands** (create-goal, edit-draft): ~300-500 lines

### Key Elements

1. **YAML frontmatter** - description, argument hints
2. **Clear usage** - Show syntax examples
3. **Inline workflows** - Don't just say "create goal", show HOW
4. **MCP tool examples** - Include JSON payloads
5. **Error handling** - Common errors and solutions

---

## SKILL.md Standard Format

### Purpose
Fast lookup reference (<100 lines)

### Template

```markdown
# {Agent Name} Skills - Quick Reference

<!-- PURPOSE: Fast lookup for {agent} capabilities -->
<!-- LOADED BY: /prime command at startup -->
<!-- AUDIENCE: Agent -->

---

## Your Core Job

**You {primary role in 1-2 sentences}.**

```
{Simple ASCII diagram of workflow}
```

---

## Available Commands

**AUTHORITATIVE SOURCE**: `.claude/settings.json`

Quick reference (use these exact command names):

```
/prime
/{command-1} [args]
/{command-2} [args]
/{command-3} [args]
```

---

## Critical Rules Checklist

Before EVERY action:

- [ ] Rule 1
- [ ] Rule 2
- [ ] Rule 3
- [ ] Rule 4
- [ ] Rule 5

---

## Common Patterns

### Pattern 1: {Name}
{Brief description}

### Pattern 2: {Name}
{Brief description}

---

## References

| For... | See... |
|--------|--------|
| Complete workflows | `.claude/skills/WORKFLOW.md` |
| Detailed {thing} | `.claude/commands/{command}.md` |
| {Specific topic} | `prompts/{file}.md` |

---

## Remember

✅ {Key principle 1}
✅ {Key principle 2}
✅ {Key principle 3}
```

### Size: <100 lines

### Key Sections
1. Core job (1-2 sentences)
2. Available commands (list only)
3. Critical rules (top 5-7)
4. Common patterns (2-3)
5. References (where to find details)

---

## WORKFLOW.md Structure

### Purpose
Complete step-by-step procedures

### Template

```markdown
<!-- PURPOSE: Complete procedural workflows -->
<!-- LOADED BY: /prime -->
<!-- CONTAINS: Step-by-step procedures, MCP usage -->

# {Agent Name} Detailed Workflow

## WORKFLOW A: {Primary Workflow}

### Phase 1: {Category}

#### Step 1: {Action}

{Detailed instructions with examples}

**MCP Tool: `mcp__server__function`**
```json
{example payload}
```

**Expected output**: {What you get back}

#### Step 2: {Next Action}

{Continue with complete details}

### Phase 2: {Next Category}

{Continue...}

## WORKFLOW B: {Secondary Workflow}

{Repeat structure}

---

## Best Practices

### DO:
- ✅ {Practice 1}
- ✅ {Practice 2}

### DON'T:
- ❌ {Anti-pattern 1}
- ❌ {Anti-pattern 2}

---

## Troubleshooting

### Issue: "{Problem}"
**Solution**: {How to fix}

---

## Conversation Starters

### {Scenario}
- "{Example phrase}"
- "{Example phrase}"
```

### Size: 200-600 lines (as needed)

### Key Elements
1. **Multiple workflows** - Cover all major use cases
2. **Phase organization** - Group related steps
3. **MCP examples** - Show actual tool usage
4. **Best practices** - DO/DON'T lists
5. **Troubleshooting** - Common issues
6. **Conversation templates** - Help agent talk naturally

---

## MCP Integration

### Configuration (.claude/settings.json)

```json
{
  "customCommands": {
    "prime": {
      "path": ".claude/commands/prime.md",
      "description": "Initialize context"
    },
    "command-name": {
      "path": ".claude/commands/command-name.md",
      "description": "What it does"
    }
  },
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "package-name"],
      "env": {
        "ENV_VAR": "value"
      }
    }
  }
}
```

### Common MCP Servers

**GitHub** (`github/github-mcp-server`):
- `mcp__github__list_issues`
- `mcp__github__get_issue`
- `mcp__github__close_issue`

**Linear** (`@ibraheem4/linear-mcp`):
- `mcp__linear__create_issue`
- `mcp__linear__update_issue`
- `mcp__linear__list_issues`
- `mcp__linear__get_issue`

### Documenting MCP Contracts

In `prompts/developer.md`, document:
- Tool name
- Parameters (with types)
- Return value structure
- Error codes
- Usage examples

---

## Orchestrator Integration

### Make Your Agent Discoverable

**1. Agent metadata in orchestrator's settings.json**

```json
{
  "agents": {
    "your-agent-name": {
      "path": "../your-agent-name",
      "commands": [
        "/prime",
        "/command-1 [args]",
        "/command-2 [args]"
      ],
      "description": "What your agent does"
    }
  }
}
```

**2. Create clean CLAUDE.md, SKILL.md, WORKFLOW.md**

Orchestrator's `/load-agent-context` reads:
- `../your-agent/CLAUDE.md`
- `../your-agent/.claude/skills/SKILL.md`
- `../your-agent/.claude/skills/WORKFLOW.md`

Make these comprehensive and clean!

**3. Document in ARCHITECTURE.md**

Add your agent to the system documentation with:
- Purpose
- Input/Output
- Key commands
- Workflow overview
- File structure

---

## Testing and Validation Checklist

### Pre-Launch Checklist

- [ ] **Bootstrap**: CLAUDE.md <30 lines, tells agent to run /prime
- [ ] **Context Loading**: /prime explicitly lists all files to read
- [ ] **Commands**: All commands use clean names (no prefixes)
- [ ] **Purpose Comments**: All files have <!-- PURPOSE: --> headers
- [ ] **Symlinks**: config.yaml and .env link to ../shared/
- [ ] **MCP Config**: settings.json has all MCP servers configured
- [ ] **File Hierarchy**: system.md (policies), developer.md (contracts), WORKFLOW.md (procedures)
- [ ] **SKILL.md**: <100 lines, quick reference format
- [ ] **No Duplication**: Each concept documented in ONE place
- [ ] **Orchestrator Integration**: Added to orchestrator's settings.json
- [ ] **README.md**: Complete human documentation

---

### Functional Testing

**Test 1: Launch and Prime**
```bash
cd your-agent
./run.sh
/prime
```
**Expected**: All files load, agent confirms ready

---

**Test 2: Basic Commands**
```bash
/command-1
/command-2
```
**Expected**: Commands work, no errors

---

**Test 3: MCP Integration**
```bash
/{command that uses MCP}
```
**Expected**: MCP tools work, data flows correctly

---

**Test 4: Orchestrator Coordination**
```bash
# In orchestrator
/load-agent-context your-agent
# Launch via tmux
# Send commands
```
**Expected**: Orchestrator can coordinate your agent

---

### Quality Checks

- [ ] **Command prefix check**: `grep -r "your-agent:" *.md` → 0 matches
- [ ] **File size check**: CLAUDE.md <50 lines, SKILL.md <100 lines
- [ ] **Duplicate check**: No information appears in multiple files
- [ ] **Reference check**: All cross-references are correct
- [ ] **MCP check**: All MCP tools documented in developer.md

---

## Complete Agent Template

Here's a checklist of all files to create:

```
your-agent-name/
├── CLAUDE.md                          ✅ <30 lines, bootstrap
├── README.md                          ✅ Human documentation
├── .claude/
│   ├── settings.json                  ✅ Commands + MCP
│   ├── commands/
│   │   ├── prime.md                   ✅ Context loader
│   │   ├── {command-1}.md            ✅ Your commands
│   │   ├── {command-2}.md            ✅ ...
│   │   └── {command-N}.md            ✅ ...
│   └── skills/
│       ├── SKILL.md                   ✅ <100 lines quick ref
│       ├── WORKFLOW.md                ✅ Complete procedures
│       └── {TEMPLATES.md}             ⚠️  Optional if needed
├── prompts/
│   ├── system.md                      ✅ Policies
│   ├── developer.md                   ✅ MCP contracts
│   └── user.md                        ✅ Conversation
├── adapters/                          ⚠️  Optional if needed
├── config.yaml → ../shared/           ✅ Symlink
├── .env → ../shared/                  ✅ Symlink
├── .tmp/                              ✅ Working directory
└── run.sh                             ✅ Launch script
```

---

## Quick Start: Building plan-builder

### Step 1: Copy Structure

```bash
cd redesign2
cp -r goal-builder plan-builder
cd plan-builder
```

---

### Step 2: Update CLAUDE.md

```markdown
# Plan Builder

<!-- PURPOSE: Bootstrap instruction - tell agent its role -->
<!-- THIS FILE IS AUTO-LOADED AT STARTUP -->
<!-- AUDIENCE: Agent only -->

You transform Linear goals into detailed implementation plans.

## 🔴 CRITICAL: Initialize First

**Your first action: Run `/prime` to load context.**

Type: `/prime`

This loads all your workflows, skills, and knowledge.

After /prime completes, you're ready to work.

## Your Role

- Transform Linear goals → Linear plan drafts
- Edit and refine existing plan drafts
- Break down goals into concrete tasks
- Design architecture and technical specs
- Version all drafts with automatic diffs

## Available Commands

See `.claude/settings.json` for complete command list.

Run `/prime` now to get started!
```

---

### Step 3: Update prompts/system.md

- Change "goals" references to "plans"
- Update MCP tools (Linear goals → Linear plans)
- Keep same structure (policies, approval workflows)

---

### Step 4: Update prompts/developer.md

- Document Linear MCP for plans
- Update file paths
- Keep same structure

---

### Step 5: Update Commands

Replace:
- `show-issues` → `show-goals`
- `create-goal` → `create-plan`
- `edit-draft` → `edit-draft` (same, but for plans)

---

### Step 6: Update SKILL.md and WORKFLOW.md

- Adapt workflows for goals → plans
- Keep same structure and format

---

### Step 7: Update settings.json

- Change command names
- Update descriptions
- Keep same MCP structure

---

### Step 8: Test

```bash
./run.sh
/prime
/show-goals
```

---

## Common Pitfalls

### ❌ Pitfall 1: Command Prefixes
**Wrong**: `/plan-builder:show-goals`
**Right**: `/show-goals`
**Fix**: Remove all prefixes, session context provides identity

---

### ❌ Pitfall 2: CLAUDE.md Bloat
**Wrong**: 100+ lines with command lists, examples
**Right**: <30 lines, pure bootstrap
**Fix**: Move details to prompts/ and skills/

---

### ❌ Pitfall 3: Information Duplication
**Wrong**: Same policy in system.md, WORKFLOW.md, commands/
**Right**: Policy in system.md ONLY, others reference it
**Fix**: Apply Single Source of Truth principle

---

### ❌ Pitfall 4: Implicit Loading
**Wrong**: "Load all files in prompts/"
**Right**: List exact files: "1. prompts/system.md, 2. prompts/developer.md..."
**Fix**: Make /prime explicit

---

### ❌ Pitfall 5: Missing Purpose Comments
**Wrong**: No <!-- PURPOSE: --> headers
**Right**: All files have purpose, audience, loading info
**Fix**: Add headers to all files

---

## Summary Checklist

When building a new agent, ensure:

✅ **Architecture**
- [ ] Workspace is self-contained
- [ ] Symlinks to shared config/env
- [ ] .tmp/ directory created

✅ **Bootstrap**
- [ ] CLAUDE.md <30 lines
- [ ] /prime command implemented
- [ ] Explicit file loading list

✅ **Context Hierarchy**
- [ ] system.md (policies only)
- [ ] developer.md (contracts only)
- [ ] user.md (greetings)
- [ ] SKILL.md (<100 lines)
- [ ] WORKFLOW.md (complete)

✅ **Commands**
- [ ] Clean names (no prefixes)
- [ ] Comprehensive (300-500 lines for major commands)
- [ ] MCP usage documented

✅ **Quality**
- [ ] Purpose comments on all files
- [ ] No information duplication
- [ ] All references correct
- [ ] grep for prefixes → 0 matches

✅ **Integration**
- [ ] Added to orchestrator settings.json
- [ ] Documented in ARCHITECTURE.md
- [ ] Testable via orchestrator

---

## Need Help?

1. **Reference Agents**: Look at goal-builder as the gold standard
2. **ARCHITECTURE.md**: System-level context
3. **CODEBASE-ANALYSIS.md**: Identifies patterns and issues
4. **NO-PREFIX-RATIONALE.md**: Explains command naming

---

## Conclusion

Follow this guide and your new agent will:
- ✅ Integrate seamlessly with orchestrator
- ✅ Have clean, maintainable structure
- ✅ Load context bulletproof every time
- ✅ Follow all established patterns
- ✅ Be easy to test and debug

**Remember**: The best agents are simple, explicit, and self-contained.
