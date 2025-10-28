#!/usr/bin/env python3
"""
List all open GitHub issues from the configured repository.
"""
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
    """List all open GitHub issues."""
    # Load environment
    ensure_env_loaded()

    # Get project root
    project_root = Path.cwd()

    # Initialize config and logger
    config = ConfigLoader(project_root)
    config.load()
    logger = MixerLogger(project_root, "goal-builder")

    # Get GitHub configuration
    github_token = config.get_env_token("github")
    github_repo = config.get("github.repo")

    if not github_token:
        print("❌ GitHub token not found in environment")
        sys.exit(1)

    if not github_repo:
        print("❌ GitHub repo not configured in config.yaml")
        sys.exit(1)

    # Initialize GitHub client
    github = GitHubClient(github_token, github_repo, logger)

    # Fetch open issues
    print(f"\n📋 Fetching issues from {github_repo}...")
    issues = github.get_open_issues()

    if not issues:
        print("\n✨ No open issues found in the repository.")
        print("Create some GitHub issues to use as your 'stash' of ideas!")
        return

    print(f"\n📌 Found {len(issues)} open issues:\n")
    print("=" * 80)

    for issue in issues:
        print(f"\n#{issue['number']}: {issue['title']}")
        print(f"Created: {issue['created_at']}")
        print(f"URL: {issue['url']}")

        if issue.get('labels'):
            labels = ', '.join(issue['labels'])
            print(f"Labels: {labels}")

        if issue.get('body'):
            body = issue['body']
            # Show first 200 chars of body
            excerpt = body[:200] + "..." if len(body) > 200 else body
            print(f"\nDescription:\n{excerpt}")

        print("-" * 80)

    print(f"\n📊 Total: {len(issues)} open issues")
    print("\n💡 Tip: Use '/create-goal' to group these issues into a goal")


if __name__ == "__main__":
    main()