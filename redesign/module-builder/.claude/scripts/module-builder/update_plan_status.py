#!/usr/bin/env python3
"""
Update the status of a Linear plan ticket.
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
    parser = argparse.ArgumentParser(description="Update plan status")
    parser.add_argument("--plan-id", required=True, help="Plan ticket ID")
    parser.add_argument("--status", required=True, help="New status (draft, todo, doing, done)")
    args = parser.parse_args()

    # Load environment and config
    ensure_env_loaded()
    project_root = Path.cwd()
    config = ConfigLoader(project_root)
    config.load()
    logger = MixerLogger(project_root, "module-builder")

    # Initialize Linear client
    linear_token = config.get_env_token("linear")
    linear_workspace = config.get("linear.workspace")
    linear_team = config.get("linear.team_id")

    if not linear_token:
        print("❌ Linear API key not found")
        sys.exit(1)

    linear = LinearClient(linear_token, linear_workspace, linear_team, logger)

    # Map status to Linear state names
    status_map = {
        "draft": "Draft",
        "todo": "Todo",
        "doing": "In Progress",
        "done": "Done",
        "closed": "Canceled"
    }

    linear_status = status_map.get(args.status.lower(), args.status)

    print(f"\n🔄 Updating plan {args.plan_id}: → {linear_status}")

    try:
        # Get the plan first to verify it exists
        plan = linear.get_issue(args.plan_id)
        if not plan:
            print(f"❌ Plan {args.plan_id} not found")
            sys.exit(1)

        # Update the status
        success = linear.update_issue_status(args.plan_id, linear_status)

        if success:
            print(f"✅ Plan status updated to: {linear_status}")

            # Add comment about status change
            linear.add_comment(args.plan_id, f"Status updated to: {linear_status}")

            # Special handling for "doing" status
            if args.status.lower() == "doing":
                print("\n📌 Plan is now in progress")
                print("   Work through the implementation steps")
                print("   Test frequently as you go")

        else:
            print(f"❌ Failed to update plan status")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Failed to update status: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()