#!/bin/bash

# Orchestrator Agent Launcher
# Coordinates interactions between user and builder agents

set -euo pipefail

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored message
print_msg() {
  local color=$1
  shift
  echo -e "${color}$@${NC}"
}

# Check prerequisites
check_prerequisites() {
  # Check if Claude CLI is available
  if ! command -v claude &> /dev/null; then
    print_msg "$RED" "❌ Error: Claude CLI not found"
    print_msg "$YELLOW" "Install from: https://github.com/anthropics/claude-cli"
    exit 1
  fi

  # Check if tmux is available
  if ! command -v tmux &> /dev/null; then
    print_msg "$RED" "❌ Error: tmux not found"
    print_msg "$YELLOW" "Install: brew install tmux (macOS) or apt-get install tmux (Linux)"
    exit 1
  fi

  # Check if builder agents exist
  if [ ! -d "../goal-builder" ]; then
    print_msg "$RED" "❌ Error: ../goal-builder directory not found"
    exit 1
  fi
}

# Display startup banner
show_banner() {
  print_msg "$BLUE" "╔════════════════════════════════════════╗"
  print_msg "$BLUE" "║      Orchestrator Agent v3.0           ║"
  print_msg "$BLUE" "║   Multi-Agent Workflow Coordinator     ║"
  print_msg "$BLUE" "╚════════════════════════════════════════╝"
  echo ""
  print_msg "$GREEN" "🎭 Coordinate interactions with specialized builder agents"
  print_msg "$GREEN" "🔧 Launch goal-builder, plan-builder, module-builder via tmux"
  echo ""
}

# Display workflow
show_workflow() {
  print_msg "$YELLOW" "📋 Mixer System Workflow:"
  echo ""
  echo "  GitHub Issues  →  Linear Goals  →  Linear Plans  →  Code Modules"
  echo "                     ↑                  ↑                 ↑"
  echo "                 goal-builder      plan-builder     module-builder"
  echo ""
  print_msg "$BLUE" "You coordinate these agents through tmux sessions."
  echo ""
}

# Main execution
main() {
  show_banner

  print_msg "$YELLOW" "🔍 Checking prerequisites..."
  check_prerequisites
  print_msg "$GREEN" "✅ Prerequisites OK"
  echo ""

  show_workflow

  print_msg "$BLUE" "🚀 Starting Orchestrator..."
  echo ""

  print_msg "$YELLOW" "💡 Tips:"
  echo "  - You relay messages between user and builder agents"
  echo "  - Use tmux to launch and interact with agents"
  echo "  - Always translate user intent into agent slash commands"
  echo "  - Detect auto-update patterns in user messages"
  echo ""

  # Launch Claude CLI with this directory as working directory
  # The CLAUDE.md file will be auto-loaded
  claude
}

# Trap errors
trap 'print_msg "$RED" "❌ Error occurred. Exiting..."; exit 1' ERR

# Run main function
main
