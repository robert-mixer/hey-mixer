#!/bin/bash
# Mixer System V2 - Main Entry Point
# Usage: ./mixer.sh <agent-name>
# Example: ./mixer.sh goal-builder

set -e

# Get the directory where this script is located
MIXER_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Agent name from first argument
AGENT_NAME="${1}"

if [ -z "$AGENT_NAME" ]; then
    echo "Usage: ./mixer.sh <agent-name>"
    echo ""
    echo "Available agents:"
    echo "  goal-builder   - Process GitHub issues and create Linear goals"
    echo "  plan-builder   - Break down goals into actionable plans"
    echo "  module-builder - Implement plans as code modules"
    exit 1
fi

# Check if agent exists
AGENT_DIR="${MIXER_ROOT}/agents/${AGENT_NAME}"
if [ ! -d "$AGENT_DIR" ]; then
    echo "Error: Agent '${AGENT_NAME}' not found"
    echo "Expected directory: ${AGENT_DIR}"
    exit 1
fi

# Check if run.sh exists
RUN_SCRIPT="${AGENT_DIR}/run.sh"
if [ ! -f "$RUN_SCRIPT" ]; then
    echo "Error: ${RUN_SCRIPT} not found"
    exit 1
fi

# Make sure run.sh is executable
chmod +x "$RUN_SCRIPT"

# Export variables that agents might need
export MIXER_ROOT
export AGENT_NAME
export AGENT_DIR

# Run the agent
echo "=€ Starting ${AGENT_NAME}..."
echo "   Root: ${MIXER_ROOT}"
echo "   Agent: ${AGENT_DIR}"
echo ""

cd "$MIXER_ROOT"
exec "${RUN_SCRIPT}"
