# Goal Builder Agent - Skill Awareness Update

## 🎯 Problem Solved
The agent wasn't aware of its skill files in `.claude/skills/goal-builder/` because they weren't explicitly mentioned in the system prompt.

## ✅ Changes Made to `agents/goal-builder/system-prompt.md`

### 1. Added Dedicated Skill Section
Created a comprehensive "Your Goal-Builder Skill" section that:
- Lists all skill files (SKILL.md, TEMPLATES.md, WORKFLOW.md)
- Explains what each file contains
- **Shows HOW to access them using the Read tool**

### 2. Added Explicit Read Instructions
```
When you need templates or workflow guidance, use the Read tool:
- Read(".claude/skills/goal-builder/SKILL.md") - For main workflow
- Read(".claude/skills/goal-builder/TEMPLATES.md") - For goal templates
- Read(".claude/skills/goal-builder/WORKFLOW.md") - For detailed procedures
```

### 3. Updated Startup Message
Added "Resources I use:" section mentioning:
- Goal templates for different scenarios
- Detailed workflow documentation
- Best practices for ticket writing

### 4. Enhanced Interactive Ticket Writing Section
Added "Using Templates" subsection that explains:
- How to identify which template fits best
- Using templates as foundations (not copying)
- Always customizing based on actual issues

### 5. Added Example in Interaction Section
Shows the agent actually using the Read tool to access templates:
```
User: "Can you show me what templates you have?"
You: "Let me check my templates for you."
[Use Read tool with ".claude/skills/goal-builder/TEMPLATES.md"]
```

### 6. Added Important Note
**"When the user asks about templates or you need guidance, actively READ these files using the Read tool. Don't just mention they exist - actually use them!"**

## 🚀 Result
The Goal Builder agent now:
- ✅ Knows it has skill files
- ✅ Knows WHERE they are (`.claude/skills/goal-builder/`)
- ✅ Knows HOW to access them (Read tool)
- ✅ Knows WHEN to use them (templates, workflow guidance)
- ✅ Will proactively read them when needed

## 📋 Testing
When you run the agent, try asking:
- "What templates do you have?"
- "Show me the workflow for creating a goal"
- "Can you use a template for this feature?"

The agent should now use the Read tool to access its skill files and provide the actual content!