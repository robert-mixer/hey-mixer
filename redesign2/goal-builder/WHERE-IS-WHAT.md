# Information Architecture - Goal Builder

**Purpose**: Crystal-clear map of where every piece of information lives
**Rule**: Every topic has EXACTLY ONE authoritative source
**When to read**: FIRST thing when working with goal-builder

---

## The Single Source of Truth Principle

**Every piece of information exists in ONE place.**

All other files either:
1. Don't mention it at all, OR
2. Briefly reference the authoritative source

**Never duplicate. Always reference.**

---

## What Lives Where

### 1. Policies (Non-Negotiable Rules)

**Authoritative Source**: `prompts/system.md`

**What's There**:
- ✅ Approval policy (must wait for "approved", "yes", "looks good", etc.)
- ✅ Auto-update mode rules (when --auto-update flag is used)
- ✅ Version management system (v1, v2, v3, diffs, .tmp/goal-version.txt)
- ✅ Archive system (after successful Linear update)
- ✅ File writing safety (only write to ./out/)
- ✅ Output format standards (Markdown, tables, diffs)
- ✅ Natural language understanding (map "show issues" → `/show-issues`)

**Who References It**:
- All command files (create-goal.md, edit-draft.md, etc.) reference these policies
- WORKFLOW.md references for detailed procedures
- No duplication - if you want policy details, look ONLY in system.md

**When Loaded**: By `/prime` command at startup

---

### 2. MCP Contracts (External Integrations)

**Authoritative Source**: `prompts/developer.md`

**What's There**:
- ✅ GitHub MCP tools (list_issues, get_issue, close_issue) with full syntax
- ✅ Linear MCP tools (create_issue, update_issue, list_issues, get_issue) with full syntax
- ✅ Configuration structure (config.yaml schema)
- ✅ Environment variables (.env format)
- ✅ MCP server specifications

