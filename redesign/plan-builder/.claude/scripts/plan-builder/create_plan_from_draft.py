#!/usr/bin/env python3
"""
Create a Linear plan ticket from a draft file and update the parent goal.
The draft contains EXACT content written collaboratively with the user.
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
    parser = argparse.ArgumentParser(description="Create Linear plan from draft")
    parser.add_argument("--draft-file", required=True, help="Path to draft plan")
    parser.add_argument("--goal-id", required=True, help="Parent goal ticket ID")
    parser.add_argument("--status", default="draft", help="Initial status (always draft)")
    args = parser.parse_args()

    # Load environment and config
    ensure_env_loaded()
    project_root = Path.cwd()
    config = ConfigLoader(project_root)
    config.load()
    logger = MixerLogger(project_root, "plan-builder")

    # Read the draft
    draft_path = Path(args.draft_file)
    if not draft_path.exists():
        print(f"❌ Draft file not found: {draft_path}")
        sys.exit(1)

    with open(draft_path, 'r') as f:
        plan_content = f.read()

    # Extract title
    lines = plan_content.split('\n')
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
        print("❌ Linear API key not found")
        sys.exit(1)

    linear = LinearClient(linear_token, linear_workspace, linear_team, logger)

    # Get the goal ticket
    print(f"\n📋 Loading goal {args.goal_id}...")
    goal = linear.get_issue(args.goal_id)

    if not goal:
        print(f"❌ Goal {args.goal_id} not found")
        sys.exit(1)

    # Validate goal status
    goal_status = goal['state']['name'].lower()
    if goal_status != 'todo':
        print(f"⚠️  Warning: Goal {args.goal_id} has status '{goal['state']['name']}' (expected 'Todo')")
        print("   Goals should be in 'Todo' status before creating plans.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled")
            sys.exit(0)

    # Map status to Linear format
    status_map = {
        "draft": "Draft",
        "todo": "Todo",
        "doing": "In Progress",
        "done": "Done"
    }
    linear_status = status_map.get(args.status.lower(), "Draft")

    # Create plan with EXACT content from draft
    print(f"\n📝 Creating plan ticket: {title}")

    try:
        plan = linear.create_issue(
            title=title,
            description=plan_content,  # EXACT content written with user!
            label_name="plan",
            status=linear_status,
            parent_id=args.goal_id  # Link to parent goal
        )

        if plan:
            print(f"✅ Created plan: {plan.get('identifier', 'Unknown')}")
            print(f"📝 Status: {linear_status}")
            print(f"🔗 Parent: {args.goal_id}")
            print(f"🔗 URL: {plan.get('url', 'N/A')}")

            # Update goal status from "todo" to "doing"
            if goal_status == 'todo':
                print(f"\n🔄 Updating goal {args.goal_id}: todo → doing")
                linear.update_issue_status(args.goal_id, "In Progress")
                linear.add_comment(args.goal_id, f"Plan created: {plan.get('identifier', 'Unknown')}")
                print(f"✅ Goal status updated")
            else:
                print(f"\n⚠️  Goal status not updated (was: {goal['state']['name']})")

            # Clean up draft file
            draft_path.unlink()
            print("🗑️  Cleaned up draft file")

            # Report next steps
            print("\n📌 Next Steps:")
            print("   1. Review the plan in Linear")
            print("   2. When ready, change plan status from 'Draft' to 'Todo'")
            print("   3. Run Module Builder to implement")

        else:
            print("❌ Failed to create plan ticket")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Failed to create plan: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()