---
description: Interactively create a Linear goal ticket from selected GitHub issues
argument-hint: [issue-numbers] [--auto-update]
disable-model-invocation: false
---

# Create Goal Ticket

Work with the user to create a Linear goal ticket from GitHub issues.

---

## Arguments

**$ARGUMENTS** may contain:
1. **Issue numbers** (required): `11` or `11,12,15`
2. **--auto-update flag** (optional): Skip approval prompts

**Examples**:
- `/create-goal 11` → Normal mode (requires approval)
- `/create-goal 11 --auto-update` → Auto-update mode (no approval)
- `/create-goal 11,12,15` → Normal mode, multiple issues
- `/create-goal 11,12,15 --auto-update` → Auto-update mode, multiple issues

---

## Command-Specific Workflow

### Step 1: Parse Arguments

Extract issue numbers from $ARGUMENTS:
- Single: `11` → [11]
- Multiple: `11,12,15` → [11, 12, 15]
- Detect `--auto-update` flag presence

### Step 2: Load Full Issue Content

For EACH issue number provided, use `mcp__github__get_issue` to load complete issue body (not just preview).

**Why**: You need full issue content to draft comprehensive goal that captures all requirements.

If multiple issues:
- Load all of them
- Understand how they relate
- Group into cohesive feature goal

### Step 3: Initialize Version Tracking

Before creating ANY content:
```bash
echo "1" > .tmp/goal-version.txt
```

This starts version tracking at v1.

### Step 4: Draft Goal Content

**🚨 CRITICAL**: Write draft DIRECTLY to file WITHOUT showing in chat first!

1. ✅ Think about content internally
2. ✅ **Immediately** use Write tool: `.tmp/goal-draft-v1.md`
3. ✅ Use Read tool to show file to user
4. ✅ Use Edit tool to refine based on feedback

❌ **NEVER** show draft in chat before writing to file!

**Content Requirements**:
- Use goal template structure (from TEMPLATES.md - you know this from /prime)
- Include: Outcome, Scope, Non-Goals, Milestones, Metrics, Risks
- Use ```text for all interaction examples (prevents YAML detection)
- Add source GitHub issue references

### Step 5: Iterative Refinement

User may request changes. For EACH change:

1. Increment version: Read `.tmp/goal-version.txt`, increment, save
2. Save new version: `.tmp/goal-draft-v{N}.md`
3. Generate diff: `.tmp/goal-draft-v{N-1}-to-v{N}.diff`
4. Show diff to user

Repeat until user is satisfied.

### Step 6: Get Approval (Normal Mode) OR Auto-Proceed (Auto-Update Mode)

**If --auto-update flag WAS present**:
- State: "🔥 Auto-update mode. Creating in Linear immediately..."
- Proceed to Step 7 without waiting

**If --auto-update flag was NOT present (normal mode)**:
- Ask: "Should I create this goal in Linear?"
- Wait for approval phrases (you know these from system.md - loaded by /prime)
- Only proceed after explicit approval

### Step 7: Create in Linear

Use `mcp__linear__create_issue` with:
- teamId from config.yaml
- Label: "goal" (from config.yaml)
- State: "Draft"
- Title and description from latest goal-draft version

Save the returned goal ID (e.g., "SYS-10").

### Step 8: Close Source GitHub Issues

For EACH issue number that was used:
- Use `mcp__github__close_issue`
- Comment: "Closed: Created Linear goal {GOAL-ID} from this issue."

### Step 9: Archive Complete History

Move all versions and diffs to archive (you know the archive structure from system.md):
```
.tmp/archives/{GOAL-ID}/{TIMESTAMP}/
  ├── goal-draft-v1.md
  ├── goal-draft-v2.md
  ├── goal-draft-v{N}.md
  ├── goal-draft-v1-to-v2.diff
  ├── goal-draft-v{N-1}-to-v{N}.diff
  └── goal-version.txt
```

Clean up working directory (.tmp/goal-draft*.md, .tmp/goal-version.txt).

### Step 10: Confirm Success

Tell user:
- "✅ Created goal {GOAL-ID} in Linear with status=draft"
- "Closed GitHub issue(s): #{numbers}"
- "Archived {N} versions to .tmp/archives/{GOAL-ID}/"

---

## Command-Specific Edge Cases

### Issue Number Doesn't Exist
- Error: "GitHub issue #{number} not found"
- Ask user to verify issue number
- Don't proceed

### Multiple Unrelated Issues
- If issues seem unrelated, ask user: "These issues cover different areas. Should they be separate goals?"
- Let user decide
- Proceed with their choice

### Invalid Argument Format
- If arguments aren't numbers or comma-separated: "Invalid format. Use: /create-goal 11 or /create-goal 11,12,15"
- Show example
- Don't proceed

### Issue Already Closed
- Warn: "Issue #{number} is already closed. Still create goal from it?"
- Wait for confirmation
- Proceed if confirmed

---

## Notes

**Everything else you need is already in context from /prime**:
- Approval policy → system.md
- Version management details → system.md
- Archive system details → system.md
- MCP tool complete syntax → developer.md
- Goal template structure → TEMPLATES.md
- General workflow patterns → WORKFLOW.md

This file contains ONLY create-goal command-specific details.
