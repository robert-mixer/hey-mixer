# Goal Builder Agent

<!-- PURPOSE: Comprehensive guide for goal-builder - quick start and deep reference combined -->
<!-- AUDIENCE: All users - from beginners to advanced developers -->

Transform GitHub issues into structured Linear goal tickets through interactive AI collaboration.

---

## Quick Start

Get started in 3 steps:

```bash
# 1. Launch the agent
./run.sh

# 2. Initialize context (REQUIRED!)
/prime

# 3. Start working
/show-issues        # View open GitHub issues
/create-goal 11     # Create goal from issue #11
/edit-draft SYS-10  # Edit existing draft goal
```

---

## What is This?

The Goal Builder is an AI agent powered by Claude that bridges the gap between raw ideas (GitHub issues) and structured planning (Linear goals).

**It helps teams**:
- **Organize** scattered GitHub issues into coherent feature goals
- **Write** comprehensive goal tickets with clear requirements and scope
- **Establish** boundaries to prevent scope creep
- **Maintain** traceability from issues to goals to implementation
- **Collaborate** interactively to write meaningful content (not templates)

---

## Core Capabilities

### Create Goals from Issues
- Transform single or multiple GitHub issues into one cohesive goal
- Automatically load full issue content via GitHub MCP
- Group related issues into logical features
- Close source issues after goal creation

### Edit and Refine Drafts
- Load and modify existing draft goals from Linear
- Iterate collaboratively with version tracking
- Preserve complete edit history with automatic diffs
- Update goals based on changing requirements

### Intelligent Analysis
- Suggest logical issue groupings by feature area
- Identify dependencies and complexity
- Recommend goal boundaries and scope

### Version Management
- Automatic versioning: v1, v2, v3...
- Diff generation between all versions
- Complete audit trail in archive system
- Never lose history

---

## Architecture

### Workspace Isolation

This is a **self-contained workspace** with everything needed to run independently:

```
goal-builder/
├── CLAUDE.md                    # Auto-loaded bootstrap
├── README.md                    # This file
├── .claude/
│   ├── commands/               # Slash commands (7 total)
│   │   ├── prime.md           # Context loader
│   │   ├── show-issues.md     # List GitHub issues
│   │   ├── show-drafts.md     # List Linear drafts
│   │   ├── analyze-issues.md  # Suggest groupings
│   │   ├── create-goal.md     # Create from issues
│   │   ├── edit-draft.md      # Edit existing draft
│   │   └── save-draft.md      # Save to file
│   ├── skills/                # Workflows & templates
│   │   ├── SKILL.md          # Quick reference
│   │   ├── WORKFLOW.md       # Complete procedures
│   │   └── TEMPLATES.md      # Goal templates
│   └── settings.json         # MCP configuration
├── prompts/                   # Context hierarchy
│   ├── system.md             # Guardrails & policies
│   ├── developer.md          # MCP contracts
│   └── user.md               # Conversation patterns
├── adapters/                 # Data transformations
│   ├── transforms/gh_to_linear.md
│   └── handoff/             # Future: researcher agent
├── config.yaml → ../shared/ # Symlink to shared config
├── .env → ../shared/        # Symlink to shared credentials
└── out/                     # Output directory
    └── .tmp/               # Working files & archives
```

### MCP Integration

Uses Model Context Protocol (MCP) servers for external integrations:

**GitHub MCP** (`github/github-mcp-server`):
- `list_issues` - Browse open issues
- `get_issue` - Load full issue content
- `close_issue` - Archive after goal creation

**Linear MCP** (`@ibraheem4/linear-mcp`):
- `create_issue` - Create goal tickets
- `update_issue` - Modify existing drafts
- `list_issues` - Browse draft goals
- `get_issue` - Load complete goal content

All API access goes through MCP (no custom Python scripts).

---

## Workflow Modes

### Normal Mode (Default)

**Interactive collaboration with explicit approval**:
- Draft content WITH user (not templates)
- Show versions and diffs after each change
- Wait for explicit approval before creating/updating in Linear
- Full version tracking (v1, v2, v3...)
- Complete audit trail

**Approval phrases**: "approved", "yes", "create it", "looks good", "go ahead"

