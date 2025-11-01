# Shared Resources

<!-- PURPOSE: Document shared configuration and credentials -->
<!-- AUDIENCE: Developers and users setting up the system -->

This directory contains configuration and credentials shared by all agents in the Mixer system.

## Contents

### config.yaml
System-wide configuration for GitHub, Linear, and agent behavior.

**What's configured:**
- **GitHub Integration**: Repository, issue tracking
- **Linear Integration**: Workspace, team ID, label conventions, status names
- **Module Types**: Base directory and module categories
- **Agent Settings**: Timezone and behavior for each agent

**Who uses it:**
- All builder agents (goal-builder, plan-builder, module-builder)
- Orchestrator (for understanding system configuration)

**When to update:**
- Changing GitHub repository
- Changing Linear workspace or team
- Modifying label conventions
- Adding new module types
- Adjusting agent behavior

### .env
API credentials and tokens for external services.

**What's configured:**
- `GITHUB_TOKEN` - GitHub Personal Access Token
- `LINEAR_API_KEY` - Linear API Key

**Who uses it:**
- All builder agents (via MCP servers)
- MCP servers read these environment variables

**When to update:**
- Token rotation (security practice)
- Switching accounts
- Token expiration
- Permission changes

### README.md (this file)
Documentation about shared resources.

---

## Why Shared Resources?

### The Problem
Multiple agents need to:
- Access the same GitHub repository
- Work with the same Linear workspace
- Use consistent label conventions
- Share API credentials

### The Solution
**Centralized configuration** = Single source of truth

**Benefits:**
- ✅ **Consistency**: All agents use same settings
- ✅ **Maintainability**: Update once, affects all agents
- ✅ **Security**: One place to manage credentials
- ✅ **Simplicity**: No duplicate configuration files

---

## Configuration Details

### config.yaml Structure

```yaml
# Project metadata
project:
  name: "hey-mixer"
  version: "1.0.0"

# GitHub integration
github:
  enabled: true
  repo: "owner/repository-name"    # Format: owner/repo
  stash:
    use_issues: true               # Use issues as idea stash
  auth:
    token_env: "GITHUB_TOKEN"      # Env var name for token

# Linear integration
linear:
  enabled: true
  workspace: "WorkspaceName"       # Your Linear workspace name
  team_id: "TEAM"                  # Team prefix (e.g., SYS, ENG)
  tickets:
    goal_label: "goal"             # Label for goal tickets
    plan_label: "plan"             # Label for plan tickets
    statuses:
      draft: "Draft"               # Needs review
      todo: "Todo"                 # Ready for work
      doing: "In Progress"         # Work started
      done: "Done"                 # Completed
      closed: "Canceled"           # Canceled
  auth:
    api_key_env: "LINEAR_API_KEY"  # Env var name for API key

# Module configuration
modules:
  base_dir: "modules/"             # Where feature modules live
  types:
    - name: "general"
      enabled: true
      description: "General purpose modules"

# Agent-specific settings
agents:
  goal_builder:
    timezone: "America/Los_Angeles"
  plan_builder:
    timezone: "America/Los_Angeles"
  module_builder:
    timezone: "America/Los_Angeles"
```

### .env Structure

```bash
# GitHub Configuration
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Linear Configuration
LINEAR_API_KEY=lin_api_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**IMPORTANT**: Never commit `.env` to version control! It should be in `.gitignore`.

---

## Setup Instructions

### Initial Setup

1. **Copy .env template** (if you don't have .env yet):
   ```bash
   cd /Users/Shyroian/mixer-backend/hey-mixer/redesign2/shared
   # Create .env with your tokens
   ```

2. **Get GitHub Token**:
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Generate new token (classic)
   - Required scopes: `repo` (full repository access)
   - Copy token to `GITHUB_TOKEN` in `.env`

3. **Get Linear API Key**:
   - Go to Linear Settings → API
   - Create new API key
   - Copy key to `LINEAR_API_KEY` in `.env`

4. **Update config.yaml**:
   ```yaml
   github:
     repo: "your-org/your-repo"  # Replace with your GitHub repo

   linear:
     workspace: "YourWorkspace"  # Replace with your Linear workspace
     team_id: "TEAM"             # Replace with your team prefix
   ```

### Updating Configuration

#### Change GitHub Repository
Edit `config.yaml`:
```yaml
github:
  repo: "new-owner/new-repo"
```

All agents will now work with the new repository.

#### Change Linear Workspace
Edit `config.yaml`:
```yaml
linear:
  workspace: "NewWorkspace"
  team_id: "NEW"
