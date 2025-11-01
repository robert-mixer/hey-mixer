---
description: Display all open GitHub issues from the configured repository
disable-model-invocation: false
---

# Show GitHub Issues

Display all open GitHub issues from the configured repository to start the goal creation workflow.

## Instructions

Use `mcp__github__list_issues` to fetch all open issues (tool syntax in developer.md).

**Configuration:** Repository information comes from `config.yaml` - parse the repo string to extract owner and repo name for MCP calls.

**Error Handling:**
- 401/403: "Check GITHUB_TOKEN in .env file"
- 404: "Repository not found. Verify github.repo in config.yaml"
- 429: Retry 2x with exponential backoff (1s, 2s)
- 5xx: Retry 2x with exponential backoff (1s, 2s)
- Timeout (30s): "Operation timed out. Check network connection."

After displaying issues:
1. Analyze the issues for logical groupings
2. Suggest which issues could be combined into goals
3. Ask the user what they'd like to work on

## Pagination

- Default limit: 20 items
- Display format: "Showing X of Y total" (when total count is known)
- If more than 20 issues, ask user if they want to see more
- Maximum recommended: 100 items (for performance)

## Example Output Format

For each issue, display:
- Issue number (e.g., #11)
- Title
- State (open/closed)
- Labels
- Created date
- Author
- Brief description (first 200 chars)
- URL

## Next Steps

After showing issues, ask the user:
- "Which issue(s) would you like to create goals from?"
- "Should we combine any related issues into a single goal?"
- "Would you like me to analyze and suggest groupings?"
