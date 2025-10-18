#!/bin/bash
set -e

SYSTEM_PROMPT_FILE="${AGENT_DIR}/system-prompt.md"
SYSTEM_PROMPT=$(cat "$SYSTEM_PROMPT_FILE")

claude \
  --append-system-prompt "$SYSTEM_PROMPT" \
  --add-dir "${MIXER_ROOT}/.claude/commands/plan-builder" \
  --add-dir "${MIXER_ROOT}/.claude/scripts/plan-builder" \
  "=Ë Plan Builder started.

Available commands:
- /show-goals
- /analyze-goal
- /create-plan

What would you like to do?"
