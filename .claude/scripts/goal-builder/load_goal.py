#!/usr/bin/env python3
"""
Load full Linear goal content by goal ID.
"""
import argparse
import sys
from pathlib import Path

# Add parent to path to import shared modules
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir.parent))

from shared.linear_client import LinearClient
from shared.config_loader import ConfigLoader
from shared.env_loader import ensure_env_loaded
from shared.logger import MixerLogger


def main():
    """Load a specific Linear goal with full content."""
    parser = argparse.ArgumentParser(description="Load full Linear goal content")
    parser.add_argument("--goal-id", type=str, required=True, help="Linear goal ID (e.g., SYS-8)")
    parser.add_argument("--description-only", action="store_true", help="Output only the description (for piping)")
    args = parser.parse_args()

    # Load environment
    ensure_env_loaded()

    # Get project root
    project_root = Path.cwd()

    # Initialize config and logger
    config = ConfigLoader(project_root)
    config.load()
    logger = MixerLogger(project_root, "goal-builder")

    # Get Linear configuration
    linear_token = config.get_env_token("linear")
    linear_workspace = config.get("linear.workspace")
    linear_team = config.get("linear.team_id")

    if not linear_token:
        print("❌ Linear API key not found in environment", file=sys.stderr)
        sys.exit(1)

    if not linear_workspace or not linear_team:
        print("❌ Linear workspace or team not configured in config.yaml", file=sys.stderr)
        sys.exit(1)

    # Initialize Linear client
    linear = LinearClient(linear_token, linear_workspace, linear_team, logger)

    # Fetch the specific goal
    if not args.description_only:
        print(f"\n📋 Loading goal {args.goal_id} from Linear...")

    goal = linear.get_issue(args.goal_id)

    if not goal:
        print(f"❌ Goal {args.goal_id} not found", file=sys.stderr)
        sys.exit(1)

    # Description-only mode (for piping to file)
    if args.description_only:
        print(goal.get('description', ''))
        return

    # Full display mode
    print(f"\n{'='*80}")
    print(f"Goal: {goal['identifier']} - {goal['title']}")
    print(f"Status: {goal['state']['name']}")
    print(f"URL: {goal['url']}")

    if goal.get('labels') and goal['labels'].get('nodes'):
        labels = [label['name'] for label in goal['labels']['nodes']]
        if labels:
            print(f"Labels: {', '.join(labels)}")

    print(f"{'='*80}")

    if goal.get('description'):
        print(f"\n📄 Full Description:\n")
        print(goal['description'])
    else:
        print(f"\n⚠️  This goal has no description content.")

    print(f"\n{'='*80}")

    # Show parent goal if exists
    if goal.get('parent'):
        parent = goal['parent']
        print(f"\n⬆️  Parent: {parent['identifier']} - {parent['title']}")

    # Show child plans if exist
    if goal.get('children') and goal['children'].get('nodes'):
        print(f"\n⬇️  Child plans:")
        for child in goal['children']['nodes']:
            print(f"   - {child['identifier']}: {child['title']} ({child['state']['name']})")


if __name__ == "__main__":
    main()
