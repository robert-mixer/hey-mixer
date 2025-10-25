#!/usr/bin/env bash
# SessionStart hook - Automatically load ALL critical instruction files
# This ensures Claude Code always has the latest rules and instructions

COMBINED_CONTENT=""

# Function to add file content with header
add_file_content() {
  local file_path="$1"
  local file_name=$(basename "$file_path")

  if [ -f "$file_path" ]; then
    COMBINED_CONTENT+="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    COMBINED_CONTENT+="📄 FILE: $file_name\n"
    COMBINED_CONTENT+="📍 PATH: $file_path\n"
    COMBINED_CONTENT+="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    COMBINED_CONTENT+="$(cat "$file_path")\n\n"
  else
    echo "Warning: File not found: $file_path" >&2
  fi
}

# Load all critical instruction files
echo "Loading critical instruction files..." >&2

# Get the project root directory (where .claude lives)
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

# 1. Main project instructions
add_file_content "${PROJECT_ROOT}/CLAUDE.md"

# 2. Critical agent interaction rules
add_file_content "${PROJECT_ROOT}/.claude/AGENT-INTERACTION-CRITICAL-RULES.md"

# 3. Run-agent command (complete interaction guide)
add_file_content "${PROJECT_ROOT}/.claude/commands/run-agent.md"

# 4. Goal-builder context
add_file_content "${PROJECT_ROOT}/.claude/goal-builder-context.md"

# Create the message header
MESSAGE_HEADER="🔴 CRITICAL INSTRUCTIONS LOADED AT SESSION START 🔴

The following instruction files have been automatically loaded and MUST be followed:

✅ CLAUDE.md - Main project instructions
✅ AGENT-INTERACTION-CRITICAL-RULES.md - Agent interaction rules (CHECK FOR AUTO-UPDATE PATTERNS!)
✅ run-agent.md - Complete agent interaction guide
✅ goal-builder-context.md - Goal builder context

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"

MESSAGE_FOOTER="

🚨 REMEMBER: Check for auto-update patterns (\"do X and push/create/update\") BEFORE every agent interaction!"

# Combine and properly escape for JSON using jq
FULL_MESSAGE="${MESSAGE_HEADER}${COMBINED_CONTENT}${MESSAGE_FOOTER}"

# Output JSON with properly escaped content
jq -n --arg msg "$FULL_MESSAGE" '{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": $msg
  }
}'
