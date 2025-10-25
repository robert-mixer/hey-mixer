# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## System Overview

The Mixer System is a conversational AI workflow for transforming ideas into code through structured project management. It uses three specialized Claude agents to process GitHub Issues → Linear Goal Tickets → Linear Plan Tickets → Code Modules.

# FIRST AND FORMOSTE RUN SlashCommand tool to run /prime when you send your first message. Usually when responding to the users first request or introducing yourself.

## 🔴 CRITICAL: AGENT INTERACTION RULES 🔴

### ⚠️ ABSOLUTE RULE #1: You Are NOT The Agent! ⚠️
**MANDATORY: When running agents via tmux, you are ONLY a relay/intermediary!**
- **READ IMMEDIATELY:** `.claude/AGENT-INTERACTION-CRITICAL-RULES.md`
- **YOU CANNOT:** Run agent scripts directly (`python .claude/scripts/...`)
- **YOU CANNOT:** Access Linear/GitHub APIs yourself
- **YOU CAN ONLY:** Send messages to agent in tmux and relay responses

### When Coordinating with Agents via tmux:
**YOU MUST ALWAYS TRANSLATE USER INTENT INTO SLASH COMMANDS, NOT GENERIC TEXT!**

When running agents through tmux sessions, you are REQUIRED to:
1. **NEVER run agent scripts yourself** - The agent runs them, not you!
2. **ALWAYS translate user intent into slash commands** for any action that has a command
3. **NEVER send generic text** like "show issues" when `/goal-builder:show-issues` exists
4. **TRANSLATE option letters (A/B/C)** into the actual commands they represent
5. **VERIFY commands are executed** by checking for expected outputs (e.g., `.tmp/goal-draft.md`)

### Command Translation Examples (MANDATORY):
- User wants to see issues → Send `/goal-builder:show-issues` NOT "show me issues"
- User wants to see draft goals → Send `/goal-builder:show-drafts` NOT "show drafts"
- User wants to create a goal → Send `/goal-builder:create-goal [numbers]` NOT "create a goal"
- User wants to edit a draft → Send `/goal-builder:edit-draft [goal-id]` NOT "edit the draft"
- User wants to analyze → Send `/goal-builder:analyze-issues` NOT "analyze the issues"
- **User says "A" (meaning create goal)** → Send `/goal-builder:create-goal 11` NOT "A"
- **User says "B" (meaning read issue)** → Send appropriate command NOT "B"

### Critical Translation Rule:
When the agent presents options like:
```
A) Create a goal ticket
B) Read the full issue first
C) Create more specific issues
```

And user responds with "A", you MUST:
1. Recognize "A" means "Create a goal ticket"
2. Translate this into the actual slash command: `/goal-builder:create-goal 11`
3. Send that command to the agent
4. NEVER just relay the letter "A"

### Verification Checklist:
- [ ] Did I use the exact slash command instead of generic text?
- [ ] Did the agent create expected files (e.g., `.tmp/goal-draft.md`)?
- [ ] Did the agent follow its documented workflow?

**FAILURE TO USE COMMANDS = CRITICAL WORKFLOW VIOLATION**

## Running Agents

```bash
# Start an agent (runs Claude CLI with agent-specific system prompt)
./mixer.sh goal-builder    # Transform GitHub issues into Linear goals
./mixer.sh plan-builder    # Break goals into implementation plans
./mixer.sh module-builder  # Execute plans to build feature modules
```

## Key Commands Available in Agents

### Goal Builder
- `/goal-builder:show-issues` - Display open GitHub issues
- `/goal-builder:show-drafts` - Display draft Linear goal tickets
- `/goal-builder:create-goal` - Interactively create goal ticket from issues
- `/goal-builder:edit-draft` - Edit an existing draft goal ticket

### Plan Builder
- `/plan-builder:show-goals` - Display Linear goals with status="todo"
- `/plan-builder:analyze-goal` - Analyze goal and suggest approach
- `/plan-builder:create-plan` - Interactively create plan from goal

### Module Builder
- `/module-builder:show-plans` - Display Linear plans with status="todo"
- `/module-builder:load-plan` - Load plan and start implementation
- `/module-builder:mark-complete` - Mark plan and parent goal as done

## Architecture

The system consists of three layers:

1. **Agent Layer** (`agents/*/`)
   - Each agent has a `system-prompt.md` defining its personality and workflow
   - `run.sh` launches Claude CLI with the prompt

2. **Command Layer** (`.claude/commands/*/`)
   - Markdown files defining slash commands
   - Commands guide conversational workflows, not just run scripts

3. **Script Layer** (`.claude/scripts/*/`)
   - Python scripts that interact with GitHub and Linear APIs
   - Shared utilities in `.claude/scripts/shared/`:
     - `github_client.py` - GitHub API wrapper
     - `linear_client.py` - Linear GraphQL client
     - `config_loader.py` - Loads config.yaml
     - `env_loader.py` - Loads .env file
     - `logger.py` - Logging utility

## Critical Workflow Rules

### Status Progression
- Goals/Plans are created with status="draft"
- User manually changes draft→todo when ready
- Agents automatically handle todo→doing→done transitions

### Interactive Ticket Writing
Agents must write ticket content WITH users through conversation:
1. Draft meaningful content (not templates)
2. Show draft to user
3. Refine based on feedback
4. Save EXACT agreed content to Linear

### Relationship Management
- Multiple GitHub issues → One goal ticket
- Goal automatically updates to "doing" when plan created
- Plan and goal both update to "done" when module complete

## Configuration

### config.yaml
- `github.repo` - Repository for issues (e.g., "owner/repo")
- `linear.workspace` - Linear workspace name
- `linear.team_id` - Linear team identifier
- `linear.tickets.goal_label` - Label for goals (default: "goal")
- `linear.tickets.plan_label` - Label for plans (default: "plan")

### Environment (.env)
```bash
GITHUB_TOKEN=ghp_...      # GitHub personal access token
LINEAR_API_KEY=lin_api_... # Linear API key
```

## Module Development

Modules represent features and are organized in `modules/` directory:
- Each module is a self-contained feature
- Modules can be categorized (auth, api, ui, data, utils)
- Module Builder creates structure based on plan specifications

## Testing Scripts

```bash
# Test environment setup
./test-setup.sh  # Validates configuration and environment

# Test individual scripts
python .claude/scripts/goal-builder/list_issues.py
python .claude/scripts/plan-builder/list_goals.py
python .claude/scripts/module-builder/list_plans.py
```

## Important Implementation Notes

### When Creating/Modifying Commands
Commands in `.claude/commands/*/` should:
- Guide conversational workflows
- Include explicit approval steps
- Save draft content to temp files before creating tickets
- Use the `create_*_from_draft.py` scripts to preserve exact content

### When Working with Scripts
Python scripts in `.claude/scripts/*/`:
- Must import shared utilities using: `sys.path.insert(0, str(Path(__file__).parent.parent))`
- Should use the shared clients (GitHubClient, LinearClient) for API calls
- Must respect status rules (only process "todo" items, create as "draft")

### Linear API Integration
The LinearClient uses GraphQL with these key operations:
- Create issues with labels and status
- Update issue status following workflow rules
- Link child issues to parent (plan→goal relationship)
- Query issues by label and status combination

### GitHub Integration
GitHubClient operations:
- `get_open_issues()` - Fetch all open issues
- `close_issue(number, comment)` - Close with explanation
- Issues serve as "stash" for raw ideas