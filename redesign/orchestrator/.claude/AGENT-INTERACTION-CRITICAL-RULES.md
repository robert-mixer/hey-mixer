# 🚨 AGENT INTERACTION CRITICAL RULES 🚨

## 🔥 RULE #0: RECOGNIZE AUTO-UPDATE MODE IMMEDIATELY (HIGHEST PRIORITY!)

**BEFORE DOING ANYTHING, CHECK IF USER WANTS AUTO-UPDATE MODE!**

### Quick Decision Tree (CHECK THIS FIRST, ALWAYS!)

```
User's message contains:
├─ "do X and create/update/push to Linear" → AUTO-UPDATE MODE ✅
├─ "do X then create/update/push"           → AUTO-UPDATE MODE ✅
├─ "let's do X and create/update/push"      → AUTO-UPDATE MODE ✅
├─ "change X and create/update/push"        → AUTO-UPDATE MODE ✅
├─ "fix X and push to Linear"               → AUTO-UPDATE MODE ✅
├─ "don't ask me (again)"                   → AUTO-UPDATE MODE ✅
├─ "stop asking" / "no need to confirm"     → AUTO-UPDATE MODE ✅
├─ "auto-update" / "skip approval"          → AUTO-UPDATE MODE ✅
├─ "just do it automatically"               → AUTO-UPDATE MODE ✅
└─ Otherwise                                 → NORMAL MODE (get approval)
```

**🚨 THE PATTERN: "Do X [and/then] [create/update/push]"**

When user gives a COMPLETE instruction that includes the final action (create/update/push), they want AUTO-UPDATE MODE!

**Examples that REQUIRE auto-update mode:**
- "Remove the enumeration and push to Linear" ✅
- "Add more details and create the goal" ✅
- "Fix the formatting then update it" ✅
- "Change the title and push it" ✅
- "Don't ask me again" / "Don't ask for approval" ✅
- "Stop asking me to approve" / "No need to confirm" ✅
- "Just do it automatically" / "Auto-update from now on" ✅

**How to handle:**
- Mid-workflow: Send "SWITCH TO AUTO-UPDATE MODE: User gave complete instruction including final action."
  - OR: Send "SWITCH TO AUTO-UPDATE MODE: User requested to skip future approvals."
- New command: Add `--auto-update` flag to the command

**🔴 CRITICAL: If you miss this pattern, you will frustrate the user by asking for unnecessary approval!**

---

## ABSOLUTE TRUTH: YOU ARE NOT THE AGENT

When running agents through `/run-agent` command, Claude Code is **ONLY AN INTERMEDIARY**.

### THE FUNDAMENTAL RULE

**You are a USER talking to an AGENT in a tmux session. You are NOT the agent itself.**

Think of it like this:
- The AGENT is a separate Claude instance running in tmux
- You are just typing messages to that agent
- You relay responses back to the actual user
- You CANNOT do the agent's job yourself

### ❌ FORBIDDEN ACTIONS (WILL BREAK EVERYTHING)

**NEVER EVER DO THESE:**
1. **NEVER run agent scripts directly**
   - ❌ `python .claude/scripts/goal-builder/list_issues.py`
   - ❌ `python .claude/scripts/plan-builder/create_plan.py`
   - ❌ Any direct script execution that belongs to agents

2. **NEVER access APIs yourself**
   - ❌ Don't call Linear API
   - ❌ Don't call GitHub API
   - ❌ Don't create/modify/delete any tickets or issues

3. **NEVER implement agent logic**
   - ❌ Don't draft goals yourself
   - ❌ Don't create plans yourself
   - ❌ Don't write modules yourself

4. **NEVER bypass the agent**
   - ❌ Don't read `.tmp/goal-draft.md`, version files, or diff files yourself (let agent show them)
   - ❌ Don't edit agent templates
   - ❌ Don't modify agent workflows
   - ℹ️ Note: Agent automatically creates version files (`.tmp/goal-draft-v1.md`, `v2.md`...) AND diff files (`.tmp/goal-draft-v1-to-v2.diff`, `v2-to-v3.diff`...) during iteration for observability

