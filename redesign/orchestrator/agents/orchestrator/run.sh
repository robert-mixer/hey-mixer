#!/bin/bash
# Orchestrator Agent Launcher
# This launches the main orchestrator that coordinates all sub-agents

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ORCHESTRATOR_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "🎯 Starting Orchestrator Agent"
echo "   Workspace: $ORCHESTRATOR_ROOT"
echo ""

# Change to orchestrator workspace
cd "$ORCHESTRATOR_ROOT"

# Launch Claude CLI with orchestrator system prompt
if command -v claude &> /dev/null; then
    echo "📚 Loading orchestrator system prompt..."
    echo "🚀 Launching orchestrator..."
    echo ""

    # Run claude with the system prompt
    claude --system-prompt "$SCRIPT_DIR/system-prompt.md"
else
    echo "❌ Error: Claude CLI not found"
    echo "Please install Claude CLI first"
    exit 1
fi