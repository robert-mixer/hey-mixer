---
description: Mark plan and goal as completed
allowed-tools: Bash
---

# Mark Plan and Goal Complete

Mark both the plan and its parent goal as completed after implementation.

## Process

### 1. Verify Completion

Before marking complete, ensure:
- All implementation steps are done
- Tests are passing
- Code is properly documented
- No outstanding issues

### 2. Run Tests One Final Time

```bash
# Run all tests to verify
python -m pytest modules/<module-name>/tests/ -v
```

### 3. Mark Both Tickets Complete

**CRITICAL**: Update BOTH plan and goal:

```bash
python .claude/scripts/module-builder/mark_complete.py --plan-id "<plan-id>"
```

This script will:
- Update plan from "doing" to "done"
- Update parent goal from "doing" to "done"
- Add completion timestamps to both
- Link completion notes

### 4. Summary

After marking complete:
- Summarize what was built
- List key features implemented
- Note any follow-up items

## Important

- ONLY mark complete when ALL steps are done
- Tests MUST be passing
- Updates BOTH plan and goal together
- Never mark partial implementations as complete
