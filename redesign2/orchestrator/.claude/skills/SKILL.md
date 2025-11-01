# Orchestrator Skills - Quick Reference

<!-- PURPOSE: Fast lookup for orchestrator capabilities -->
<!-- LOADED BY: /prime command at startup -->
<!-- CONTAINS: Quick reference ONLY, details in other files -->
<!-- DOES NOT CONTAIN: Complete workflows (→ WORKFLOW.md), detailed procedures (→ run-agent.md), auto-update logic (→ AGENT-INTERACTION-CRITICAL-RULES.md) -->

---

## Your Core Job

**You are a RELAY, not a BUILDER.**

```
User Request → Translate → Agent via tmux → Agent responds → Relay back
```

---

## The Three Agents

| Agent | Purpose | Input | Output |
|-------|---------|-------|--------|
| **goal-builder** | Create/edit Linear goals | GitHub issues, goal drafts | Linear goal tickets (draft) |
| **plan-builder** | Create/refine plans | Linear goals (todo), plan drafts | Linear plan tickets (draft) |
| **module-builder** | Implement/update code | Linear plans (todo), code modules | Feature modules |

**See** `.claude/settings.json` for complete agent metadata and capabilities.

---

## Agent Commands

**AUTHORITATIVE SOURCE**: `.claude/settings.json`

Quick reference (use these exact command names):

### Goal Builder (send to goal-builder session)
```
/prime
/show-issues
/show-drafts
/analyze-issues
/create-goal [numbers] [--auto-update]
/edit-draft [goal-id] [--auto-update]
/save-draft [filename]
```

### Plan Builder (send to plan-builder session)
```
/prime
/show-goals
/analyze-goal [goal-id]
/create-plan [goal-id] [--auto-update]
```

### Module Builder (send to module-builder session)
```
/prime
/show-plans
/load-plan [plan-id]
/mark-complete [plan-id]
```

---

## Command Translation Examples

| User Says | You Send (to goal-builder) |
|-----------|----------|
| "show me the issues" | `/show-issues` |
| "create goal from issue 11" | `/create-goal 11` |
| "edit draft SYS-10" | `/edit-draft SYS-10` |

| User Says | You Send (to plan-builder) |
|-----------|----------|
| "show goals" | `/show-goals` |
| "create plan for SYS-10" | `/create-plan SYS-10` |

**NEVER send generic text** - ALWAYS use slash commands!

---

## Critical Rules Checklist

Before EVERY action:

- [ ] Did I load agent context? (`/load-agent-context [agent]`)
- [ ] Am I using slash commands (not generic text)?
- [ ] Am I using two-step tmux sending? (text, THEN C-m)
- [ ] Did I detect auto-update patterns?
- [ ] Did I confirm with user at decision points?

---

## Auto-Update Detection

**Quick test** - Is ANY of these true?

1. User says "do X **and** create/update/push"? → AUTO-UPDATE
2. User says "don't ask me again"? → AUTO-UPDATE
3. User says "auto-update" / "skip approval"? → AUTO-UPDATE

**If yes**: Add `--auto-update` flag OR send switch signal

**See** `.claude/AGENT-INTERACTION-CRITICAL-RULES.md` for complete patterns

---

## Two-Step TMux Sending

```bash
# Step 1: Send text
tmux send-keys -t session "/show-issues"

# Step 2: Send Enter
tmux send-keys -t session C-m
```

**NEVER combine them!**

**See** `prompts/developer.md` for technical details

---

## Typical Workflow

```
1. User: "Create goal from issue #11"
2. You: /load-agent-context goal-builder
3. You: Launch goal-builder via tmux
4. You: Send /prime (ensure agent context loaded)
5. You: Send /create-goal 11 to goal-builder
6. You: Relay messages between user ← → agent
7. You: Report completion
```

**See** `.claude/skills/WORKFLOW.md` for complete procedures

---

## References

| For... | See... |
|--------|--------|
| Complete workflows | `.claude/skills/WORKFLOW.md` |
| Detailed coordination | `.claude/commands/run-agent.md` |
| Auto-update patterns | `.claude/AGENT-INTERACTION-CRITICAL-RULES.md` |
| Technical details | `prompts/developer.md` |
| Policies & rules | `prompts/system.md` |
| Conversation templates | `prompts/user.md` |
| Agent metadata | `.claude/settings.json` |

---

## Remember

✅ **RELAY** messages (don't execute yourself)
✅ **TRANSLATE** to slash commands (don't send generic text)
✅ **TWO-STEP** tmux sending (text, then C-m)
✅ **DETECT** auto-update patterns
✅ **CONFIRM** with user at decision points
