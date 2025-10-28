#!/bin/bash
# Goal Builder Agent Runner
# This script runs the goal-builder agent in its isolated workspace
# Note: This script must run from the agent's workspace directory

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_WORKSPACE="$(cd "$SCRIPT_DIR/../.." && pwd)"
SYSTEM_PROMPT_FILE="$SCRIPT_DIR/system-prompt.md"

# Check if system prompt exists
if [ ! -f "$SYSTEM_PROMPT_FILE" ]; then
    echo "❌ Error: System prompt not found: $SYSTEM_PROMPT_FILE"
    exit 1
fi

# CRITICAL: Change to agent workspace
cd "$AGENT_WORKSPACE"

# Display agent info
echo "═══════════════════════════════════════════════════════════════"
echo "🎯 GOAL BUILDER AGENT (Isolated Workspace)"
echo "═══════════════════════════════════════════════════════════════"
echo "Transform GitHub issues into structured Linear goal tickets"
echo "Workspace: $AGENT_WORKSPACE"
echo "───────────────────────────────────────────────────────────────"
echo ""

# Load system prompt
SYSTEM_PROMPT=$(cat "$SYSTEM_PROMPT_FILE")

# Define allowed tools for the goal builder agent
# Based on CLI documentation, we can specify exact tools and even specific commands
ALLOWED_TOOLS=(
    "SlashCommand"
    "Read"
    "Write"
    "Edit"
    "Bash(python:.claude/scripts/goal-builder/*)"
    "Bash(git status)"
    "Bash(git diff)"
    "Glob"
    "Grep"
)

# Build the allowed tools arguments
TOOL_ARGS=""
for tool in "${ALLOWED_TOOLS[@]}"; do
    TOOL_ARGS="$TOOL_ARGS --allowedTools \"$tool\""
done

# Run Claude with optimized settings for the goal builder agent
# Using eval to properly handle the tool arguments with spaces
eval claude \
    --append-system-prompt \"\$SYSTEM_PROMPT\" \
    --model opus \
    --dangerously-skip-permissions \
    $TOOL_ARGS \
    --add-dir \".claude\" \
    --add-dir \"agents\"
