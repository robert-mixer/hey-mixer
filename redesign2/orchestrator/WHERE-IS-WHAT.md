# Information Architecture - Orchestrator

**Purpose**: Crystal-clear map of where every piece of information lives
**Rule**: Every topic has EXACTLY ONE authoritative source
**When to read**: FIRST thing when working with orchestrator

---

## The Single Source of Truth Principle

**Every piece of information exists in ONE place.**

All other files either:
1. Don't mention it at all, OR
2. Briefly reference the authoritative source

**Never duplicate. Always reference.**

---

## What Lives Where

### 1. Agent Interaction Critical Rules

**Authoritative Source**: `.claude/AGENT-INTERACTION-CRITICAL-RULES.md`

**What's There**:
- ✅ **Natural language to slash command translation** (THE definitive guide)
  - All translation patterns
  - All examples ("show issues" → `/show-issues`)
  - Edge cases (user says "A", user says informal text)
  - Mid-workflow switching detection
- ✅ Auto-update mode detection (complete patterns)
- ✅ Absolute rule: You are NOT the agent (forbidden actions, allowed actions)
- ✅ Role explanation (relay, not builder)
- ✅ Approval rules (never approve on behalf of user in normal mode)
- ✅ Mental models (correct vs incorrect thinking)
- ✅ Real incident examples (violations and corrections)

**This is THE BIBLE for orchestrator behavior.**

**Who References It**:
- prompts/system.md: "See AGENT-INTERACTION-CRITICAL-RULES.md for translation rules"
- run-agent.md: "See AGENT-INTERACTION-CRITICAL-RULES.md for complete translation guide"
- SKILL.md: "Always translate (see AGENT-INTERACTION-CRITICAL-RULES.md)"
- WORKFLOW.md: References for specific patterns
- prime.md: Loads this file at startup

**When Loaded**: By `/prime` command at startup

---

### 2. Policies (Non-Negotiable Rules)

**Authoritative Source**: `prompts/system.md`

