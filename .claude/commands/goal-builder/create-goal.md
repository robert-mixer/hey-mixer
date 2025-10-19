---
description: Interactively create a Linear goal ticket from selected GitHub issues
allowed-tools: Bash(python:.claude/scripts/goal-builder/*), Write, Read
argument-hint: [issue-numbers]
disable-model-invocation: false
---

# Create Goal Ticket

Work with the user to create a Linear goal ticket from GitHub issues.

## Process

This is an INTERACTIVE process where you WRITE THE TICKET CONTENT WITH THE USER.

### 1. Load GitHub Issues

First, get the list of open issues:

```bash
python .claude/scripts/goal-builder/list_issues.py
```

### 2. Draft Ticket Content Interactively

**CRITICAL**: Don't auto-generate content. WRITE THE ACTUAL TICKET with the user:

- Discuss which issues to include
- Draft the goal ticket content in markdown
- Include sections like:
  - Description (what needs to be built)
  - Requirements
  - Success Criteria
  - Target (e.g., `modules/auth/`)
  - Related GitHub Issues
- Show the draft to the user
- Refine based on feedback
- Continue until user says it's perfect

### 3. Save Draft and Get Approval

Once the user approves the content:

```bash
# Save the exact draft content to a temporary file
cat > /tmp/goal-draft.md << 'EOF'
[PASTE THE EXACT MARKDOWN CONTENT HERE]
EOF
```

Show the final version and get explicit approval.

### 4. Create Ticket with Exact Draft Content

```bash
# Create the Linear goal ticket with the draft content
python .claude/scripts/goal-builder/create_goal_from_draft.py \
  --draft-file "/tmp/goal-draft.md" \
  --issues "12,15,18" \
  --status "draft"
```

### 5. Close GitHub Issues

After successfully creating the goal:

```bash
# Close the GitHub issues that were included
python .claude/scripts/goal-builder/close_issues.py --issues "12,15,18"
```

### 6. Explain Next Steps

Tell the user:
- The goal is now in "draft" status
- They should review it in Linear
- When ready, change status to "todo" for Plan Builder

## Important

- ALWAYS create with status="draft"
- Get user approval before creating
- The ticket contains EXACTLY what you wrote together
- Close GitHub issues after creating goal
- Explain the draft→todo transition
