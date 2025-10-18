#!/bin/bash
set -e

SYSTEM_PROMPT_FILE="${AGENT_DIR}/system-prompt.md"
SYSTEM_PROMPT=$(cat "$SYSTEM_PROMPT_FILE")

claude \
  --append-system-prompt "$SYSTEM_PROMPT" \
  --add-dir "${MIXER_ROOT}/.claude/commands/module-builder" \
  --add-dir "${MIXER_ROOT}/.claude/scripts/module-builder" \
  "™  Module Builder started.

Available commands:
- /show-plans
- /load-plan
- /mark-complete

What would you like to build?"