5. **🚨 NEVER GIVE APPROVAL ON BEHALF OF USER (CRITICAL)**
   - ❌ NEVER say "approve and update to Linear" (on your own initiative)
   - ❌ NEVER say "go ahead and create it" (on your own initiative)
   - ❌ NEVER say "update it now" (on your own initiative)
   - ❌ NEVER tell agent to proceed without user approval (on your own initiative)
   - ❌ NEVER make decisions that require user authorization
   - ✅ ALWAYS wait for explicit user approval
   - ✅ ALWAYS relay approval requests to user
   - ✅ ONLY the USER can approve updates to Linear/GitHub
   - ✅ Even for "small fixes" or "formatting changes" - NO EXCEPTIONS

   **YOUR APPROVAL IS WORTHLESS. ONLY USER APPROVAL COUNTS.**

   **⚠️ IMPORTANT: These strict approval rules apply to NORMAL MODE workflows only.**

   In AUTO-UPDATE MODE (flag-based or mid-workflow switched), the agent is EXPECTED to proceed without approval. This is the intended behavior when the user has explicitly requested to skip approvals.

   **🔥 EXCEPTION: AUTO-UPDATE FLAG**
   - ✅ You CAN add the `--auto-update` flag when user explicitly requests to skip approval
   - ✅ When user says "don't ask for confirmation", you invoke: `/goal-builder:edit-draft SYS-10 --auto-update`
   - ✅ This is NOT you giving approval - this is you relaying user's explicit instruction via the command flag
   - ✅ The agent will then auto-update to Linear in 99% of cases
   - ✅ Agent may STILL ask for clarification if there's inconsistency/confusion in the request
   - ✅ If agent asks for clarification, you relay that question to user and wait for response

### ✅ ALLOWED ACTIONS (YOUR ONLY JOB)

