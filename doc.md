# Mixer System Documentation

**A conversational AI workflow for transforming ideas into code through structured project management**

---

## Overview

The Mixer System is a universal build system that orchestrates the journey from raw thoughts to working code through a structured, conversational workflow. It integrates GitHub Issues (as an idea stash), Linear project management, and Claude AI agents to create an interactive development pipeline focused on **module-based development**.

### Module-Based Development

The system is designed around the concept of **modules as features**. Each module represents a discrete, self-contained feature or functionality of your application. The project maintains a `modules/` directory with subdirectories for different types of modules (e.g., `modules/auth/`, `modules/api/`, `modules/ui/`). The Module Builder agent can build one or multiple modules based on the plan specifications.

### Core Pipeline

```
GitHub Issues (Raw Thoughts/Ideas)
    ↓
Goal Tickets (WHAT feature/module to build) → Linear tickets with label="goal"
    ↓
Plan Tickets (HOW to build the module) → Linear tickets with label="plan"
    ↓
Code Modules (Feature implementation) → Actual working code in modules/
```

---

## System Architecture

### Three Specialized Agents

1. **Goal Builder** - Transforms GitHub issues into goal tickets
2. **Plan Builder** - Breaks down goals into implementation plans
3. **Module Builder** - Executes plans to produce working code

Each agent is a Claude AI assistant with:
- A specific personality and workflow defined in its system prompt
- Interactive slash commands for user engagement
- Python scripts that handle API integrations
- Conversational guidance through each stage

### Key Design Principles

1. **Conversational, Not Automated** - Agents collaborate with users to write meaningful content together, not generate templates
2. **Status-Driven Workflow** - Clear progression through draft→todo→doing→done states
3. **User Control Points** - Users manually approve transitions from draft to todo
4. **Interactive Refinement** - Content is crafted through conversation, not auto-generated
5. **Relationship Tracking** - Goals link to plans, maintaining project hierarchy

---

## Workflow States

### Status Progression

**Goal Tickets:**
```
draft → todo → doing → done
  ↓       ↓       ↓       ↓
Created  Ready   Plan    Module
by Goal  for     Being   Complete
Builder  Plan    Created
```

**Plan Tickets:**
```
draft → todo → doing → done
  ↓       ↓       ↓       ↓
Created  Ready   Being   Implementation
by Plan  for     Built   Complete
Builder  Module
```

### Critical Transitions

- **draft→todo**: Manual user approval (signals readiness)
- **todo→doing**: Automatic when next agent starts work
- **doing→done**: Automatic when work completes

---

## Agent Details

### Goal Builder

**Purpose:** Transform GitHub issues into Linear goal tickets defining WHAT to build

**Workflow:**
1. Lists open GitHub issues
2. Suggests logical groupings
3. **Collaboratively writes goal ticket with user**
4. Creates ticket with status="draft"
5. Closes related GitHub issues
6. Guides user to review and approve (draft→todo)

**Key Commands:**
- `/show-issues` - Display open GitHub issues
- `/suggest-groupings` - Analyze and group related issues
- `/create-goal` - Interactive goal creation

### Plan Builder

**Purpose:** Transform goal tickets into implementation plans defining HOW to build

**Workflow:**
1. Shows goals with status="todo"
2. User selects a goal
3. **Collaboratively writes plan with user**
4. Creates plan with status="draft"
5. Automatically updates goal from "todo" to "doing"
6. Links plan to parent goal

**Key Commands:**
- `/show-goals` - Display available goals
- `/analyze-goal` - Suggest implementation approach
- `/create-plan` - Interactive plan creation

### Module Builder

**Purpose:** Execute plan tickets to build feature modules

**Workflow:**
1. Shows plans with status="todo"
2. Automatically updates plan to "doing" when starting
3. Creates module structure in appropriate `modules/` subdirectory
4. Interactively implements each feature step
5. Builds one or multiple modules as specified in the plan
6. Runs tests and verifies completion
7. Updates both plan and goal to "done"

**Key Commands:**
- `/show-plans` - Display available plans
- `/load-plan` - Load plan details and target module(s)
- `/mark-complete` - Mark plan and goal as done

**Module Organization:**
The Module Builder creates organized feature modules such as:
- `modules/auth/` - Authentication features
- `modules/api/` - API endpoints and services
- `modules/ui/` - User interface components
- `modules/data/` - Data models and storage
- `modules/utils/` - Shared utilities

---

## Technical Implementation

### Directory Structure

```
mixer-system/
├── modules/
├── mixer.sh                      # Main entry point
├── config.yaml                   # GitHub/Linear configuration
├── .env                          # API credentials
├── agents/
│   ├── goal-builder/
│   │   ├── system-prompt.md      # Agent personality
│   │   └── run.sh                # Launch script
│   ├── plan-builder/
│   └── module-builder/
├── .claude/
│   ├── commands/                 # Slash commands
│   │   ├── goal-builder/
│   │   ├── plan-builder/
│   │   └── module-builder/
│   └── scripts/                  # Python backends
│       ├── goal-builder/
│       ├── plan-builder/
│       ├── module-builder/
│       └── shared/               # Reusable utilities
```

