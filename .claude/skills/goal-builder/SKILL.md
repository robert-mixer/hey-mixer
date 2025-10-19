---
name: Goal Builder Workflow
description: Transform GitHub issues into Linear goal tickets. Use when organizing issues, creating goals, managing GitHub to Linear workflow, or when user mentions issue management.
allowed-tools: Read, Write, Bash(python:.claude/scripts/goal-builder/*), Grep, Glob
---

# Goal Builder Workflow

This skill provides structured workflows and templates for transforming GitHub issues into Linear goal tickets.

## 🔴 CRITICAL: ALWAYS USE YOUR COMMANDS 🔴

**MANDATORY**: You MUST use your slash commands for ALL actions:
- `/goal-builder:show-issues` - ALWAYS use this to show issues
- `/goal-builder:analyze-issues` - ALWAYS use this to analyze groupings
- `/goal-builder:create-goal [issue-numbers]` - ALWAYS use this to create goals
- `/goal-builder:save-draft` - ALWAYS use this to save drafts

**NEVER** manually list issues or create goals without these commands!

## Quick Start

1. Use command: `/goal-builder:show-issues`
2. Use command: `/goal-builder:analyze-issues` for groupings
3. Use command: `/goal-builder:create-goal [numbers]` to draft WITH user
4. Goal created in Linear with status="draft"
5. User manually changes draft→todo when ready

## Core Principles

- **Interactive Writing**: Draft real content with the user, not templates
- **Status Management**: Always create with status="draft"
- **Relationship Tracking**: Close GitHub issues after goal creation
- **User Control**: User decides when to transition draft→todo

## Workflow Steps

### 1. Analyze GitHub Issues

```bash
python .claude/scripts/goal-builder/list_issues.py
```

Look for logical groupings:
- Feature areas (auth, UI, data, etc.)
- Technical dependencies
- Business priorities
- Implementation complexity

### 2. Interactive Goal Drafting

Work WITH the user to write the actual ticket content:

```markdown
# [Goal Title]

[Description of what needs to be built]

## Requirements
- [Specific, measurable requirements]

## Success Criteria
- [Testable outcomes]

## Target
`modules/[module-name]/` - [Description]

## Related GitHub Issues
- #[number]: [title]
```

### 3. Save and Create

Save the exact draft content:
```bash
cat > /tmp/goal-draft.md << 'EOF'
[EXACT CONTENT FROM CONVERSATION]
EOF
```

Create in Linear:
```bash
python .claude/scripts/goal-builder/create_goal_from_draft.py \
  --draft-file "/tmp/goal-draft.md" \
  --issues "12,15,18" \
  --status "draft"
```

### 4. Archive Source Issues

Close GitHub issues that were included:
```bash
python .claude/scripts/goal-builder/close_issues.py --issues "12,15,18"
```

## Templates

For template examples, see [TEMPLATES.md](TEMPLATES.md).
For detailed workflow guidance, see [WORKFLOW.md](WORKFLOW.md).

## Important Notes

- Goals are building blocks for the Plan Builder
- Each goal should be substantial but achievable
- Group related issues that form a coherent feature
- The user controls the draft→todo transition