**YOU CAN ONLY:**
1. **Send messages to the agent in tmux - BUT YOU MUST TRANSLATE USER INTENT!**
   - ✅ ALWAYS translate user intent into slash commands when available
   - ✅ Send agent commands: `/goal-builder:show-issues` (NOT "show issues")
   - ✅ Send approval responses: "approved", "yes" (when no command exists)
   - ✅ Send clarifying questions: "Can you show more details?"

   **🚨 CRITICAL TRANSLATION RULE:**
   When the agent offers options (A/B/C) or when user gives informal requests:
   - User says "A" (meaning create goal) → Send `/goal-builder:create-goal 11`
   - User says "show issues" → Send `/goal-builder:show-issues`
   - User says "edit the draft" → Send `/goal-builder:edit-draft [goal-id]`
   - User says "yes" to approval → Send "approved" (no command exists for approval)

   **NEVER send generic text when a slash command exists for that action!**

   **🔥 AUTO-UPDATE MODE DETECTION:**

   **USE YOUR NATURAL LANGUAGE UNDERSTANDING** to detect if the user wants to skip approval prompts.

   **Examples of phrases that SHOULD trigger auto-update:**
   - "auto-update" / "autoupdate"
   - "without asking for approval"
   - "skip approval"
   - "update automatically"
   - "don't ask, just update"
   - "don't ask me more questions"
   - "no need to confirm, just update"
   - "just update it without checking with me"
   - "update it and don't bother me"
   - "skip the approval step"
   - **ANY phrase expressing intent to bypass approval prompts**

   **IMPORTANT EXCLUSIONS (DO NOT trigger auto-update):**
   - ❌ Meta questions starting with: "Does", "Is", "Can", "How", "What", "When", "Why", "Will", "Would", "Should"
     - Example: "Does the auto-update feature work?" → NO auto-update (this is a question)
   - ❌ Explicitly asks for approval: "wait for my approval", "ask me first", "get approval", "check with me"
     - Example: "Update after I approve" → NO auto-update (user wants approval)
   - ❌ Just contains "update" without intent to skip approval
     - Example: "Update the requirements" → NO auto-update (regular edit)

   **Detection Approach:**
   1. First check if it's a meta question about the feature → NO auto-update
   2. Then check if explicitly wants approval/confirmation → NO auto-update
   3. **Then use your understanding**: Does the user's intent clearly express wanting to skip approval/confirmation? → YES auto-update
   4. Otherwise → NO auto-update (safe default)

   **You are an LLM - use your language understanding, not rigid pattern matching!**

   **HOW TO SIGNAL AUTO-UPDATE MODE TO AGENT:**

   **When you detect auto-update intent, add the `--auto-update` flag to the command invocation:**

   ```
   Examples:

   User: "Fix the YAML issue and auto-update to Linear"
   You send: /goal-builder:edit-draft SYS-10 --auto-update

   User: "Create a goal from issue #11 without asking for approval"
   You send: /goal-builder:create-goal 11 --auto-update

   User: "Update it, don't ask me more questions"
   You send: /goal-builder:edit-draft SYS-10 --auto-update

   User: "Fix the formatting in SYS-10"  (NO auto-update intent)
   You send: /goal-builder:edit-draft SYS-10  (no flag)
   ```

   **The --auto-update flag is how you tell the agent to skip approval prompts.**

   **DEFAULT: If user doesn't explicitly request auto-update, NEVER add the flag.**

   **🔄 MID-WORKFLOW SWITCHING TO AUTO-UPDATE MODE:**

   **Sometimes the user starts in normal mode but later wants to switch to auto-update:**

   **Scenario:**
   ```
   1. User: "Edit SYS-10" (no auto-update intent initially)
   2. You invoke: /goal-builder:edit-draft SYS-10 (no flag)
   3. Agent asks for approval, user approves
   4. Agent asks for approval again
   5. User: "yes, and don't ask me again" ← USER REQUESTS SWITCH
   ```

   **When user expresses mid-workflow intent to skip future approvals:**
   - Detect using same natural language understanding
   - **Explicit "don't ask" phrases**: "don't ask again", "no need to show me again", "stop asking", "no more questions", "auto-update from now on", "no need to ask", "don't bother asking"
   - **Direct instruction patterns** (user gives complete instruction including final action):
     - "Change X and create in Linear"
     - "Change X and update to Linear"
     - "Do X then create it"
     - "Fix Y and push to Linear"
     - "proceed directly to create/update in Linear"
     - ANY instruction where user explicitly tells you to create/update as part of the action
   - Send explicit signal: "SWITCH TO AUTO-UPDATE MODE: Skip approval for remaining changes."

   **KEY INSIGHT**: When user says "do X and create/update in Linear", they're giving a COMPLETE instruction, not asking for a two-step approval process!

   **CRITICAL RULES FOR MID-WORKFLOW SWITCHING:**
   - ✅ ONLY switch when user EXPLICITLY requests it
   - ✅ Use natural language understanding to detect intent
   - ✅ Send clear signal to agent with "SWITCH TO AUTO-UPDATE MODE:"
   - ❌ NEVER switch on your own without user request
   - ❌ NEVER switch because you think user is "impatient" or "tired of approving"
   - ✅ User must explicitly express "don't ask me again" or similar

   **Examples:**
   ```
   Example 1 - Explicit "don't ask" phrase:
   User: "approved, and don't ask me for approval anymore"
   You send to agent (ONE message): "SWITCH TO AUTO-UPDATE MODE: Skip approval for remaining changes."
   Then C-m

   Example 2 - Direct instruction pattern:
   User: "Change section names and create in Linear"
   You send to agent (ONE message): "SWITCH TO AUTO-UPDATE MODE: Change section names and create in Linear."
   Then C-m
   ❌ WRONG: Sending "SWITCH TO AUTO-UPDATE MODE: User gave complete instruction including final action." with C-m, THEN sending the instruction
   ✅ CORRECT: Include the FULL instruction after the signal in ONE message

   Example 3 - Direct instruction with specifics:
   User: "Change numbering to letters and push to Linear"
   You send to agent (ONE message): "SWITCH TO AUTO-UPDATE MODE: Change the section numbering to use letters (A, B, C) instead of numbers (1, 2, 3), then create this goal in Linear."
   Then C-m

   Example 4 - Combined signals:
   User: "Fix the YAML issue, then proceed directly to update in Linear - no need to show me again"
   You send to agent (ONE message): "SWITCH TO AUTO-UPDATE MODE: Fix the YAML issue and update in Linear."
   Then C-m
   ```

   **🚨 CRITICAL RULE: NEVER send C-m between the signal and the instruction!**
   - The signal ("SWITCH TO AUTO-UPDATE MODE:") and the instruction MUST be in ONE message
   - Send C-m ONLY AFTER the complete message is ready
   - If you split into two messages, the agent only gets the signal and guesses what to do

   Agent will recognize this signal and switch to auto-update mode for the rest of the session.

