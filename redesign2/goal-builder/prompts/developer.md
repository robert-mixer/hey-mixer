# Developer Essentials

<!-- PURPOSE: Critical technical information for development -->
<!-- LOADED BY: /prime command at startup -->
<!-- CONTAINS: Only absolutely essential technical details -->
<!-- DOES NOT CONTAIN: Workflows (see WORKFLOW.md), Complete MCP specs (inline in commands) -->

## 🔴 CRITICAL: Code Block Formatting

**ALWAYS use ```text for interaction examples in goal tickets:**

✅ **CORRECT**:
````text
User: "create auth endpoint"
System: "Created POST /api/auth/login"
````

❌ **WRONG** (triggers YAML detection):
````
User: "create auth endpoint"
System: "Created POST /api/auth/login"
````

**WHY**: Code blocks with `Key: value` patterns (User:, API:, Response:) trigger YAML auto-detection in Linear without explicit language specifiers. Using ```text prevents this and ensures proper "copy as markdown" functionality.

**This applies to**:
- Example interactions
- API request/response examples
- CLI command examples
- Voice command examples
- Any content with colon-based patterns

## MCP Tool Reference (Complete)

The agent uses Model Context Protocol servers for external integrations. All tool syntax is documented here.

### GitHub MCP Tools

**Tool: `mcp__github__list_issues`**
```json
{
  "owner": "{from config.yaml: github.repo owner}",
  "repo": "{from config.yaml: github.repo name}",
  "state": "open"
}
```
Returns: List of open issues with number, title, state, labels

**Tool: `mcp__github__get_issue`**
```json
{
  "owner": "{from config.yaml: github.repo owner}",
  "repo": "{from config.yaml: github.repo name}",
  "issue_number": 11
}
```
Returns: Complete issue with body, comments, full context

**Tool: `mcp__github__close_issue`**
```json
{
  "owner": "{from config.yaml: github.repo owner}",
  "repo": "{from config.yaml: github.repo name}",
  "issue_number": 11,
  "comment": "Closed: Created Linear goal SYS-10 from this issue."
}
```
Returns: Success confirmation

### Linear MCP Tools

**Tool: `mcp__linear__list_issues`**
```json
{
  "filter": {
    "labels": {
      "name": {"eq": "goal"}
    },
    "state": {
      "name": {"eq": "Draft"}
    }
  }
}
```
Returns: List of issues matching filter (goals with status=draft)

**Tool: `mcp__linear__get_issue`**
```json
{
  "id": "{Linear issue ID or identifier like SYS-10}"
}
```
Returns: Complete issue with description, status, all fields

**Tool: `mcp__linear__create_issue`**
```json
{
  "teamId": "{from config.yaml: linear.team_id}",
  "title": "Goal title here",
  "description": "Complete goal content in markdown",
  "labelIds": ["{goal label ID}"],
  "stateId": "{Draft state ID}"
}
```
Returns: Created issue with ID, identifier (e.g., SYS-10)

**Tool: `mcp__linear__update_issue`**
```json
{
  "id": "{Linear issue ID}",
  "title": "Updated title",
  "description": "Updated complete content"
}
```
Returns: Updated issue confirmation

### Configuration Values

**From config.yaml** (via symlink from ../shared/config.yaml):
- `github.repo`: Format is "owner/repo-name" (split on "/")
- `linear.workspace`: Workspace name
- `linear.team_id`: UUID for the team
- `linear.tickets.goal_label`: Label name for goals (default: "goal")

**From .env** (via symlink from ../shared/.env):
- `GITHUB_TOKEN`: GitHub personal access token
- `LINEAR_API_KEY`: Linear API key

MCP servers automatically use these environment variables.

## Configuration Sources

### config.yaml
Located at `../shared/config.yaml` (symlinked to workspace root)

```yaml
github:
  repo: "owner/repo-name"

linear:
  workspace: "workspace-name"
  team_id: "TEAM-UUID"
  tickets:
    goal_label: "goal"
```

### .env
Located at `../shared/.env` (symlinked to workspace root)

```bash
GITHUB_TOKEN=ghp_xxxxxxxxxxxxx
LINEAR_API_KEY=lin_api_xxxxxxxxxxxxx
```