**Who References It**:
- All command files reference MCP tools (don't duplicate syntax)
- Example: "Use mcp__github__list_issues (see developer.md for syntax)"

**When Loaded**: By `/prime` command at startup

---

### 3. Commands (What Agent Can Do)

**Authoritative Source**: `.claude/settings.json`

**What's There**:
- ✅ Complete list of all slash commands
- ✅ Command paths
- ✅ Command descriptions
- ✅ This is the ONLY place where commands are defined

**Who References It**:
- CLAUDE.md: "See settings.json for complete command list"
- README.md: User-friendly table (allowed as user documentation)
- SKILL.md: "See settings.json for commands"
- NO other file should list commands

**When Loaded**: By Claude Code at startup (reads settings.json automatically)

---

### 4. Procedures (Step-by-Step How-To)

**Authoritative Source**: `.claude/skills/WORKFLOW.md`

**What's There**:
- ✅ Complete workflows for each command
- ✅ Decision trees (when to use which command)
- ✅ Step-by-step procedures
- ✅ Integration between commands

**Who References It**:
- Command files reference specific workflows
- Example: "Follow create-goal workflow from WORKFLOW.md"
- Each command file focuses on its specific implementation

**When Loaded**: By `/prime` command at startup

---

### 5. Templates (Content Structure)

**Authoritative Source**: `.claude/skills/TEMPLATES.md`

**What's There**:
- ✅ Goal ticket template structure
- ✅ Example goals
- ✅ Field definitions (Outcome, Scope, Non-Goals, etc.)
- ✅ Formatting rules (use ```text for examples)

**Who References It**:
- create-goal.md: "Use goal template from TEMPLATES.md"
- edit-draft.md: "Follow template structure from TEMPLATES.md"
- No duplication of template structure

**When Loaded**: By `/prime` command at startup

---

### 6. Quick Reference

**Authoritative Source**: `.claude/skills/SKILL.md`

**What's There**:
- ✅ Agent role summary (one sentence)
- ✅ Critical rules checklist (top 5-7 rules)
- ✅ Common patterns (quick lookup)
- ✅ References to detailed documentation

**Format**: <100 lines, designed for quick lookup

**When Loaded**: By `/prime` command at startup

---

### 7. Conversation Patterns

**Authoritative Source**: `prompts/user.md`

**What's There**:
- ✅ Greeting templates
- ✅ How to interact with users
- ✅ Tone and style guidelines
- ✅ Common user interaction patterns

**When Loaded**: By `/prime` command at startup

---

### 8. Data Transformations

**Authoritative Source**: `adapters/transforms/gh_to_linear.md`

**What's There**:
- ✅ How to map GitHub issue fields to Linear goal fields
- ✅ Field transformations
- ✅ Data structure mappings

**Who References It**:
- create-goal.md: "Transform per gh_to_linear.md mapping"
- No duplication of transformation logic

**When Loaded**: On-demand when creating goals from GitHub issues

---

### 9. User Documentation

**Authoritative Source**: `README.md`

**What's There**:
- ✅ Quick start guide
- ✅ What is goal-builder (for humans)
- ✅ Command reference table (user-friendly)
- ✅ Common workflows (user perspective)
- ✅ Troubleshooting
- ✅ Configuration setup
- ✅ Integration info

**Audience**: Humans (developers, users)

**When Loaded**: NEVER (not loaded by agent - this is for humans)

**Note**: README.md is allowed to have user-friendly explanations of policies, commands, etc. This is NOT duplication because it's for a different audience.

---

### 10. Bootstrap

**Authoritative Source**: `CLAUDE.md`

**What's There**:
- ✅ Agent role (one sentence)
- ✅ "Run /prime first" instruction
- ✅ Essential rules only (<40 lines total)
- ✅ Reference to settings.json for commands

**What's NOT There**:
- ❌ Command lists (see settings.json)
- ❌ Detailed workflows (see WORKFLOW.md)
- ❌ Policies (see system.md)
- ❌ Procedures (see WORKFLOW.md)

**When Loaded**: Automatically by Claude Code at startup

---

### 11. Individual Commands

**Authoritative Source**: `.claude/commands/[command-name].md`

**What's There** (for each command):
- ✅ Command-specific workflow
- ✅ Arguments and flags
- ✅ **References** to policies (system.md), procedures (WORKFLOW.md), MCP tools (developer.md)
- ✅ Command-specific edge cases

**What's NOT There**:
- ❌ Full policy explanations (reference system.md instead)
- ❌ Full MCP tool syntax (reference developer.md instead)
- ❌ Duplicate workflow details (reference WORKFLOW.md instead)

**When Loaded**: On-demand when command is invoked

---

## Information Flow

```
Session Start
    ↓
CLAUDE.md (auto-loaded) - Bootstrap
    ↓
    Tells agent: "Run /prime"
    ↓
User types: /prime
    ↓
prompts/system.md ← POLICIES loaded
prompts/developer.md ← MCP CONTRACTS loaded
prompts/user.md ← CONVERSATION PATTERNS loaded
.claude/skills/SKILL.md ← QUICK REFERENCE loaded
.claude/skills/WORKFLOW.md ← PROCEDURES loaded
.claude/skills/TEMPLATES.md ← TEMPLATES loaded
adapters/transforms/gh_to_linear.md ← TRANSFORMATIONS loaded
    ↓
Agent is now fully initialized with ALL context
    ↓
User types: /create-goal 11
    ↓
.claude/commands/create-goal.md ← COMMAND IMPLEMENTATION loaded
    (References system.md, developer.md, WORKFLOW.md, TEMPLATES.md)
    (NO duplication - just references)
    ↓
Agent executes command using loaded context
```

---

## How to Use This Map

### When Creating New Commands

1. Read this file FIRST
2. Identify what information you need (policy? procedure? MCP tool? template?)
3. **Reference** the authoritative source (don't duplicate it)
4. Keep command file focused on command-specific logic only

### When Modifying Policies

1. Read this file to find where policy lives (always prompts/system.md)
2. Update ONLY system.md
3. All command files automatically get the update (they reference it)
4. Never update in multiple places

### When Adding New Information

1. Ask: "Where does this information belong?"
2. Check this map for the appropriate authoritative source
3. Add to ONLY that file
4. Update this map if you create a new information category

---

## File Loading Matrix

| File | When Loaded | Audience | Purpose |
|------|-------------|----------|---------|
| CLAUDE.md | Startup (auto) | Agent | Bootstrap |
| README.md | Never | Humans | User docs |
| WHERE-IS-WHAT.md | Never | Developers | Architecture map |
| prompts/system.md | /prime | Agent | Policies |
| prompts/developer.md | /prime | Agent | MCP contracts |
| prompts/user.md | /prime | Agent | Conversation patterns |
| .claude/settings.json | Startup (auto) | Claude Code | Commands definition |
| .claude/skills/SKILL.md | /prime | Agent | Quick reference |
| .claude/skills/WORKFLOW.md | /prime | Agent | Procedures |
| .claude/skills/TEMPLATES.md | /prime | Agent | Content templates |
| .claude/commands/*.md | On-demand | Agent | Command implementation |
| adapters/transforms/*.md | On-demand | Agent | Data transformations |

---

## Rules for Maintaining This Architecture

### Rule 1: ONE Source of Truth
Every piece of information exists in EXACTLY ONE authoritative file.

### Rule 2: Reference, Don't Duplicate
If you need information from another file, REFERENCE it (don't copy it).

**Good**: "Follow approval policy from system.md"
**Bad**: Copying approval phrases into command file

### Rule 3: Update This Map
If you add a new information category, update WHERE-IS-WHAT.md.

### Rule 4: User Docs Exception
README.md is allowed to explain things for users (different audience = not duplication).

### Rule 5: Check Before Writing
Before adding information to a file, check this map: "Does this belong here?"

---

## Quick Lookup

**Need to find...**
- Approval phrases? → prompts/system.md
- Version management? → prompts/system.md
- MCP tool syntax? → prompts/developer.md
- Command list? → .claude/settings.json
- Workflow steps? → .claude/skills/WORKFLOW.md
- Goal template? → .claude/skills/TEMPLATES.md
- User guide? → README.md

---

**This map ensures**: "from some high level files it is extremely clear where what information lives in what file" ✅

**Last Updated**: 2025-10-31
