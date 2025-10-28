#!/usr/bin/env python3
"""
Analyze a Linear goal and suggest implementation approach.
"""
import argparse
import sys
from pathlib import Path

# Add project root to path

# Add parent to path to import shared modules
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir.parent))

script_dir = Path(__file__).parent

from shared.linear_client import LinearClient
from shared.config_loader import ConfigLoader
from shared.env_loader import ensure_env_loaded
from shared.logger import MixerLogger


def analyze_goal_content(goal):
    """
    Analyze goal content and suggest implementation approach.
    This is a simple implementation - could be enhanced with AI.
    """
    title = goal['title'].lower()
    description = goal.get('description', '').lower()

    suggestions = []

    # Check for common patterns
    if 'auth' in title or 'login' in title or 'auth' in description:
        suggestions.append({
            'area': 'Authentication',
            'steps': [
                'Set up authentication module structure',
                'Implement JWT token generation',
                'Create login/logout endpoints',
                'Add password hashing',
                'Implement session management',
                'Write authentication tests'
            ]
        })

    if 'api' in title or 'endpoint' in title or 'api' in description:
        suggestions.append({
            'area': 'API Development',
            'steps': [
                'Design API schema',
                'Set up routing structure',
                'Implement CRUD endpoints',
                'Add input validation',
                'Implement error handling',
                'Write API tests'
            ]
        })

    if 'ui' in title or 'frontend' in title or 'dashboard' in description:
        suggestions.append({
            'area': 'Frontend/UI',
            'steps': [
                'Create component structure',
                'Implement UI layouts',
                'Add state management',
                'Connect to backend APIs',
                'Implement user interactions',
                'Write UI tests'
            ]
        })

    if 'database' in title or 'model' in title or 'schema' in description:
        suggestions.append({
            'area': 'Database/Data Model',
            'steps': [
                'Design database schema',
                'Create migration files',
                'Implement models/entities',
                'Add data validation',
                'Create seed data',
                'Write database tests'
            ]
        })

    return suggestions


def main():
    parser = argparse.ArgumentParser(description="Analyze a Linear goal")
    parser.add_argument("goal_id", help="Goal ticket ID (e.g., AUTH-123)")
    args = parser.parse_args()

    # Load environment and config
    ensure_env_loaded()
    project_root = Path.cwd()
    config = ConfigLoader(project_root)
    config.load()
    logger = MixerLogger(project_root, "plan-builder")

    # Initialize Linear client
    linear_token = config.get_env_token("linear")
    linear_workspace = config.get("linear.workspace")
    linear_team = config.get("linear.team_id")

    if not linear_token:
        print("❌ Linear API key not found")
        sys.exit(1)

    linear = LinearClient(linear_token, linear_workspace, linear_team, logger)

    # Load and analyze the goal
    print(f"\n🔍 Analyzing goal {args.goal_id}...")

    try:
        goal = linear.get_issue(args.goal_id)

        if not goal:
            print(f"❌ Goal {args.goal_id} not found")
            sys.exit(1)

        print(f"\n{'='*80}")
        print(f"Goal: {goal['identifier']} - {goal['title']}")
        print(f"{'='*80}")

        # Analyze the goal
        suggestions = analyze_goal_content(goal)

        if suggestions:
            print("\n📋 **Suggested Implementation Approach:**\n")

            for suggestion in suggestions:
                print(f"\n**{suggestion['area']} Components:**")
                for i, step in enumerate(suggestion['steps'], 1):
                    print(f"  {i}. {step}")

        # General implementation steps
        print("\n📝 **General Implementation Plan Structure:**\n")
        print("1. **Setup Phase**")
        print("   - Create module/component structure")
        print("   - Set up configuration")
        print("   - Install dependencies")
        print()
        print("2. **Core Implementation**")
        print("   - Build main functionality")
        print("   - Implement business logic")
        print("   - Add data handling")
        print()
        print("3. **Integration**")
        print("   - Connect components")
        print("   - Add API endpoints/routes")
        print("   - Implement error handling")
        print()
        print("4. **Testing**")
        print("   - Write unit tests")
        print("   - Add integration tests")
        print("   - Perform manual testing")
        print()
        print("5. **Documentation**")
        print("   - Add code comments")
        print("   - Update README")
        print("   - Document API/usage")

        print(f"\n{'='*80}")
        print("\n✅ Use this analysis to help write your implementation plan")
        print("   The Plan Builder agent will help you refine these into a detailed plan")

    except Exception as e:
        print(f"❌ Failed to analyze goal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()