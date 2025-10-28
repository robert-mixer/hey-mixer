#!/usr/bin/env python3
"""
Update an existing Linear goal ticket from a draft file.
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
    parser = argparse.ArgumentParser(description="Update Linear goal from draft")
    parser.add_argument("--goal-id", required=True, help="Goal identifier (e.g., SYS-8)")
    parser.add_argument("--draft-file", required=True, help="Path to draft file")
    args = parser.parse_args()

    # Load environment and config
    ensure_env_loaded()
    project_root = Path.cwd()
    config = ConfigLoader(project_root)
    config.load()
    logger = MixerLogger(project_root, "goal-builder")

    # Read the draft
    draft_path = Path(args.draft_file)
    if not draft_path.exists():
        print(f"❌ Draft file not found: {draft_path}")
        sys.exit(1)

    with open(draft_path, 'r') as f:
        ticket_content = f.read()

    # Extract title from first # heading
    lines = ticket_content.split('\n')
    title = None
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break

    if not title:
        print("❌ No title found in draft (needs # heading)")
        sys.exit(1)

    # Initialize Linear client
    linear_token = config.get_env_token("linear")
    linear_workspace = config.get("linear.workspace")
    linear_team = config.get("linear.team_id")

    if not linear_token:
        print("❌ Linear API key not found in environment")
        sys.exit(1)

    linear = LinearClient(linear_token, linear_workspace, linear_team, logger)

    # Update the goal
    print(f"\n📝 Updating goal ticket: {args.goal_id}")
    print(f"   New title: {title}")

    try:
        success = linear.update_issue(
            issue_id=args.goal_id,
            title=title,
            description=ticket_content
        )

        if success:
            # Get updated issue to show details
            updated = linear.get_issue(args.goal_id)
            if updated:
                print(f"✅ Updated goal: {updated.get('identifier')}")
                print(f"📝 Title: {updated.get('title')}")
                print(f"🔗 URL: {updated.get('url')}")
                print("\n📋 The ticket has been updated with the new content")

                # Clean up draft file
                draft_path.unlink()
                print("🗑️  Cleaned up draft file")

                # Report next steps
                print("\n📌 Next Steps:")
                print("   1. Review the updated goal in Linear")
                print("   2. When ready, change status from 'Draft' to 'Todo'")
                print("   3. Run Plan Builder to create implementation plan")
            else:
                print("✅ Goal updated successfully")
        else:
            print("❌ Failed to update goal ticket")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Failed to update goal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
