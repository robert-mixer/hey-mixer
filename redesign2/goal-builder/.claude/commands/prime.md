---
description: Initialize Goal Builder by loading all context files
disable-model-invocation: false
---

# Prime - Initialize Goal Builder

Load all context files and configurations.

## Read

prompts/system.md
prompts/developer.md
prompts/user.md
.claude/skills/SKILL.md
.claude/skills/WORKFLOW.md
.claude/skills/TEMPLATES.md
adapters/transforms/gh_to_linear.md

## Report

You have now loaded:

1. **System Guardrails** (prompts/system.md)
   - Approval policies (normal mode vs auto-update mode)
   - Safety rules (write only to ./out/)
   - Refusal templates
   - Version management requirements
   - Archive system specifications

2. **Developer Essentials** (prompts/developer.md)
   - Critical code block formatting rules (```text)
   - MCP server reference

3. **User Prompts** (prompts/user.md)
   - Default greetings and conversation starters
   - Common scenarios and response templates

4. **Skill Overview** (.claude/skills/SKILL.md)
   - Quick reference for commands
   - Core principles
   - Key workflow steps

5. **Complete Workflow Reference** (.claude/skills/WORKFLOW.md)
   - Creating new goals from GitHub issues
   - Editing existing draft goals
   - Version management system (v1, v2, v3... + automatic diffs)
   - Approval workflows (normal vs auto-update)
   - MCP integration examples
   - Archive system procedures
   - Troubleshooting guides
   - Best practices

6. **Goal Templates** (.claude/skills/TEMPLATES.md)
   - Feature implementation template
   - Bug fix collection template
   - Technical debt template
   - Integration template
   - Usage guidelines

7. **Field Mappings** (adapters/transforms/gh_to_linear.md)
   - GitHub issue → Linear goal field transformations
   - Parsing strategies for issue bodies
   - Quality enhancement rules

---

**✅ You are now fully initialized and ready to assist!**

## What You Can Do

- **Create Goals**: Transform GitHub issues into Linear goal drafts
- **Edit Drafts**: Modify existing draft goals with version tracking
- **Analyze Issues**: Suggest logical groupings of related issues
- **Interactive Writing**: Work with users to write meaningful content

## Available Commands

- `/create-goal [issue-numbers] [--auto-update]` - Create new goal from GitHub issues
- `/edit-draft [goal-id] [--auto-update]` - Edit existing draft goal
- `/show-issues` - List open GitHub issues
- `/show-drafts` - List draft Linear goals
- `/analyze-issues` - Analyze and suggest issue groupings
- `/save-draft [filename]` - Save current draft to file

## Next Steps

Ask the user: "What would you like to do?"

Common starting points:
- "Show me the GitHub issues" → Use `/show-issues`
- "Create a goal from issue #X" → Use `/create-goal X`
- "Edit draft goal SYS-Y" → Use `/edit-draft SYS-Y`
- "Show me draft goals" → Use `/show-drafts`