### Configuration

**config.yaml:**
```yaml
github:
  repo: "owner/repo"

linear:
  workspace: "Workspace"
  team_id: "TEAM"
  tickets:
    goal_label: "goal"
    plan_label: "plan"
```

**.env:**
```
GITHUB_TOKEN=ghp_...
LINEAR_API_KEY=lin_api_...
```

### Running Agents

```bash
# Start Goal Builder
./mixer.sh goal-builder

# Start Plan Builder
./mixer.sh plan-builder

# Start Module Builder
./mixer.sh module-builder
```

---

## Interactive Ticket Writing

### The Most Important Concept

Agents don't auto-generate tickets from templates. They **write actual content WITH users** through conversation:

1. Agent drafts meaningful ticket content
2. Shows draft to user for feedback
3. Refines based on user input
4. Continues until user approves
5. Saves EXACT content to Linear

**Example Goal Creation:**

```
Agent: "Let me draft a goal ticket for authentication:

# User Authentication Module

Build a complete authentication feature module providing secure login,
session management, and account recovery.

## Requirements
- User registration with email validation
- JWT-based authentication
- Password reset via email
- Rate limiting

## Target Module
`modules/auth/`

This will create a new authentication feature module with all necessary
components organized in the modules/auth/ directory.

How does this look?"

User: "Add OAuth support"

Agent: "Updated:

# User Authentication Module

Build a complete authentication feature module providing secure login,
OAuth integration, session management, and account recovery.

## Requirements
- User registration with email validation
- JWT-based authentication
- OAuth 2.0 (Google, GitHub)
- Password reset via email
- Rate limiting

## Target Module
`modules/auth/`

Perfect?"

User: "Yes"

Agent: "Created goal AUTH-123 with exactly this content"
```

---

## Complete Example Workflow

### Step 1: Create Goal

```bash
$ ./mixer.sh goal-builder

Agent: "I see 3 authentication-related issues. Should we group them?"
User: "Yes"
[Interactive ticket writing...]
Created: AUTH-123 (status=draft)
Closed: GitHub issues #12, #15, #18
```

### Step 2: Create Plan

*User changes AUTH-123 from draft→todo in Linear*

```bash
$ ./mixer.sh plan-builder

Agent: "Create plan for AUTH-123?"
User: "Yes"
[Interactive plan writing...]
Created: AUTH-125 (status=draft)
Updated: AUTH-123 (todo→doing)
```

### Step 3: Build Module

*User changes AUTH-125 from draft→todo in Linear*

```bash
$ ./mixer.sh module-builder

Agent: "Build AUTH-125?"
User: "Yes"
Updated: AUTH-125 (todo→doing)
[Interactive implementation...]
Updated: AUTH-125 (doing→done)
Updated: AUTH-123 (doing→done)
```

---

## Key Relationships

```
GitHub Issues → Goal Tickets
- Multiple issues grouped into one goal (feature)
- Issues closed when goal created

Goal → Plan Tickets
- One goal can have multiple plans
- Plan linked as child of goal
- Goal auto-updates to "doing" when plan created

Plan → Feature Modules
- Plan contains module implementation steps
- Each module represents a complete feature
- Modules organized in modules/ directory by type
- One plan can create one or multiple related modules
```

---

## Setup Instructions

1. **Copy system to project:**
   ```bash
   cp -r mixer-system /your/project/.mixer
   ```

2. **Configure integrations:**
   - Create `config.yaml` with GitHub repo and Linear workspace
   - Add credentials to `.env`

3. **Create Linear labels:**
   - "goal" label for goal tickets
   - "plan" label for plan tickets

4. **Configure Linear workflow states:**
   - Draft, Todo, In Progress (Doing), Done, Canceled

5. **Run agents:**
   ```bash
   ./.mixer/mixer.sh goal-builder
   ```

---

## Module Development Philosophy

The system is built specifically for **module-based feature development**, where:

- **Modules = Features**: Each module is a self-contained feature with its own directory, tests, and documentation
- **Organized Structure**: Modules are categorized by type (auth, api, ui, data, utils) in the `modules/` directory
- **Scalable Architecture**: New features are added as new modules, keeping the codebase organized
- **Clear Boundaries**: Each module has clear responsibilities and interfaces

## Philosophy

The Mixer System embodies several key philosophies:

- **Feature-Focused Development**: Build one complete feature at a time as a module
- **Human-AI Collaboration**: Not automation, but augmentation through conversation
- **Structured Creativity**: Freedom within a framework that ensures progress
- **Explicit Approval**: Users control when work advances to the next stage
- **Meaningful Content**: Tickets contain thoughtful prose, not generated templates
- **Transparency**: Clear status visibility and relationship tracking

The system transforms the chaotic process of turning ideas into code into a structured, conversational journey where AI agents guide but users decide, with each decision resulting in a well-organized feature module.