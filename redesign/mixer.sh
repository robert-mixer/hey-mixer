#!/bin/bash
# Mixer System V3 - Isolated Workspaces Launcher
# Usage: ./mixer.sh <agent-name>
# Example: ./mixer.sh goal-builder

set -e

# Get the directory where this script is located
MIXER_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Agent name from first argument
AGENT_NAME="${1}"

if [ -z "$AGENT_NAME" ]; then
    echo "═══════════════════════════════════════════════════════════════"
    echo "🎯 MIXER SYSTEM V3 - ISOLATED WORKSPACES"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "Usage: ./mixer.sh <agent-name>"
    echo ""
    echo "Available agents:"
    echo "  orchestrator   - Main coordinator agent (talks to all sub-agents)"
    echo "  goal-builder   - Process GitHub issues → Linear goals"
    echo "  plan-builder   - Transform goals → implementation plans"
    echo "  module-builder - Transform plans → working code"
    echo ""
    echo "Example:"
    echo "  ./mixer.sh orchestrator  # Start main orchestrator"
    echo "  ./mixer.sh goal-builder   # Start goal-builder directly"
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    exit 1
fi

# Check if agent workspace exists
AGENT_WORKSPACE="${MIXER_ROOT}/${AGENT_NAME}"
if [ ! -d "$AGENT_WORKSPACE" ]; then
    echo "❌ Error: Agent workspace '${AGENT_NAME}' not found"
    echo "   Expected: ${AGENT_WORKSPACE}"
    echo ""
    echo "Available agents:"
    ls -d ${MIXER_ROOT}/*/ 2>/dev/null | xargs -n1 basename | grep -v "^\." | sort
    exit 1
fi

# Check if run.sh exists
RUN_SCRIPT="${AGENT_WORKSPACE}/agents/${AGENT_NAME}/run.sh"
if [ ! -f "$RUN_SCRIPT" ]; then
    echo "❌ Error: ${RUN_SCRIPT} not found"
    exit 1
fi

# Make sure run.sh is executable
chmod +x "$RUN_SCRIPT"

# Display startup info
echo "═══════════════════════════════════════════════════════════════"
echo "🚀 LAUNCHING ${AGENT_NAME^^} AGENT"
echo "═══════════════════════════════════════════════════════════════"
echo "Workspace: ${AGENT_WORKSPACE}"
echo "Script: ${RUN_SCRIPT}"
echo "───────────────────────────────────────────────────────────────"
echo ""

# Execute the agent's run script
# The run script will change to its workspace directory
exec "${RUN_SCRIPT}"