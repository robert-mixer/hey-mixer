---
name: Goal Builder Workflow
description: Transform GitHub issues into Linear goal tickets. Use when organizing issues, creating goals, managing GitHub to Linear workflow, or when user mentions issue management.
allowed-tools: Read, Write, Bash(python:.claude/scripts/goal-builder/*), Grep, Glob
---

# Goal Builder Workflow

This skill provides structured workflows and templates for transforming GitHub issues into Linear goal tickets.

## 🔴 CRITICAL: ALWAYS USE YOUR COMMANDS 🔴

**MANDATORY**: You MUST use your slash commands for ALL actions:
- `/goal-builder:show-issues` - ALWAYS use this to show GitHub issues
- `/goal-builder:show-drafts` - ALWAYS use this to show draft Linear goals
- `/goal-builder:analyze-issues` - ALWAYS use this to analyze groupings
- `/goal-builder:create-goal [issue-numbers]` - ALWAYS use this to create new goals from issues
- `/goal-builder:edit-draft [goal-id]` - ALWAYS use this to edit existing draft goals
- `/goal-builder:save-draft` - ALWAYS use this to save drafts

**NEVER** manually list issues or create goals without these commands!

## Quick Start

### Creating New Goals from GitHub Issues

1. Use command: `/goal-builder:show-issues` (shows 200-char previews)
2. Use command: `/goal-builder:analyze-issues` for groupings
3. Use command: `/goal-builder:create-goal [numbers]` to draft WITH user
   - Command automatically loads full issue content via `load_issue.py`
   - Agent sees complete issue body, not just preview
4. Goal created in Linear with status="draft"
5. User manually changes draft→todo when ready

### Editing Existing Draft Goals

1. Use command: `/goal-builder:show-drafts` (shows 200-char previews)
2. User selects which draft to edit
3. Use command: `/goal-builder:edit-draft [goal-id]` to modify WITH user
   - Command automatically loads full goal content via `load_goal.py`
   - Agent sees complete description, not just preview
4. Goal updated in Linear (stays as "draft")
5. User manually changes draft→todo when ready

## Core Principles

- **Interactive Writing**: Draft real content with the user, not templates
- **Status Management**: Always create with status="draft"
- **Relationship Tracking**: Close GitHub issues after goal creation
- **User Control**: User decides when to transition draft→todo

## Workflow Steps

### Creating Goals from GitHub Issues

#### 1. Analyze GitHub Issues

```bash
# List all open issues (200-char previews)
python .claude/scripts/goal-builder/list_issues.py

# Load specific issue's FULL content
python .claude/scripts/goal-builder/load_issue.py --issue-number 11
```

Look for logical groupings:
- Feature areas (auth, UI, data, etc.)
- Technical dependencies
- Business priorities
- Implementation complexity

### 2. Interactive Goal Drafting with Version Management

Work WITH the user to write the actual ticket content. Each iteration is automatically versioned for full observability:

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

**Version Management:**
- Initial draft saved as `.tmp/goal-draft-v1.md`
- Each edit creates new version (v2, v3...)
- Diffs shown automatically after each change
- All versions cleaned up after successful creation/update

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

#### 4. Archive Source Issues

Close GitHub issues that were included:
```bash
python .claude/scripts/goal-builder/close_issues.py --issues "12,15,18"
```

### Editing Existing Draft Goals

#### 1. List Draft Goals

```bash
# List all draft goals (200-char previews)
python .claude/scripts/goal-builder/list_drafts.py
```

Shows all Linear goals with status="draft" that can be edited.

#### 2. Load and Edit Draft with Version Management

Work WITH the user to modify the existing goal content. All iterations are versioned:

```bash
# Load full goal content from Linear to draft file
python .claude/scripts/goal-builder/load_goal.py \
  --goal-id "SYS-8" \
  --description-only > .tmp/goal-draft.md

# Initialize versioning (loaded content is v1)
echo "1" > .tmp/goal-version.txt
cp .tmp/goal-draft.md .tmp/goal-draft-v1.md

# User provides changes
# Agent iteratively updates the file using Edit tool
# Each edit creates new version with automatic diff display
# Updates the exact content back to Linear
```

#### 3. Update in Linear

```bash
python .claude/scripts/goal-builder/update_goal.py \
  --goal-id "SYS-8" \
  --draft-file ".tmp/goal-draft.md"

# Clean up versions after successful update
if [ $? -eq 0 ]; then
  rm -f .tmp/goal-draft*.md .tmp/goal-version.txt
fi
```

The goal stays in "draft" status until user manually changes to "todo".

## Templates

For template examples, see [TEMPLATES.md](TEMPLATES.md).
For detailed workflow guidance, see [WORKFLOW.md](WORKFLOW.md).

## Important Notes

- Goals are building blocks for the Plan Builder
- Each goal should be substantial but achievable
- Group related issues that form a coherent feature
- The user controls the draft→todo transition