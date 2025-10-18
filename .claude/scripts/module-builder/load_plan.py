#!/usr/bin/env python3
"""
Load a specific Linear plan ticket for implementation.
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
    parser = argparse.ArgumentParser(description="Load a Linear plan")
    parser.add_argument("plan_id", help="Plan ticket ID (e.g., AUTH-125)")
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

    # Load the plan
    print(f"\n📋 Loading plan {args.plan_id}...")

    try:
        plan = linear.get_issue(args.plan_id)

        if not plan:
            print(f"❌ Plan {args.plan_id} not found")
            sys.exit(1)

        print(f"\n{'='*80}")
        print(f"Plan: {plan['identifier']} - {plan['title']}")
        print(f"Status: {plan['state']['name']}")

        # Show parent goal
        if plan.get('parent'):
            print(f"Parent Goal: {plan['parent']['identifier']} - {plan['parent']['title']}")

        print(f"URL: {plan['url']}")
        print(f"{'='*80}")

        # Display full plan content
        if plan.get('description'):
            print("\n📄 Plan Content:")
            print(plan['description'])
        else:
            print("\n⚠️  No plan description found")

        print(f"{'='*80}")

        # Check status
        status = plan['state']['name'].lower()
        if status == 'todo':
            print("\n✅ This plan is ready for implementation")
            print("   Next: Update status to 'doing' before starting work")
        elif status == 'draft':
            print("\n⚠️  This plan is still in 'Draft' status")
            print("   It should be changed to 'Todo' in Linear before implementation")
        elif status in ['in progress', 'doing']:
            print("\n🔄 This plan is currently being implemented")
        elif status == 'done':
            print("\n✅ This plan has been completed")
        else:
            print(f"\n📌 Current status: {plan['state']['name']}")

    except Exception as e:
        print(f"❌ Failed to load plan: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()