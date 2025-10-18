# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## System Overview

The Mixer System is a conversational AI workflow for transforming ideas into code through structured project management. It uses three specialized Claude agents to process GitHub Issues → Linear Goal Tickets → Linear Plan Tickets → Code Modules.

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
- `/goal-builder:create-goal` - Interactively create goal ticket from issues

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