---
description: Analyze GitHub issues and suggest logical groupings for goals
disable-model-invocation: false
---

# Analyze Issues for Goal Groupings

Fetch GitHub issues and provide intelligent grouping suggestions.

## Instructions

1. Use `mcp__github__list_issues` to get all open issues (tool syntax in developer.md). Parse `github.repo` from config.yaml to extract owner and repo name.

2. Analyze the issues for:
   - Feature areas (authentication, UI, data, etc.)
   - Technical dependencies
   - Implementation complexity
   - Business priorities

3. Present grouping suggestions:
   - Group related issues that form complete features
   - Identify dependencies between issues
   - Suggest priority order
   - Estimate complexity for each group

4. Format output as:
```
**[Group Name]** ([Priority])
- #[number]: [title] ([complexity])
- #[number]: [title] ([complexity])
Rationale: [Why these belong together]

Estimated effort: [small/medium/large]
Dependencies: [any prerequisites]
```

5. Ask the user which grouping they'd like to convert into a goal

## Analysis Guidelines

### Feature Grouping Criteria
- Issues that implement a complete user-facing feature
- Issues that touch the same module or codebase area
- Issues that have shared technical requirements
- Issues that deliver cohesive business value

### Complexity Estimation
- **Small**: 1-2 days, single developer, minimal dependencies
- **Medium**: 3-5 days, 1-2 developers, some dependencies
- **Large**: 1-2 weeks, multiple developers, complex dependencies

### Priority Assessment
- **High**: Blockers, critical bugs, core features
- **Medium**: Important features, performance improvements
- **Low**: Nice-to-haves, technical debt, optimizations

## Example Analysis

```
**Authentication System** (High Priority)
- #11: Implement user registration ([medium])
- #12: Add password reset flow ([small])
- #15: OAuth integration ([large])
Rationale: These issues form a complete authentication feature. Registration and password reset are prerequisites for OAuth.

Estimated effort: Large (1-2 weeks)
Dependencies: Database schema must be ready first
Suggested goal: "Complete Authentication System"

**Dashboard UI** (Medium Priority)
- #18: Create dashboard layout ([medium])
- #19: Add data visualization ([medium])
Rationale: Both issues contribute to the main dashboard interface.

Estimated effort: Medium (3-5 days)
Dependencies: API endpoints must exist
Suggested goal: "User Dashboard Interface"
```

## Next Steps

After presenting analysis:
- Ask user which grouping to pursue first
- Offer to create a goal from selected grouping
- Suggest creating multiple goals if needed
- Guide user to `/create-goal [issue-numbers]`

## Error Handling

If issues can't be fetched:
- 401/403: "Check GITHUB_TOKEN in .env file"
- 404: "Repository not found. Verify github.repo in config.yaml"
- Network errors: Retry 2x with backoff
- Timeout: "Operation timed out. Check network connection."