**Example**:
```
/create-goal 11

Agent: [Drafts goal content]
Agent: "This looks good. Should I create it in Linear?"
User: "yes"
Agent: [Creates in Linear with status=draft]
```

### Auto-Update Mode

**Skip approval prompts for faster workflow**:
- Triggered by `--auto-update` flag OR user saying "don't ask me again"
- Still maintains full version tracking and audit trail
- Agent proceeds immediately after making changes
- Useful for batch operations or when user trusts the agent

**Example**:
```
/edit-draft SYS-10 --auto-update

Agent: [Makes changes, shows diff]
Agent: "🔥 Auto-update mode. Updating Linear immediately..."
Agent: [Updates without asking]
```

**Mid-workflow switching**: User can say "don't ask again" during any session to switch modes.

---

## Commands Reference

All commands listed in `.claude/settings.json`.

### Essential Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/prime` | Initialize (REQUIRED first step!) | `/prime` |
| `/show-issues` | Display open GitHub issues | `/show-issues` |
| `/show-drafts` | Display draft Linear goals | `/show-drafts` |
| `/create-goal [numbers]` | Create goal from issues | `/create-goal 11` or `/create-goal 11,12,15` |
| `/edit-draft [goal-id]` | Edit existing draft | `/edit-draft SYS-10` |
| `/analyze-issues` | Suggest issue groupings | `/analyze-issues` |
| `/save-draft [filename]` | Save draft to file | `/save-draft my-goal.md` |

### Command Flags

- `--auto-update` - Skip approval prompts (works with `/create-goal` and `/edit-draft`)

---

## Common Workflows

### Create Goal from Single Issue

```
1. /show-issues
2. Select issue number
3. /create-goal 11
4. Collaborate on content interactively
5. Approve when ready ("yes")
6. Goal created in Linear (status=draft)
```

### Create Goal from Multiple Issues

```
/create-goal 11,12,15

Agent loads all three issues and helps create comprehensive goal.
```

### Edit Existing Draft

```
1. /show-drafts
2. /edit-draft SYS-10
3. Request changes ("add OAuth support")
4. Review diff
5. Approve updates ("looks good")
6. Goal updated in Linear
```

### Analyze and Group Issues

```
/analyze-issues

Agent suggests logical groupings by feature area, complexity, dependencies.
Then use /create-goal with suggested issue numbers.
```

---

## Features in Detail

### 1. Interactive Writing

The agent writes **WITH** you, not FOR you:
- No generic templates shipped to Linear
- Real requirements from actual conversation
- Iterative refinement based on your feedback
- Final ticket contains exactly what you wrote together

### 2. Version Management

Every edit creates a new version:
- Files: `.tmp/goal-draft-v1.md`, `v2.md`, `v3.md`...
- Diffs: `.tmp/goal-draft-v1-to-v2.diff`, `v2-to-v3.diff`...
- Complete observability of all changes
- Can request specific version diffs on demand

### 3. Archive System

After successful create/update, all versions archived:
```
.tmp/archives/
  └── SYS-10/
      ├── 20251031-143022/     # Session 1
      │   ├── goal-draft-v1.md
      │   ├── goal-draft-v2.md
      │   └── goal-draft-v1-to-v2.diff
      └── 20251031-151530/     # Session 2
          └── ...
```

Never lose history. Review any past session.

### 4. Quality Standards

Every goal includes:
- **Outcome**: What success looks like (1-2 sentences)
- **Scope**: Specific requirements
- **Non-Goals**: Explicit boundaries
- **Milestones**: 3-5 key checkpoints
- **Metrics**: Quantifiable success measures
- **Risks**: Top blockers + mitigations
- **Examples** (optional): Interaction scenarios for features
- **Related Issues**: Source GitHub issues

**Code Block Formatting**: Use ```text for all examples to prevent YAML auto-detection in Linear.

---

## Configuration

### Required Setup

**1. Environment Variables** (in `../shared/.env`):
```bash
GITHUB_TOKEN=ghp_...      # GitHub personal access token
LINEAR_API_KEY=lin_api_... # Linear API key
```

**2. Configuration** (in `../shared/config.yaml`):
```yaml
github:
  repo: "owner/repo-name"

