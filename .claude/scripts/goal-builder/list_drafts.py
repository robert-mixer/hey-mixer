#!/usr/bin/env python3
"""
List all draft Linear goal tickets.
"""
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
    """List all draft Linear goals."""
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
        print("❌ Linear API key not found in environment")
        sys.exit(1)

    if not linear_workspace or not linear_team:
        print("❌ Linear workspace or team not configured in config.yaml")
        sys.exit(1)

    # Initialize Linear client
    linear = LinearClient(linear_token, linear_workspace, linear_team, logger)

    # Fetch draft goals
    print(f"\n📋 Fetching draft goal tickets from Linear...")
    drafts = linear.get_issues_by_label_and_status("goal", "draft")

    if not drafts:
        print("\n✨ No draft goals found.")
        print("Create a goal using /goal-builder:create-goal to get started!")
        return

    print(f"\n📌 Found {len(drafts)} draft goals:\n")
    print("=" * 80)

    for draft in drafts:
        identifier = draft.get('identifier', 'Unknown')
        title = draft.get('title', 'No title')
        url = draft.get('url', 'N/A')
        description = draft.get('description', '')

        print(f"\n{identifier}: {title}")
        print(f"Status: {draft.get('state', {}).get('name', 'Unknown')}")
        print(f"URL: {url}")

        # Show first 200 chars of description
        if description:
            excerpt = description[:200] + "..." if len(description) > 200 else description
            print(f"\nDescription:\n{excerpt}")

        print("-" * 80)

    print(f"\n📊 Total: {len(drafts)} draft goals")
    print("\n💡 Tip: Use '/goal-builder:edit-draft [identifier]' to modify a draft")


if __name__ == "__main__":
    main()
