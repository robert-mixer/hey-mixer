---
name: Goal Builder Workflow
description: Transform GitHub issues into Linear goal tickets. Use when organizing issues, creating goals, managing GitHub to Linear workflow, or when user mentions issue management.
---

# Goal Builder Workflow

This skill provides structured workflows and templates for transforming GitHub issues into Linear goal tickets using MCP servers.

## 🔴 CRITICAL: ALWAYS USE YOUR COMMANDS 🔴

**MANDATORY**: You MUST use your slash commands for ALL actions:
- `/show-issues` - ALWAYS use this to show GitHub issues
- `/show-drafts` - ALWAYS use this to show draft Linear goals
- `/analyze-issues` - ALWAYS use this to analyze groupings
- `/create-goal [issue-numbers]` - ALWAYS use this to create new goals from issues
- `/edit-draft [goal-id]` - ALWAYS use this to edit existing draft goals
- `/save-draft` - ALWAYS use this to save drafts

**NEVER** manually list issues or create goals without these commands!

## Quick Start

### Creating New Goals from GitHub Issues

1. Use command: `/show-issues` (shows GitHub issues via MCP)
2. Use command: `/analyze-issues` for groupings
3. Use command: `/create-goal [numbers]` to draft WITH user
   - Command automatically loads full issue content via GitHub MCP
   - Agent sees complete issue body, not just preview
4. Goal created in Linear with status="draft" via Linear MCP
5. User manually changes draft→todo when ready

### Editing Existing Draft Goals

1. Use command: `/show-drafts` (shows draft goals via Linear MCP)
2. User selects which draft to edit
3. Use command: `/edit-draft [goal-id]` to modify WITH user
   - Command automatically loads full goal content via Linear MCP
   - Agent sees complete description, not just preview
4. Goal updated in Linear (stays as "draft")
5. User manually changes draft→todo when ready

## Core Principles

- **Interactive Writing**: Draft real content with the user, not templates
- **Status Management**: Always create with status="draft"
- **Relationship Tracking**: Close GitHub issues after goal creation
- **User Control**: User decides when to transition draft→todo
- **MCP Integration**: All GitHub and Linear operations use MCP servers

## Workflow Steps

For detailed step-by-step workflows, see [WORKFLOW.md](WORKFLOW.md).

## Templates

For template examples, see [TEMPLATES.md](TEMPLATES.md).

## Important Notes

- Goals are building blocks for the Plan Builder
- Each goal should be substantial but achievable
- Group related issues that form a coherent feature
- The user controls the draft→todo transition
- All API operations use MCP servers (not Python scripts)
