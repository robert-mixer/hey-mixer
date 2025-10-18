#!/usr/bin/env python3
"""
Close GitHub issues after they've been included in a goal.
"""
import argparse
import sys
from pathlib import Path

# Add parent to path to import shared modules
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir.parent))

from shared.github_client import GitHubClient
from shared.config_loader import ConfigLoader
from shared.env_loader import ensure_env_loaded
from shared.logger import MixerLogger


def main():
    parser = argparse.ArgumentParser(description="Close GitHub issues")
    parser.add_argument("--issues", required=True, help="Comma-separated issue numbers")
    args = parser.parse_args()

    # Load environment and config
    ensure_env_loaded()
    project_root = Path.cwd()
    config = ConfigLoader(project_root)
    config.load()
    logger = MixerLogger(project_root, "goal-builder")

    # Initialize GitHub client
    github_token = config.get_env_token("github")
    github_repo = config.get("github.repo")

    if not github_token or not github_repo:
        print("❌ GitHub configuration missing")
        sys.exit(1)

    github = GitHubClient(github_token, github_repo, logger)

    # Parse issue numbers
    issue_numbers = [int(num.strip()) for num in args.issues.split(",")]

    print(f"\n🔒 Closing {len(issue_numbers)} GitHub issues...")

    for issue_num in issue_numbers:
        try:
            # Close the issue with a comment
            github.close_issue(
                issue_num,
                comment="✅ This issue has been included in a Linear goal ticket and is being tracked there."
            )
            print(f"   ✅ Closed issue #{issue_num}")
        except Exception as e:
            print(f"   ⚠️  Failed to close #{issue_num}: {e}")

    print("\n✅ GitHub issues have been archived")


if __name__ == "__main__":
    main()