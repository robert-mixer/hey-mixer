---
description: Create a plan ticket from a goal (interactive)
allowed-tools: Bash, Write, Read
---

# Create Plan Ticket

Work with the user to create a Linear plan ticket from a goal ticket.

## Process

This is an INTERACTIVE process where you WRITE THE PLAN WITH THE USER.

### 1. Load Goals with status="todo"

First, get goals that are ready for planning:

```bash
python .claude/scripts/plan-builder/list_goals.py --status todo
```

### 2. Load Selected Goal

Once user selects a goal:

```bash
python .claude/scripts/plan-builder/load_goal.py <goal-id>
```

### 3. Draft Plan Content Interactively

**CRITICAL**: Don't auto-generate. WRITE THE ACTUAL PLAN with the user:

- Analyze the goal's requirements
- Draft implementation steps (numbered, clear)
- Include sections like:
  - Goal Reference
  - Target
  - Implementation Steps (detailed)
  - Technical Approach
  - Dependencies
  - Success Criteria
- Show the draft to the user
- Refine based on feedback
- Continue until user approves

### 4. Save Draft and Get Approval

Once the user approves:

```bash
# Save the exact plan content to a temporary file
cat > /tmp/plan-draft.md << 'EOF'
[PASTE THE EXACT MARKDOWN CONTENT HERE]
EOF
```

### 5. Create Plan and Update Goal

```bash
# Create the plan ticket with draft content
python .claude/scripts/plan-builder/create_plan_from_draft.py \
  --draft-file "/tmp/plan-draft.md" \
  --goal-id "<goal-id>" \
  --status "draft"
```

This script will:
- Create plan with status="draft"
- Link plan to parent goal
- Update goal from "todo" to "doing"

### 6. Explain Next Steps

Tell the user:
- Plan is in "draft" status
- Goal has been updated to "doing"
- When ready, change plan to "todo" for Module Builder

## Important

- ONLY process goals with status="todo"
- ALWAYS create plans with status="draft"
- IMMEDIATELY update goal to "doing"
- Link plan to parent goal
- The plan contains EXACTLY what you wrote together
