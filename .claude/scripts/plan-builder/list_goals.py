#!/usr/bin/env python3
"""
List Linear goal tickets, optionally filtered by status.
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
    parser = argparse.ArgumentParser(description="List Linear goals")
    parser.add_argument("--status", help="Filter by status (draft, todo, doing, done)")
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

    # Get goals
    if args.status:
        print(f"\n📋 Fetching goal tickets with status='{args.status}'...")
        goals = linear.get_issues_by_label_and_status("goal", args.status)
    else:
        print("\n📋 Fetching all goal tickets...")
        # Get all goals regardless of status
        all_goals = []
        for status in ["draft", "todo", "doing", "done"]:
            all_goals.extend(linear.get_issues_by_label_and_status("goal", status))
        goals = all_goals

    if not goals:
        if args.status:
            print(f"\n✨ No goal tickets found with status='{args.status}'")
            if args.status == "todo":
                print("\n💡 Goals need to be in 'Todo' status to create plans.")
                print("   Change a goal from 'Draft' to 'Todo' in Linear when ready.")
        else:
            print("\n✨ No goal tickets found")
        return

    print(f"\n📌 Found {len(goals)} goal ticket(s):\n")
    print("=" * 80)

    for goal in goals:
        print(f"\n{goal['identifier']}: {goal['title']}")
        print(f"Status: {goal['state']['name']}")
        print(f"URL: {goal['url']}")

        # Check for linked plans
        if goal.get('children') and goal['children'].get('nodes'):
            print(f"Linked Plans:")
            for child in goal['children']['nodes']:
                print(f"  - {child['identifier']}: {child['title']}")

        # Show description preview
        if goal.get('description'):
            desc = goal['description']
            excerpt = desc[:200] + "..." if len(desc) > 200 else desc
            print(f"\nDescription:\n{excerpt}")

        print("-" * 80)

    if args.status == "todo":
        print("\n✅ These goals are ready for plan creation")
        print("   Use '/create-plan' to create an implementation plan")


if __name__ == "__main__":
    main()