#!/usr/bin/env python3
"""
Mark both a plan and its parent goal as complete.
"""
import argparse
import sys
from pathlib import Path

# Add parent to path to import shared modules
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir.parent))

from datetime import datetime

# Add project root to path
script_dir = Path(__file__).parent

from shared.linear_client import LinearClient
from shared.config_loader import ConfigLoader
from shared.env_loader import ensure_env_loaded
from shared.logger import MixerLogger


def main():
    parser = argparse.ArgumentParser(description="Mark plan and goal complete")
    parser.add_argument("--plan-id", required=True, help="Plan ticket ID")
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

    print(f"\n📋 Loading plan {args.plan_id}...")

    try:
        # Get the plan
        plan = linear.get_issue(args.plan_id)

        if not plan:
            print(f"❌ Plan {args.plan_id} not found")
            sys.exit(1)

        # Verify plan is in "doing" status
        plan_status = plan['state']['name'].lower()
        if plan_status not in ['in progress', 'doing']:
            print(f"⚠️  Warning: Plan is in '{plan['state']['name']}' status (expected 'In Progress')")
            response = input("Mark as complete anyway? (y/n): ")
            if response.lower() != 'y':
                print("Cancelled")
                sys.exit(0)

        # Get the parent goal
        parent_goal = plan.get('parent')
        if parent_goal:
            print(f"📋 Found parent goal: {parent_goal['identifier']} - {parent_goal['title']}")
        else:
            print("⚠️  No parent goal found for this plan")

        # Update plan to done
        print(f"\n🔄 Updating plan {args.plan_id}: → Done")
        success = linear.update_issue_status(args.plan_id, "Done")

        if success:
            timestamp = datetime.now().isoformat()
            linear.add_comment(args.plan_id, f"✅ Implementation complete at {timestamp}")
            print(f"✅ Plan marked as done")
        else:
            print(f"❌ Failed to update plan status")
            sys.exit(1)

        # Update parent goal to done
        if parent_goal:
            goal_id = parent_goal['identifier']
            print(f"\n🔄 Updating goal {goal_id}: → Done")

            success = linear.update_issue_status(goal_id, "Done")
            if success:
                linear.add_comment(
                    goal_id,
                    f"✅ Goal complete. Plan {args.plan_id} implemented at {timestamp}"
                )
                print(f"✅ Goal marked as done")
            else:
                print(f"⚠️  Failed to update goal status")

        print("\n🎉 Implementation complete!")
        print("\nSummary:")
        print(f"  Plan {args.plan_id}: ✅ Done")
        if parent_goal:
            print(f"  Goal {parent_goal['identifier']}: ✅ Done")

        print("\n📌 Next steps:")
        print("   - Review the completed work")
        print("   - Check for any follow-up tasks")
        print("   - Create new goals for additional features")

    except Exception as e:
        print(f"❌ Failed to mark complete: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()