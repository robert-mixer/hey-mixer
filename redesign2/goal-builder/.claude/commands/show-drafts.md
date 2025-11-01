---
description: Display all draft Linear goal tickets that can be edited
disable-model-invocation: false
---

# Show Draft Goals

Display all Linear goal tickets with status="draft" to review or edit them.

## Instructions

Use `mcp__linear__list_issues` to fetch all draft goals with filters for status="draft" and label="goal" (tool syntax in developer.md).

**Configuration notes:**
- Goal label name comes from `config.yaml` → `linear.tickets.goal_label` (default: "goal")
- Team filtering uses `linear.team_id` from config.yaml

**Error Handling:**
- 401/403: "Check LINEAR_API_KEY in .env file"
- 404: "Team not found. Verify linear.team_id in config.yaml"
- 429: Retry 2x with exponential backoff (1s, 2s)
- 5xx: Retry 2x with exponential backoff (1s, 2s)
- Timeout (30s): "Operation timed out. Check network connection."

After displaying drafts:
1. Show the user which draft goals exist
2. Ask if they want to edit any of them
3. If yes, guide them to use `/edit-draft [goal-id]`

## Pagination

- Default limit: 20 items
- Display format: "Showing X of Y total"
- If more than 20 drafts, ask user if they want to see more

## Example Output

For each draft goal, display:
- Goal identifier (e.g., SYS-8)
- Title
- Current status (draft)
- URL to view in Linear
- Description preview (first 200 chars)
- Created date
- Related GitHub issues (if listed in description)

## Next Steps

After showing drafts, ask the user:
- "Would you like to edit any of these draft goals?"
- "Or would you like to create a new goal instead?"
- "You can use `/edit-draft [goal-id]` to edit"
