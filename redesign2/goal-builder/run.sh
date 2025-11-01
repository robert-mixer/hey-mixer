#!/bin/bash

# Goal Builder Agent Launcher
# Starts Claude Code with Goal Builder context

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

  # Check if .env file exists in shared
  if [ ! -f "../shared/.env" ]; then
    print_msg "$RED" "❌ Error: ../shared/.env not found"
    print_msg "$YELLOW" "Create .env with GITHUB_TOKEN and LINEAR_API_KEY"
    exit 1
  fi

  # Check if config.yaml exists
  if [ ! -f "../shared/config.yaml" ]; then
    print_msg "$RED" "❌ Error: ../shared/config.yaml not found"
    print_msg "$YELLOW" "Create config.yaml with github.repo and linear settings"
    exit 1
  fi

  # Source environment variables
  set -a
  source "../shared/.env"
  set +a

  # Validate required env vars
  if [ -z "${GITHUB_TOKEN:-}" ]; then
    print_msg "$RED" "❌ Error: GITHUB_TOKEN not set in .env"
    exit 1
  fi

  if [ -z "${LINEAR_API_KEY:-}" ]; then
    print_msg "$RED" "❌ Error: LINEAR_API_KEY not set in .env"
    exit 1
  fi
}

# Create necessary directories
setup_directories() {
  mkdir -p out/.tmp/archives
  mkdir -p out/drafts
  mkdir -p out/handoff
}

# Display startup banner
show_banner() {
  print_msg "$BLUE" "╔════════════════════════════════════════╗"
  print_msg "$BLUE" "║       Goal Builder Agent v3.0          ║"
  print_msg "$BLUE" "║   GitHub Issues → Linear Goals         ║"
  print_msg "$BLUE" "╚════════════════════════════════════════╝"
  echo ""
  print_msg "$GREEN" "📋 Transform GitHub issues into structured Linear goal tickets"
  print_msg "$GREEN" "🔧 Using MCP servers for GitHub and Linear"
  echo ""
}

# Main execution
main() {
  show_banner

  print_msg "$YELLOW" "🔍 Checking prerequisites..."
  check_prerequisites
  print_msg "$GREEN" "✅ Prerequisites OK"
  echo ""

  print_msg "$YELLOW" "📁 Setting up directories..."
  setup_directories
  print_msg "$GREEN" "✅ Directories ready"
  echo ""

  print_msg "$BLUE" "🚀 Starting Goal Builder..."
  print_msg "$YELLOW" "📝 Remember to run /prime first to load all context!"
  echo ""

  # Launch Claude CLI with this directory as working directory
  # The CLAUDE.md file will be auto-loaded
  claude
}

# Trap errors
trap 'print_msg "$RED" "❌ Error occurred. Exiting..."; exit 1' ERR

# Run main function
main
