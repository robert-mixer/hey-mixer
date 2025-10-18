#!/bin/bash
# Goal Builder Agent Runner
# This script runs the goal-builder agent using the claude CLI

set -e

# Read the system prompt
SYSTEM_PROMPT_FILE="agents/goal-builder/system-prompt.md"
if [ ! -f "$SYSTEM_PROMPT_FILE" ]; then
    echo "Error: System prompt not found: $SYSTEM_PROMPT_FILE"
    exit 1
fi

cat "$SYSTEM_PROMPT_FILE"

SYSTEM_PROMPT=$(cat "$SYSTEM_PROMPT_FILE")

# Run Claude with the system prompt and agent-specific tools
claude --append-system-prompt "$SYSTEM_PROMPT"
