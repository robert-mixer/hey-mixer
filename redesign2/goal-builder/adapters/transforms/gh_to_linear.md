<!-- PURPOSE: Field mapping documentation for GitHub → Linear transformations -->
<!-- LOADED BY: /prime command at startup -->
<!-- CONTAINS: Transformation rules, parsing strategies, quality enhancement -->

# GitHub Issue to Linear Goal Field Mappings

This document defines how GitHub issue fields map to Linear goal ticket fields.

## Direct Mappings

| GitHub Field | Linear Field | Transformation |
|--------------|--------------|----------------|
| `issue.title` | `goal.title` | Use as-is, optionally enhance for clarity |
| `issue.number` | `goal.description` | Reference as "Related GitHub Issues: #X" |
| `issue.url` | `goal.description` | Include link in Related Issues section |
| `issue.body` | `goal.description` | Parse into structured sections (see below) |
| `issue.created_at` | - | Not mapped (informational only) |
| `issue.author` | - | Reference in description if relevant |

## Status Mapping

| GitHub Status | Linear Status | Note |
|---------------|---------------|------|
| `open` | `draft` | ALWAYS create as draft |
| `closed` | - | Close after goal creation |

## Label Mapping

| GitHub Label | Linear Label | Action |
|--------------|--------------|--------|
| `bug` | - | Inform goal type (bug fix collection) |
| `enhancement` | `goal` | ALWAYS add "goal" label |
| `feature` | `goal` | ALWAYS add "goal" label |
| `documentation` | - | Consider if worth a goal |
| Custom labels | - | Mention in description if relevant |

## Body Parsing Strategies

### Strategy 1: Markdown Structure Preservation

If the GitHub issue body already has markdown structure:

```markdown
# Original Issue Body

## Background
[context]

## Requirements
- Requirement 1
- Requirement 2

## Acceptance Criteria
- Criterion 1
- Criterion 2
```

**Transform to:**

```markdown
# [Enhanced Title]

## Outcome
[Synthesize from context and requirements]

## Scope
- Requirement 1 (from issue)
- Requirement 2 (from issue)

## Success Criteria (from Acceptance Criteria)
- Criterion 1
- Criterion 2

## Non-Goals
[Add explicit boundaries]

## Milestones
[Add 3-5 key checkpoints]

## Metrics
[Add quantifiable measures]

## Risks
[Identify potential blockers]

## Related GitHub Issues
- #X: [Original issue title]
```

### Strategy 2: Unstructured Text Processing

If the GitHub issue body is plain text:

1. **Extract intent**: What needs to be built?
2. **Identify requirements**: What are the key needs?
3. **Define boundaries**: What's out of scope?
4. **Add structure**: Apply goal ticket quality bars
5. **Enhance**: Add missing sections (milestones, metrics, risks)

**Example Transformation:**

GitHub Issue:
```
We need a login system. Users should be able to register,
login, and reset passwords. Make it secure.
```

Linear Goal:
```markdown
# User Authentication System

Build a secure authentication system that enables user registration,
login, and password recovery with industry-standard security practices.

## Outcome
Users can securely create accounts, authenticate, and recover access
to the application using email-based authentication.

## Scope
- User registration with email validation
- Secure login with JWT tokens
- Password reset flow
- Session management
- Rate limiting and CSRF protection

## Non-Goals
- Social media authentication (future phase)
- Multi-factor authentication (separate goal)
- Single sign-on integration

## Milestones
1. Database schema and user model
2. Registration and email validation
3. Login flow with JWT
4. Password reset functionality
5. Security hardening and testing

## Metrics
- 99.9% uptime for auth service
- < 200ms average response time
- Zero security vulnerabilities in audit
- 100% test coverage on critical paths

## Risks
- **Risk**: Password reset emails may be marked as spam
  **Mitigation**: Use reputable email service, implement SPF/DKIM
- **Risk**: Token expiration may disrupt user sessions
  **Mitigation**: Implement refresh tokens, clear expiration messaging

## Related GitHub Issues
- #12: Login system needed
```

### Strategy 3: Issue Body with Examples

If the issue contains example interactions:

**Preserve and enhance the examples in a dedicated section:**

```markdown
## Examples

```text
User: "sign up with email@example.com"
System: "Verification email sent to email@example.com"

User: clicks verification link
System: "Account verified! You can now log in."

User: enters credentials
System: "Welcome back! Session expires in 24 hours."
```
```

**CRITICAL**: Always use ```text language specifier for examples to prevent YAML detection in Linear.

## Quality Enhancement Rules

### ALWAYS Add (if missing):

1. **Outcome Section** (1-2 sentences)
   - Synthesize from issue content
   - Make it measurable and clear

2. **Non-Goals Section**
   - Identify scope boundaries
   - Prevent feature creep

3. **Milestones Section** (3-5 items)
   - Break down implementation phases
   - Show progress checkpoints

4. **Metrics Section**
   - Add quantifiable success measures
   - Include performance, reliability, coverage targets

5. **Risks Section** (2-3 items)
   - Anticipate potential blockers
   - Provide mitigation strategies

### OPTIONALLY Add (when beneficial):

1. **Examples Section** (HIGHLY RECOMMENDED for interactive features)
   - Required for: voice commands, APIs, chatbots, CLI tools
   - Show 2-10 concrete interaction scenarios
   - Use ```text code blocks

