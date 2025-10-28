---
description: Load a plan and start implementation (interactive)
allowed-tools: Bash, Write, Read, Edit
---

# Load Plan and Start Implementation

Load a Linear plan ticket and begin interactive implementation.

## Process

### 1. Show Available Plans

First, list plans ready for implementation:

```bash
python .claude/scripts/module-builder/list_plans.py --status todo
```

### 2. Load Selected Plan

When user selects a plan:

```bash
python .claude/scripts/module-builder/load_plan.py <plan-id>
```

### 3. Update Status to "doing"

**CRITICAL**: Update BEFORE starting work:

```bash
python .claude/scripts/module-builder/update_plan_status.py \
  --plan-id "<plan-id>" \
  --status "doing"
```

### 4. Interactive Implementation

Work through each step WITH the user:

- Show the implementation steps
- For each step:
  - Explain what you're about to do
  - Show the code you're writing
  - Get feedback before proceeding
  - Test as you go
- Track progress through the steps
- Ask questions when design decisions arise

### 5. Testing During Implementation

Run tests frequently:

```bash
# Run tests for the module being built
python -m pytest modules/<module-name>/tests/ -v
```

### 6. Mark Complete When Done

After ALL steps are complete and tests pass:

```bash
python .claude/scripts/module-builder/mark_complete.py --plan-id "<plan-id>"
```

This will:
- Update plan from "doing" to "done"
- Update parent goal to "done"

## Important

- ONLY process plans with status="todo"
- ALWAYS update to "doing" before starting
- Work interactively through each step
- Test frequently during implementation
- Update BOTH plan and goal when complete
