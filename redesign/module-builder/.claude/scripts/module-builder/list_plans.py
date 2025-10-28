#!/usr/bin/env python3
"""
List Linear plan tickets, optionally filtered by status.
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
    parser = argparse.ArgumentParser(description="List Linear plans")
    parser.add_argument("--status", help="Filter by status (draft, todo, doing, done)")
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

    # Get plans
    if args.status:
        print(f"\n📋 Fetching plan tickets with status='{args.status}'...")
        plans = linear.get_issues_by_label_and_status("plan", args.status)
    else:
        print("\n📋 Fetching all plan tickets...")
        # Get all plans regardless of status
        all_plans = []
        for status in ["draft", "todo", "doing", "done"]:
            all_plans.extend(linear.get_issues_by_label_and_status("plan", status))
        plans = all_plans

    if not plans:
        if args.status:
            print(f"\n✨ No plan tickets found with status='{args.status}'")
            if args.status == "todo":
                print("\n💡 Plans need to be in 'Todo' status to start implementation.")
                print("   Change a plan from 'Draft' to 'Todo' in Linear when ready.")
        else:
            print("\n✨ No plan tickets found")
        return

    print(f"\n📌 Found {len(plans)} plan ticket(s):\n")
    print("=" * 80)

    for plan in plans:
        print(f"\n{plan['identifier']}: {plan['title']}")
        print(f"Status: {plan['state']['name']}")

        # Show parent goal if exists
        if plan.get('parent'):
            print(f"Parent Goal: {plan['parent']['identifier']} - {plan['parent']['title']}")

        print(f"URL: {plan['url']}")

        # Show description preview
        if plan.get('description'):
            desc = plan['description']
            # Try to extract implementation steps
            if 'Implementation Steps' in desc or '## Steps' in desc:
                print("\nImplementation Steps Preview:")
                lines = desc.split('\n')
                step_count = 0
                for line in lines:
                    if line.strip().startswith(('1.', '2.', '3.', '- ', '* ')):
                        print(f"  {line.strip()}")
                        step_count += 1
                        if step_count >= 3:
                            print("  ...")
                            break

        print("-" * 80)

    if args.status == "todo":
        print("\n✅ These plans are ready for implementation")
        print("   Use '/load-plan' to start implementing")


if __name__ == "__main__":
    main()