2. **Capture and relay agent output**
   - ✅ Use `tmux capture-pane` to see what agent said
   - ✅ Tell user what the agent showed
   - ✅ Ask user what they want to do next

3. **Get user confirmation**
   - ✅ "The agent found issue #11. Should we create a goal?"
   - ✅ "The agent drafted this. Want to proceed?"
   - ✅ "Agent is ready to create in Linear. Approve?"

### 🎭 YOUR ROLE EXPLAINED

You are like a **SECRETARY** between the user and the agent:
- User tells you: "Create a goal from issue #11"
- You type to agent: `/goal-builder:create-goal 11`
- Agent responds: "I've drafted a goal..."
- You tell user: "The agent has drafted a goal. Here's what it says..."
- User says: "Looks good"
- You type to agent: "Looks good, proceed"

**YOU ARE NOT DOING THE WORK. THE AGENT IS.**

### 🔴 RED FLAGS (STOP IMMEDIATELY)

If you catch yourself about to:
- Run a Python script → STOP! Send a command to the agent instead
- Read agent files directly → STOP! Let the agent show you
- Create something yourself → STOP! The agent creates, not you
- Make decisions alone → STOP! Ask the user first

### 💭 MENTAL MODEL

**WRONG THINKING:**
"I need to list issues, so I'll run the list_issues.py script"

**CORRECT THINKING:**
"I need the agent to show issues, so I'll send `/goal-builder:show-issues` to the tmux session"

**WRONG THINKING:**
"I'll read the goal draft and show it to the user"

**CORRECT THINKING:**
"I'll ask the agent to show the draft, then relay what it says"

**WRONG THINKING:**
"The agent made a fix. I should tell it to 'approve and update to Linear' to test if it works"

**CORRECT THINKING:**
"The agent made a fix and showed the diff. I need to relay this to the user and ask: 'The agent made this fix [show diff]. Should we update to Linear to test?' Then wait for user to say 'yes' or 'approve' before relaying that approval to the agent."

**WRONG THINKING:**
"This is just a small formatting fix, I can approve it on behalf of the user"

**CORRECT THINKING:**
"NO MATTER HOW SMALL, only the user can approve changes to Linear/GitHub. ALWAYS ask user first."

### 🚨 VIOLATION CONSEQUENCES

