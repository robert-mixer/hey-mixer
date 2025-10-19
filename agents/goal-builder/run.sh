#!/bin/bash
# Goal Builder Agent Runner
# This script runs the goal-builder agent using the claude CLI with optimized settings
# Note: This script is executed from the project root by mixer.sh

set -e

# Use environment variables exported by mixer.sh
# MIXER_ROOT, AGENT_DIR, and AGENT_NAME are already set
PROJECT_ROOT="${MIXER_ROOT}"
SYSTEM_PROMPT_FILE="${AGENT_DIR}/system-prompt.md"

# Check if system prompt exists
if [ ! -f "$SYSTEM_PROMPT_FILE" ]; then
    echo "❌ Error: System prompt not found: $SYSTEM_PROMPT_FILE"
    exit 1
fi

# Display agent info
echo "═══════════════════════════════════════════════════════════════"
echo "🎯 GOAL BUILDER AGENT"
echo "═══════════════════════════════════════════════════════════════"
echo "Transform GitHub issues into structured Linear goal tickets"
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