2. **Technical Considerations**
   - Architecture patterns
   - Key dependencies
   - Performance constraints

3. **Target**
   - Module path (e.g., `modules/auth/`)
   - Where code will live

## Title Enhancement

### Patterns:

- **Original**: "add login"
- **Enhanced**: "User Authentication System"

- **Original**: "fix slow queries"
- **Enhanced**: "Database Performance Optimization"

- **Original**: "update ui"
- **Enhanced**: "Dashboard UI Modernization"

### Rules:

- Make titles descriptive and professional
- Use title case
- Focus on the feature/outcome, not the action
- Keep under 60 characters

## Multi-Issue Consolidation

When combining multiple GitHub issues into one goal:

```markdown
## Related GitHub Issues

- #12: Add login form (UI)
- #15: JWT implementation (Backend)
- #18: Password reset flow (Feature)

These issues form a complete authentication system.
```

**Consolidation Rules:**

1. Issues must be logically related
2. Together they form a coherent feature
3. Dependencies between issues are clear
4. Combined scope is still achievable (1-2 sprints)

## Parsing Edge Cases

### Case: Issue is Too Vague

**Problem**: "Make the app better"

**Solution**:
1. Ask user for clarification
2. Don't auto-generate generic content
3. Work interactively to define concrete requirements

### Case: Issue is Too Large

**Problem**: Issue describes 10+ features

**Solution**:
1. Identify logical subgroups
2. Suggest splitting into multiple goals
3. Let user decide groupings

### Case: Issue Has No Clear Requirements

**Problem**: "We should have X" without details

**Solution**:
1. Use issue as starting point
2. Work with user to define requirements
3. Add structure through conversation

## Configuration Sources

### config.yaml

```yaml
github:
  repo: "owner/repo-name"

linear:
  workspace: "workspace-name"
  team_id: "TEAM-UUID"
  tickets:
    goal_label: "goal"
```

### Field Extraction

```bash
# Parse repo owner and name
REPO="owner/repo-name"
OWNER=$(echo $REPO | cut -d'/' -f1)
REPO_NAME=$(echo $REPO | cut -d'/' -f2)

# Use in MCP calls
mcp__github__get_issue(owner=$OWNER, repo=$REPO_NAME, issue_number=11)
```

## Validation Rules

Before creating a Linear goal, validate:

- [ ] Title is descriptive and professional
- [ ] Outcome section exists (1-2 sentences)
- [ ] Scope section has specific requirements
- [ ] Non-Goals section defines boundaries
- [ ] Milestones section has 3-5 checkpoints
- [ ] Metrics section has quantifiable measures
- [ ] Risks section has 2-3 items with mitigations
- [ ] Examples section included for interactive features (if applicable)
- [ ] All code blocks use ```text for interaction examples
- [ ] Related GitHub Issues section references source issues
- [ ] Content is comprehensive and addresses all requirements
- [ ] Status set to "draft"
- [ ] Label includes "goal"

## Examples

### Example 1: Simple Enhancement

**GitHub Issue #45**:
```
Title: Add dark mode
Body: Users want a dark mode option in settings
```

**Linear Goal**:
```markdown
# Dark Mode Theme Support

Implement a dark mode theme option that allows users to switch between
light and dark color schemes for improved accessibility and user preference.

## Outcome
Users can toggle between light and dark themes, with their preference
persisted across sessions.

## Scope
- Theme toggle in user settings
- Dark mode color palette
- Persistent theme preference
- Smooth theme transition
- Apply to all UI components

## Non-Goals
- Custom theme creation (future phase)
- Per-page theme settings
- Automatic theme based on time of day

## Milestones
1. Define dark mode color palette
2. Implement theme context and state management
3. Create theme toggle UI component
4. Apply dark mode styles to all pages
5. Test accessibility and contrast ratios

## Metrics
- WCAG AA contrast compliance for all text
- < 100ms theme switch transition
- 100% UI component coverage
- Zero layout shift during transition

## Risks
- **Risk**: Some UI components may not support dark mode
  **Mitigation**: Audit all components, create compatibility matrix
- **Risk**: Third-party widgets may not match theme
  **Mitigation**: Create theme wrapper utilities

## Target
`modules/ui/theme/` - Theme management module

## Related GitHub Issues
- #45: Add dark mode
```

### Example 2: Multiple Issues

**GitHub Issues**:
- #12: "Add login form"
- #15: "Implement JWT"
- #18: "Password reset"

**Linear Goal**: (See "Strategy 2" example above)

## Best Practices

1. **Preserve user intent**: Don't completely rewrite, enhance
2. **Ask when unclear**: Better to clarify than guess
3. **Be specific**: Replace vague terms with concrete details
4. **Add structure**: GitHub is free-form, Linear goals need sections
5. **Include examples**: Especially for interactive/conversational features
6. **Use ```text**: For all interaction examples to prevent YAML detection
7. **Quality over speed**: Take time to write comprehensive goals
8. **Collaborate**: Write WITH the user, not FOR them