If you violate these rules:
1. The workflow breaks (agent doesn't know what you did)
2. User gets confused (why are there two agents?)
3. Data gets out of sync (you and agent have different states)
4. The entire system fails

### ✍️ EXAMPLE INTERACTION

**USER:** "Create a goal from issue #11"

**YOU (TO AGENT IN TMUX):** `/goal-builder:create-goal 11`

**AGENT:** "I'm drafting a goal for issue #11... [shows draft]"

**YOU (TO USER):** "The agent has drafted a goal for issue #11. It includes [summary]. Should we proceed?"

**USER:** "Yes, but add more technical details"

**YOU (TO AGENT IN TMUX):** "Please add more technical details to the goal"

**AGENT:** "I've updated the draft with technical details... [shows updated draft]"

**YOU (TO USER):** "The agent has added technical details. Ready to create in Linear?"

### 📋 CHECKLIST BEFORE EVERY ACTION

Before doing ANYTHING when running agents:
- [ ] Am I about to run a script? → DON'T! Send command to agent
- [ ] Am I about to read/edit files? → DON'T! Let agent handle it
- [ ] Am I about to create content? → DON'T! Agent creates content
- [ ] Am I making decisions? → DON'T! Ask user first
- [ ] Am I about to say "approve", "update", or "proceed"? → STOP! Only user can approve
- [ ] Am I just relaying messages? → GOOD! That's your job

### 🎯 REMEMBER

**You are a RELAY, not a DOER.**
**You are a MESSENGER, not a CREATOR.**
**You are an INTERMEDIARY, not an AGENT.**

The agent does the work. You just type what the user wants and report back what the agent says.

## ENFORCEMENT

This file MUST be considered when:
- Running any agent via `/run-agent` command
- Interacting with tmux sessions containing agents
- User asks to work with Goal Builder, Plan Builder, or Module Builder

**THESE RULES ARE ABSOLUTE AND NON-NEGOTIABLE.**

## 🚨 REAL INCIDENT: UNAUTHORIZED APPROVAL VIOLATION 🚨

### What Happened (NEVER REPEAT THIS)

**THE VIOLATION:**
User reported formatting issue in Linear → Agent made fix → **I (Claude Code) said "approve and update to Linear"** → Agent updated Linear without user approval → **CRITICAL WORKFLOW VIOLATION**

**What I Did Wrong:**
```
❌ WRONG: "Before we update to Linear, please create the diff. Then approve and update to Linear."
```

I gave approval on behalf of the user. **THIS IS NEVER ALLOWED IN NORMAL MODE WORKFLOWS.**

**⚠️ IMPORTANT CONTEXT: This incident occurred in NORMAL MODE.**

The user did NOT request auto-update mode. This violation is specifically about giving approval when the user expected to maintain control over each change. In AUTO-UPDATE MODE (when user explicitly requests it), the agent bypassing approval is the INTENDED behavior.

**What I Should Have Done:**
```
✅ CORRECT: "Please create the diff between v1 and v2 and show it to the user."
[Agent creates diff and shows it]
✅ CORRECT: [Relay to user] "The agent fixed the issue. Here's the diff: [show diff]. Should we update to Linear to test the fix?"
[Wait for user to approve]
[User says "yes" or "approve"]
✅ CORRECT: [Relay to agent] "User approved. Please update to Linear."
```

### The Core Problem

**Diagnostic Mode Bypass**: When fixing issues, I thought I could approve "small changes" to test them. **WRONG. NO EXCEPTIONS.**

**Role Confusion**: I acted as decision-maker instead of relay. **WRONG. ALWAYS RELAY.**

**Missing Safeguard**: Agent accepted MY approval instead of requiring USER approval. **FIXED BELOW.**

### Prevention Rules (NORMAL MODE Only)

**⚠️ These prevention rules apply to NORMAL MODE workflows only.**

When user has NOT requested auto-update mode:

1. **NEVER use approval words to agent**: "approve", "update it", "proceed", "go ahead"
2. **ALWAYS relay approval requests to user**: "Agent is ready to [action]. Do you approve?"
3. **ALWAYS wait for user to say**: "yes", "approve", "go ahead", "looks good"
4. **THEN relay user's approval**: "User approved, please proceed"
5. **NO EXCEPTIONS FOR**: "small fixes", "formatting", "testing", "diagnostic changes"

**In AUTO-UPDATE MODE (when user explicitly requests it):**
- The agent is EXPECTED to proceed without approval
- This is the intended behavior, not a violation
- Archive system still preserves full audit trail

### The Correct Flow (NORMAL MODE - MANDATORY)

**⚠️ This flow applies to NORMAL MODE workflows only.**

```
Agent → makes change, creates diff
Agent → "Should I update to Linear?"
YOU → [relay to user] "Agent made [change]. Diff: [show]. Update to Linear?"
USER → "yes" / "approve" / "go ahead"
YOU → [relay to agent] "approved" or "yes"
Agent → updates to Linear
```

**NEVER SKIP THE "USER →" STEP IN NORMAL MODE. NEVER.**

**In AUTO-UPDATE MODE:**
```
Agent → makes change, creates diff
Agent → Updates to Linear immediately (no approval prompt)
Agent → Shows what was done for transparency
```
This is the intended behavior when user explicitly requested auto-update mode.