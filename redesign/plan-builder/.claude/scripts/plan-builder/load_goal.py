#!/usr/bin/env python3
"""
Load a specific Linear goal ticket for analysis.
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


def main():
    parser = argparse.ArgumentParser(description="Load a Linear goal")
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

    # Load the goal
    print(f"\n📋 Loading goal {args.goal_id}...")

    try:
        goal = linear.get_issue(args.goal_id)

        if not goal:
            print(f"❌ Goal {args.goal_id} not found")
            sys.exit(1)

        print(f"\n{'='*80}")
        print(f"Goal: {goal['identifier']} - {goal['title']}")
        print(f"Status: {goal['state']['name']}")
        print(f"URL: {goal['url']}")
        print(f"{'='*80}")

        if goal.get('description'):
            print("\n📄 Description:")
            print(goal['description'])

        print(f"{'='*80}")

        # Check for linked plans
        if goal.get('children') and goal['children'].get('nodes'):
            print("\n⚠️  This goal already has linked plan(s):")
            for child in goal['children']['nodes']:
                print(f"   - {child['identifier']}: {child['title']} ({child['state']['name']})")
            print("\n   Consider if a new plan is needed or if you should update an existing one.")

        # Check status
        if goal['state']['name'].lower() != 'todo':
            print(f"\n⚠️  Note: This goal has status '{goal['state']['name']}'")
            print("   Goals should typically be in 'Todo' status before creating a plan.")

    except Exception as e:
        print(f"❌ Failed to load goal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()