```

All agents will now create tickets in the new workspace.

#### Rotate Tokens (Security Best Practice)
Edit `.env`:
```bash
GITHUB_TOKEN=ghp_newTokenHere
LINEAR_API_KEY=lin_api_newKeyHere
```

All agents will use new credentials on next session.

---

## How Agents Use Shared Resources

### At Runtime

1. **Agents launch** (via run.sh)
2. **MCP servers start** (configured in each agent's settings.json)
3. **MCP servers read** environment variables from `.env`
4. **Agents read** `config.yaml` for repository/workspace info
5. **Agents use MCP tools** to interact with GitHub/Linear

### Example: Creating a Goal

```
Goal Builder launches
    ↓
Reads config.yaml: github.repo = "owner/repo"
    ↓
Reads config.yaml: linear.workspace = "Workspace", team_id = "SYS"
    ↓
MCP GitHub server: Uses GITHUB_TOKEN from .env
    ↓
Fetches issues from "owner/repo"
    ↓
User selects issue #11
    ↓
Agent drafts goal
    ↓
MCP Linear server: Uses LINEAR_API_KEY from .env
    ↓
Creates goal in Linear workspace "Workspace" with team prefix "SYS"
    ↓
Result: Goal "SYS-10" created in Linear
```

---

## Workspace Isolation

### What IS Shared
- ✅ `config.yaml` - System-wide configuration
- ✅ `.env` - API credentials
- ✅ That's it!

### What is NOT Shared
- ❌ Agent identities (CLAUDE.md)
- ❌ Agent behaviors (prompts/)
- ❌ Agent commands (.claude/commands/)
- ❌ Agent skills (.claude/skills/)
- ❌ Agent working directories (.tmp/)

**Why?**
- Each agent is **completely isolated** except for shared config/credentials
- This maintains clear boundaries and prevents context pollution
- Agents can evolve independently

---

## Security Considerations

### .env Security

**DO:**
- ✅ Keep `.env` in `.gitignore`
- ✅ Rotate tokens regularly (every 90 days recommended)
- ✅ Use minimum required permissions
- ✅ Keep `.env` file permissions restricted (`chmod 600 .env`)

**DON'T:**
- ❌ Commit `.env` to version control
- ❌ Share tokens in chat or email
- ❌ Use overly permissive tokens
- ❌ Reuse tokens across projects

### Token Permissions

**GitHub Token (ghp_...):**
- Required: `repo` scope
- Allows: Read/write issues, close issues
- Does NOT need: Admin, workflow, or package permissions

**Linear API Key (lin_api_...):**
- Required: Read/write issues
- Allows: Create/update/read issues, manage status
- Check Linear API settings for exact permissions

### Revocation

If tokens are compromised:

1. **Revoke immediately** in GitHub/Linear settings
2. **Generate new tokens**
3. **Update `.env`**
4. **Restart all agents**

---

## Troubleshooting

### "Authentication failed" errors

**Cause**: Invalid or expired tokens in `.env`

**Solution:**
1. Check `.env` file exists
2. Verify token format (GitHub: `ghp_...`, Linear: `lin_api_...`)
3. Regenerate tokens if expired
4. Restart agent sessions

### "Repository not found" or "Workspace not found"

**Cause**: Incorrect repository/workspace in `config.yaml`

**Solution:**
1. Verify `github.repo` format: `"owner/repo"`
2. Verify `linear.workspace` matches your Linear workspace name
3. Check team_id matches your Linear team prefix
4. Restart agent sessions

### Changes not taking effect

**Cause**: Agents cache configuration at startup

**Solution:**
1. Kill all agent sessions: `tmux kill-server`
2. Restart agents
3. Changes will now be picked up

---

## File Permissions

Recommended permissions:
```bash
chmod 600 .env              # Only owner can read/write
chmod 644 config.yaml       # Owner read/write, others read
chmod 644 README.md         # Owner read/write, others read
```

---

## Related Documentation

- **ARCHITECTURE.md** (parent directory) - Complete system architecture
- **orchestrator/README.md** - How to use the orchestrator
- **goal-builder/README.md** - Goal builder documentation
- Each agent's `prompts/developer.md` - Technical details on config usage

---

## Summary

**Shared resources** provide centralized configuration and credentials for all agents.

**Key Benefits:**
- Single source of truth
- Easy maintenance
- Consistent behavior
- Secure credential management

**Remember:**
- Update `config.yaml` to change system behavior
- Update `.env` to rotate credentials
- Restart agents after changes
- Keep `.env` secure and never commit it!

---

**Need help?** Check ARCHITECTURE.md or agent-specific documentation.
