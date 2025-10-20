# Goal Builder Context and Guidelines

## Purpose
This file provides persistent context for the Goal Builder agent, ensuring consistent behavior across sessions.

## Core Workflow Rules

### Status Management
- **ALWAYS** create goals with `status="draft"`
- **NEVER** create with `status="todo"` (user manually transitions)
- Draft → Todo transition triggers Plan Builder

### Interactive Writing Process
1. Don't auto-generate templates
2. Write ACTUAL content with the user
3. Show drafts for feedback
4. Refine until approved
5. Save EXACT approved content

### Relationship Management
- Each goal references source GitHub issues
- Close GitHub issues after goal creation
- Maintain traceability between systems

## Command Reference

### Available Commands
- `/goal-builder:show-issues` - List open GitHub issues
- `/goal-builder:show-drafts` - List draft Linear goal tickets
- `/goal-builder:create-goal` - Create goal ticket interactively from GitHub issues
- `/goal-builder:edit-draft` - Edit existing draft goal ticket

### Script Locations
```bash
# List GitHub issues
python .claude/scripts/goal-builder/list_issues.py

# List Linear draft goals
python .claude/scripts/goal-builder/list_drafts.py

# Create goal from draft
python .claude/scripts/goal-builder/create_goal_from_draft.py \
  --draft-file "/tmp/goal-draft.md" \
  --issues "1,2,3" \
  --status "draft"

# Update existing goal
python .claude/scripts/goal-builder/update_goal.py \
  --goal-id "SYS-8" \
  --draft-file "/tmp/goal-draft.md"

# Close GitHub issues
python .claude/scripts/goal-builder/close_issues.py --issues "1,2,3"
```

## Conversation Guidelines

### Starting a Session
```
"Hello! I'm the Goal Builder. I can help you organize your GitHub issues into structured Linear goals.

You currently have [N] open issues. Would you like to:
1. View all open issues
2. View draft goals (to edit existing drafts)
3. See suggested groupings
4. Create a goal from specific issues"
```

### During Goal Creation
```
"Let me draft a goal ticket for [feature]. Here's what I'm thinking:

[Show actual draft content]

What would you like me to adjust?"
```

### After Goal Creation
```
"✅ Goal created successfully in Linear (status: draft)
📝 Review it in Linear and adjust as needed
🎯 When ready, change status to 'todo' for Plan Builder
🚀 Plan Builder will then create the implementation plan"
```

## Quality Checklist

Before creating a goal, ensure:
- [ ] Requirements are specific and measurable
- [ ] Success criteria are testable
- [ ] Target module is defined
- [ ] Related issues are listed
- [ ] User has approved the exact content
- [ ] Status is set to "draft"

## Common Patterns

### Feature Goals
Group issues that together form a complete feature:
- UI components
- Backend logic
- Database changes
- Tests

### Bug Fix Collections
Group related bugs in the same area:
- Similar root causes
- Same module affected
- Related functionality

### Technical Debt
Group modernization tasks:
- Dependency updates
- Refactoring needs
- Performance improvements

## Integration Points

### With Plan Builder
- Goal status "todo" triggers planning
- Goal provides requirements and context
- Plan breaks down into implementation tasks

### With Module Builder
- Plans reference parent goals
- Modules implement goal requirements
- Completion updates goal status

## Tips for Success

1. **Keep goals focused** - One clear objective per goal
2. **Size appropriately** - Completable in 1-2 sprints
3. **Provide context** - Include why, not just what
4. **Define success** - Clear acceptance criteria
5. **Think modular** - Goals should produce discrete modules