**What's There**:
- ✅ Core responsibility (coordinate, don't execute)
- ✅ Command translation policy (one-sentence: "ALWAYS translate user intent to slash commands")
- ✅ Never send generic text when commands exist
- ✅ Never make decisions without user confirmation
- ✅ **Reference to AGENT-INTERACTION-CRITICAL-RULES.md for details**

**What's NOT There**:
- ❌ Detailed translation examples (those are in AGENT-INTERACTION-CRITICAL-RULES.md)
- ❌ Duplicate rules (reference AGENT-INTERACTION-CRITICAL-RULES.md instead)

**When Loaded**: By `/prime` command at startup

---

### 3. Technical Implementation Details

**Authoritative Source**: `prompts/developer.md`

**What's There**:
- ✅ TMux two-step command sending (CRITICAL technical pattern)
- ✅ Agent workspace paths
- ✅ Session management patterns
- ✅ Agent command reference (lists builder commands for context)
- ✅ Auto-update pattern detection technical details
- ✅ Wait times and error detection

**Who References It**:
- run-agent.md: "See developer.md for tmux command sending"
- WORKFLOW.md: References technical patterns
- SKILL.md: References for technical details

**When Loaded**: By `/prime` command at startup

---

### 4. Commands (What Orchestrator Can Do)

**Authoritative Source**: `.claude/settings.json`

**What's There**:
- ✅ Orchestrator's own commands (prime, load-agent-context)
- ✅ **Builder agents metadata** (goal-builder, plan-builder, module-builder)
- ✅ Each builder's capabilities, commands, input/output
- ✅ This is the ONLY place where commands and agents are defined

**Who References It**:
- CLAUDE.md: "See settings.json for complete command list"
- README.md: User-friendly reference (allowed as user documentation)
- SKILL.md: "See settings.json"
- NO other file should duplicate this information

**When Loaded**: By Claude Code at startup (reads settings.json automatically)

---

### 5. Coordination Workflows

**Authoritative Source**: `.claude/skills/WORKFLOW.md`

**What's There**:
- ✅ Complete workflow for coordinating goal-builder
- ✅ Complete workflow for coordinating plan-builder
- ✅ Complete workflow for coordinating module-builder
- ✅ Multi-agent coordination procedures
- ✅ Error handling procedures
- ✅ Session management
- ✅ **References** to AGENT-INTERACTION-CRITICAL-RULES.md (doesn't duplicate)

**When Loaded**: By `/prime` command at startup

---

### 6. Quick Reference

**Authoritative Source**: `.claude/skills/SKILL.md`

**What's There**:
- ✅ Orchestrator role summary (coordinate, don't build)
- ✅ The three builder agents overview
- ✅ Agent commands orchestrator MUST use
- ✅ Critical rules checklist
- ✅ **Brief reference** to AGENT-INTERACTION-CRITICAL-RULES.md (no duplication)

**Format**: <100 lines, designed for quick lookup

**When Loaded**: By `/prime` command at startup

---

### 7. Conversation Patterns

**Authoritative Source**: `prompts/user.md`

**What's There**:
- ✅ Greeting templates
- ✅ Common user intents (what users typically ask for)
- ✅ Mid-workflow interactions
- ✅ Error handling messages
- ✅ Completion messages

**When Loaded**: By `/prime` command at startup

---

### 8. User Documentation

**Authoritative Source**: `README.md`

**What's There**:
- ✅ What is orchestrator (for humans)
- ✅ How it works (coordination model)
- ✅ When to use orchestrator vs direct builder access
- ✅ Common workflows from user perspective
- ✅ Troubleshooting

**Audience**: Humans (developers, users)

**When Loaded**: NEVER (not loaded by agent - this is for humans)

**Note**: README.md is allowed to have user-friendly explanations. This is NOT duplication because it's for a different audience.

---

### 9. Bootstrap

**Authoritative Source**: `CLAUDE.md`

**What's There**:
- ✅ Orchestrator role (one sentence: "coordinate interactions")
- ✅ "Run /prime first" instruction
- ✅ Essential rules only (<45 lines total)
- ✅ **One bullet point** about translation (not detailed examples)
- ✅ Reference to settings.json for commands

**What's NOT There**:
- ❌ Detailed translation patterns (see AGENT-INTERACTION-CRITICAL-RULES.md)
- ❌ Complete workflow procedures (see WORKFLOW.md)
- ❌ Technical implementation (see developer.md)
- ❌ Command lists (see settings.json)

**When Loaded**: Automatically by Claude Code at startup

---

### 10. Individual Commands

**Authoritative Source**: `.claude/commands/[command-name].md`

#### `/prime` (Context Loader)
**What's There**:
- ✅ List of files to load (explicit)
- ✅ What each file contains (brief description)
- ✅ Success confirmation message
- ✅ **No duplication** of the actual content (just loads it)

#### `/load-agent-context` (Agent Context Loader)
**What's There**:
- ✅ How to load specific builder agent's documentation
- ✅ Which files to read for each builder
- ✅ What to extract and memorize
- ✅ **References** builder documentation (doesn't duplicate it)

#### `/run-agent` (Agent Coordination Guide)
**What's There**:
- ✅ Complete tmux interaction guide
- ✅ Phase-by-phase coordination workflows
- ✅ Agent-specific procedures
- ✅ Troubleshooting
- ✅ **References AGENT-INTERACTION-CRITICAL-RULES.md** (doesn't duplicate translation rules)

**When Loaded**: On-demand when command is invoked

---

## Information Flow

```
Session Start
    ↓
CLAUDE.md (auto-loaded) - Bootstrap
    ↓
    Tells orchestrator: "Run /prime"
    ↓
User types: /prime
    ↓
prompts/system.md ← POLICIES loaded
prompts/developer.md ← TECHNICAL DETAILS loaded
prompts/user.md ← CONVERSATION PATTERNS loaded
.claude/skills/SKILL.md ← QUICK REFERENCE loaded
.claude/skills/WORKFLOW.md ← COORDINATION WORKFLOWS loaded
.claude/AGENT-INTERACTION-CRITICAL-RULES.md ← CRITICAL RULES loaded (including ALL translation patterns)
.claude/commands/run-agent.md ← RUN AGENT GUIDE loaded
    ↓
Orchestrator is now fully initialized
    ↓
User says: "Create a goal from issue 11"
    ↓
Orchestrator thinks:
  - Check AGENT-INTERACTION-CRITICAL-RULES.md: This means goal-builder
  - Check settings.json: goal-builder has /create-goal command
  - Translate: "create goal from 11" → `/create-goal 11`
    ↓
Orchestrator launches goal-builder via tmux
    ↓
Orchestrator sends: `/create-goal 11` to goal-builder session
    (Uses translation rules from AGENT-INTERACTION-CRITICAL-RULES.md)
    (Uses tmux patterns from developer.md)
    ↓
Orchestrator relays messages between user and goal-builder
```

---

## How to Use This Map

### When Modifying Translation Rules

1. Read this file to find where translation lives (always AGENT-INTERACTION-CRITICAL-RULES.md)
2. Update ONLY AGENT-INTERACTION-CRITICAL-RULES.md
3. All other files automatically get the update (they reference it)
4. **Never update translation patterns in multiple files**

### When Adding New Builder Agents

1. Update settings.json with new agent metadata
2. Create builder's workspace following goal-builder structure
3. Create builder's WHERE-IS-WHAT.md
4. No changes needed to orchestrator documentation (settings.json is the source)

### When Creating New Commands

1. Read this file FIRST
2. Identify what information you need
3. **Reference** the authoritative source (don't duplicate it)
4. Keep command file focused on command-specific logic only

---

## File Loading Matrix

| File | When Loaded | Audience | Purpose |
|------|-------------|----------|---------|
| CLAUDE.md | Startup (auto) | Agent | Bootstrap |
| README.md | Never | Humans | User docs |
| WHERE-IS-WHAT.md | Never | Developers | Architecture map |
| prompts/system.md | /prime | Agent | Policies |
| prompts/developer.md | /prime | Agent | Technical details |
| prompts/user.md | /prime | Agent | Conversation patterns |
| .claude/settings.json | Startup (auto) | Claude Code | Commands & agents definition |
| .claude/skills/SKILL.md | /prime | Agent | Quick reference |
| .claude/skills/WORKFLOW.md | /prime | Agent | Coordination workflows |
| .claude/AGENT-INTERACTION-CRITICAL-RULES.md | /prime | Agent | **THE BIBLE** (translation, auto-update, rules) |
| .claude/commands/*.md | On-demand | Agent | Command implementation |

---

## Rules for Maintaining This Architecture

### Rule 1: ONE Source of Truth
Every piece of information exists in EXACTLY ONE authoritative file.

**Translation rules?** → AGENT-INTERACTION-CRITICAL-RULES.md (ONLY)
**Tmux patterns?** → developer.md (ONLY)
**Agent metadata?** → settings.json (ONLY)

### Rule 2: Reference, Don't Duplicate
If you need translation rules, REFERENCE AGENT-INTERACTION-CRITICAL-RULES.md (don't copy examples).

**Good**: "See AGENT-INTERACTION-CRITICAL-RULES.md for translation patterns"
**Bad**: Copying translation examples into run-agent.md, SKILL.md, system.md, etc.

### Rule 3: Update This Map
If you add a new information category, update WHERE-IS-WHAT.md.

### Rule 4: User Docs Exception
README.md is allowed to explain things for users (different audience = not duplication).

### Rule 5: AGENT-INTERACTION-CRITICAL-RULES.md is THE Bible
For orchestrator, this file is the MOST IMPORTANT authoritative source.
- Translation patterns
- Auto-update detection
- Critical rules
- Mental models
- Real examples

**Everything else references it.**

---

## Quick Lookup

**Need to find...**
- Translation patterns? → .claude/AGENT-INTERACTION-CRITICAL-RULES.md
- Auto-update detection? → .claude/AGENT-INTERACTION-CRITICAL-RULES.md
- Forbidden actions? → .claude/AGENT-INTERACTION-CRITICAL-RULES.md
- Tmux command sending? → prompts/developer.md
- Builder commands? → .claude/settings.json
- Coordination workflows? → .claude/skills/WORKFLOW.md
- User guide? → README.md

---

**This map ensures**: "from some high level files it is extremely clear where what information lives in what file" ✅

**Last Updated**: 2025-10-31