linear:
  workspace: "workspace-name"
  team_id: "TEAM-UUID"
  tickets:
    goal_label: "goal"
    plan_label: "plan"
```

### How It Works

```
1. Agent launches
2. MCP servers start (configured in settings.json)
3. MCP servers read .env for tokens
4. Agent reads config.yaml for repo/workspace info
5. Agent uses MCP tools to interact with GitHub/Linear
```

---

## Status Flow

Goals progress through these statuses:

```
draft → todo → doing → done
```

- **draft**: Created by goal-builder (needs review)
- **todo**: User approves, ready for plan-builder
- **doing**: Plan-builder creates implementation plan
- **done**: Module-builder completes implementation

**Key Rule**: Only **users** manually transition draft→todo. Everything else is automatic.

---

## Best Practices

### DO:
- ✅ Start every session with `/prime`
- ✅ Use commands instead of manual operations
- ✅ Collaborate interactively (write WITH agent)
- ✅ Review diffs after each change
- ✅ Include Examples section for interactive features
- ✅ Use ```text for interaction examples (prevents YAML issues)
- ✅ Keep goals focused and achievable (1-2 sprints)

### DON'T:
- ❌ Skip `/prime` at startup
- ❌ Accept template content without customization
- ❌ Create goals with status="todo" directly (always "draft")
- ❌ Combine unrelated issues
- ❌ Make goals too large or vague

---

## Troubleshooting

### "MCP authentication failed"
**Cause**: Invalid tokens in `.env`
**Solution**: Check `GITHUB_TOKEN` and `LINEAR_API_KEY` in `../shared/.env`

### "Goal not found"
**Cause**: Incorrect goal ID
**Solution**: Verify goal ID (e.g., SYS-123) exists in Linear using `/show-drafts`

### "Context not loaded"
**Cause**: `/prime` not run
**Solution**: Run `/prime` first - it's REQUIRED at session start

### "Can only edit draft goals"
**Cause**: Trying to edit goal with status != "draft"
**Solution**: Only draft goals editable. For todo/doing/done, edit in Linear directly.

---

## Integration with Mixer System

### Workflow Pipeline

```
GitHub Issues
    ↓ (goal-builder)
Linear Goals (draft)
    ↓ (user: draft → todo)
Linear Goals (todo)
    ↓ (plan-builder)
Linear Plans (draft)
    ↓ (user: draft → todo)
Linear Plans (todo)
    ↓ (module-builder)
Feature Code
```

### Handoff to Plan Builder

When you change goal status from "draft" to "todo", the Plan Builder can:
1. Read the goal requirements
2. Create detailed implementation plan
3. Break down into concrete tasks
4. Define module structure

---

## Related Agents

- **Orchestrator**: Coordinates all builder agents (optional - can use goal-builder standalone)
- **Plan Builder**: Creates implementation plans from goals
- **Module Builder**: Implements plans to build feature modules

---

## Documentation

### In This Workspace

- **WORKFLOW.md**: Complete step-by-step procedures
- **TEMPLATES.md**: Goal ticket templates and examples
- **prompts/developer.md**: MCP integration contracts
- **adapters/transforms/gh_to_linear.md**: Field mapping rules

### System-Wide

- **../ARCHITECTURE.md**: Complete system overview
- **../AGENT-DEVELOPMENT-GUIDE.md**: How to build new agents
- **../shared/README.md**: Shared configuration docs

---

## Next Steps

After creating a goal:

1. **Review in Linear**: Check the draft ticket
2. **Adjust if needed**: Use `/edit-draft SYS-10`
3. **Change status**: draft → todo (manually in Linear)
4. **Hand off**: Plan-builder creates implementation plan

---

## Support

**Common Questions**:
- Check [Troubleshooting](#troubleshooting) section above
- Review WORKFLOW.md for detailed procedures
- Ensure `/prime` was run at startup
- Verify `.env` and `config.yaml` are correct

**For Issues**:
- Check MCP server status
- Verify token permissions
- Review agent logs

---

**Ready to start?** Run `./run.sh`, then type `/prime` to begin! 🚀
