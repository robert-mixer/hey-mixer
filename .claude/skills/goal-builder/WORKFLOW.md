# Goal Builder Detailed Workflow

## Phase 1: Discovery and Analysis

### Step 1: Assess Current Issues
```bash
python .claude/scripts/goal-builder/list_issues.py
```

**What to look for:**
- Natural groupings by feature area
- Dependencies between issues
- Quick wins vs. complex implementations
- Security or performance critical items

### Step 2: Suggest Groupings

Present logical groupings to the user:

```
Based on your open issues, I see three potential goals:

**Authentication System** (High Priority)
- #12: Add login form (UI)
- #15: JWT implementation (Backend)
- #18: Password reset (Feature)
These form a complete auth solution.

**Performance Optimization** (Medium Priority)
- #23: Database query optimization
- #27: Caching layer
These work together to improve response times.

**UI Improvements** (Lower Priority)
- #31: Dashboard redesign
- #33: Mobile responsiveness
Stand-alone UI enhancements.

Which would you like to tackle first?
```

## Phase 2: Interactive Drafting

### Step 1: Initial Draft

Start with a meaningful draft based on the selected issues:

```markdown
Here's my initial draft for the Authentication System goal:

# User Authentication System

Build a secure, modern authentication system that provides seamless user access management with industry-standard security practices.

## Requirements

- **User Registration**: Email-based signup with validation
- **Secure Login**: JWT-based authentication with refresh tokens
- **Session Management**: Persistent sessions with configurable timeout
- **Password Recovery**: Email-based reset flow with secure tokens
- **Security Features**: Rate limiting, CSRF protection, secure password hashing

[Continue with full draft...]

What would you like me to adjust?
```

### Step 2: Iterative Refinement

**Common refinement requests:**

- "Can you add MFA to the requirements?"
- "Let's specify the JWT expiration times"
- "Include migration from the old system"
- "Add performance requirements"

**Response approach:**
```
Great suggestion! I'll add MFA to the requirements. Here's the updated version:

[Show ONLY the changed section initially, then full draft if requested]
```

### Step 3: Final Approval

```
Here's the final version of our goal ticket:

[Show complete, formatted draft]

This looks perfect to me! Should I create this goal ticket in Linear now?
```

## Phase 3: Creation and Cleanup

### Step 1: Save Draft

```bash
# Save the exact content to a temporary file
cat > /tmp/goal-draft.md << 'EOF'
[Paste the EXACT markdown content that was approved]
EOF

echo "✅ Draft saved to /tmp/goal-draft.md"
```

### Step 2: Create Linear Ticket

```bash
python .claude/scripts/goal-builder/create_goal_from_draft.py \
  --draft-file "/tmp/goal-draft.md" \
  --issues "12,15,18" \
  --status "draft"
```

Expected output:
```
✅ Goal ticket created successfully!
📎 Linear URL: https://linear.app/workspace/issue/TEAM-123
🏷️ Labels: goal
📊 Status: draft
🔗 Linked issues: #12, #15, #18
```

### Step 3: Close GitHub Issues

```bash
python .claude/scripts/goal-builder/close_issues.py --issues "12,15,18" \
  --comment "Incorporated into Linear goal: User Authentication System (TEAM-123)"
```

### Step 4: Explain Next Steps

```
Perfect! Your goal has been created successfully. Here's what happens next:

✅ **Created**: "User Authentication System" goal in Linear (status: draft)
✅ **Archived**: GitHub issues #12, #15, #18 have been closed
📝 **Your Action**: Review the goal in Linear
🎯 **When Ready**: Change status from "draft" to "todo"
🚀 **Next Phase**: Plan Builder will create implementation plan when status is "todo"

The goal is currently in DRAFT status, giving you time to:
- Review and edit in Linear if needed
- Add any additional context
- Attach relevant documents
- Set priority and estimates

When you're satisfied, change the status to "todo" and the Plan Builder can create a detailed implementation plan.
```

## Phase 4: Handoff Points

### To Plan Builder
When goal status changes to "todo", the Plan Builder will:
1. Read the goal requirements
2. Create detailed implementation plan
3. Break down into concrete tasks
4. Define module structure

### Status Transitions
```
draft → todo: User is ready for planning (manual)
todo → doing: Plan created, implementation starting (automatic)
doing → done: Module implemented and tested (automatic)
```

## Best Practices

### DO:
- ✅ Write actual content, not templates
- ✅ Include all context in the goal
- ✅ Get explicit approval before creating
- ✅ Explain the workflow clearly
- ✅ Keep goals achievable (1-2 sprints)

### DON'T:
- ❌ Auto-generate generic content
- ❌ Create with status="todo"
- ❌ Skip the review phase
- ❌ Combine unrelated issues
- ❌ Make goals too large or vague

## Troubleshooting

### Issue: "Goal too large"
**Solution**: Split into multiple smaller goals with clear boundaries

### Issue: "Missing context"
**Solution**: Add Technical Considerations or Dependencies sections

### Issue: "Unclear requirements"
**Solution**: Make requirements specific and measurable

### Issue: "No module target"
**Solution**: Define where the code will live in the codebase

## Conversation Starters

Use these prompts to guide the conversation:

- "I see you have [N] open issues. Would you like me to suggest some logical groupings?"
- "These [N] issues seem related to [topic]. Should we create a goal for them?"
- "Let me draft a goal ticket for [feature]. We can refine it together."
- "What aspects of this goal are most important to you?"
- "Should we add any technical constraints or requirements?"
- "How would you like to handle [specific consideration]?"
- "This draft captures what we discussed. What would you like to adjust?"