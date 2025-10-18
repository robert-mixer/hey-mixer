#!/bin/bash
# Test setup script for mixer-system-v2

echo "🧪 Mixer System V2 - Test Setup"
echo "================================"
echo ""
echo "This will help you test the mixer system."
echo ""

# Check for required environment variables
if [ -z "$GITHUB_TOKEN" ] || [ -z "$LINEAR_API_KEY" ]; then
    echo "⚠️  Loading environment variables from .env..."
    source .env
fi

echo "Current Configuration:"
echo "---------------------"
if [ -f "config.yaml" ]; then
    echo "✅ config.yaml exists"
    grep "repo:" config.yaml
    grep "workspace:" config.yaml
    grep "team_id:" config.yaml
else
    echo "❌ config.yaml not found!"
    echo ""
    echo "Please create config.yaml with:"
    echo "  - github.repo: your GitHub repository"
    echo "  - linear.workspace: your Linear workspace"
    echo "  - linear.team_id: your Linear team ID"
    exit 1
fi

echo ""
echo "To test the system:"
echo "-------------------"
echo "1. Make sure you have:"
echo "   - A GitHub repo with some open issues"
echo "   - Access to a Linear workspace"
echo ""
echo "2. Update config.yaml with your details"
echo ""
echo "3. Run an agent:"
echo "   ./mixer.sh goal-builder    # Process GitHub issues → Linear goals"
echo "   ./mixer.sh plan-builder    # Create plans from goals"
echo "   ./mixer.sh module-builder  # Implement plans"
echo ""
echo "The new conversational workflow will:"
echo "- Goal Builder: Help you write goal tickets WITH the agent"
echo "- Plan Builder: Collaborate on implementation plans"
echo "- Module Builder: Implement code interactively"
echo ""