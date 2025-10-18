#!/usr/bin/env python3
"""
Create a Linear goal ticket from a draft file.
The draft contains EXACT content written collaboratively with the user.
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
    parser = argparse.ArgumentParser(description="Create Linear goal from draft")
    parser.add_argument("--draft-file", required=True, help="Path to draft ticket")
    parser.add_argument("--issues", help="GitHub issues to reference (comma-separated)")
    parser.add_argument("--status", default="draft", help="Initial status (always draft)")
    args = parser.parse_args()

    # Load environment and config
    ensure_env_loaded()
    project_root = Path.cwd()
    config = ConfigLoader(project_root)
    config.load()
    logger = MixerLogger(project_root, "goal-builder")

    # Read the draft (written WITH the user, not auto-generated!)
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

    # Map status to Linear format
    status_map = {
        "draft": "Draft",
        "todo": "Todo",
        "doing": "In Progress",
        "done": "Done"
    }
    linear_status = status_map.get(args.status.lower(), "Draft")

    # Create goal with EXACT content from draft
    print(f"\n📝 Creating goal ticket: {title}")

    try:
        goal = linear.create_issue(
            title=title,
            description=ticket_content,  # EXACT content written with user!
            label_name="goal",
            status=linear_status
        )

        if goal:
            print(f"✅ Created goal: {goal.get('identifier', 'Unknown')}")
            print(f"📝 Status: {linear_status}")
            print(f"🔗 URL: {goal.get('url', 'N/A')}")
            print("\n📋 The ticket contains EXACTLY what we wrote together")

            # Clean up draft file
            draft_path.unlink()
            print("🗑️  Cleaned up draft file")

            # Report next steps
            print("\n📌 Next Steps:")
            print("   1. Review the goal in Linear")
            print("   2. When ready, change status from 'Draft' to 'Todo'")
            print("   3. Run Plan Builder to create implementation plan")
        else:
            print("❌ Failed to create goal ticket")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Failed to create goal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()