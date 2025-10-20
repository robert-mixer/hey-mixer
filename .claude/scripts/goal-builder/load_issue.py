#!/usr/bin/env python3
"""
Load full GitHub issue content by issue number.
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
    """Load a specific GitHub issue with full content."""
    parser = argparse.ArgumentParser(description="Load full GitHub issue content")
    parser.add_argument("--issue-number", type=int, required=True, help="GitHub issue number (e.g., 11)")
    parser.add_argument("--body-only", action="store_true", help="Output only the issue body (for piping)")
    args = parser.parse_args()

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
        print("❌ GitHub token not found in environment", file=sys.stderr)
        sys.exit(1)

    if not github_repo:
        print("❌ GitHub repo not configured in config.yaml", file=sys.stderr)
        sys.exit(1)

    # Initialize GitHub client
    github = GitHubClient(github_token, github_repo, logger)

    # Fetch the specific issue
    if not args.body_only:
        print(f"\n📋 Loading issue #{args.issue_number} from {github_repo}...")

    issue = github.get_issue(args.issue_number)

    if not issue:
        print(f"❌ Issue #{args.issue_number} not found", file=sys.stderr)
        sys.exit(1)

    # Body-only mode (for piping to file)
    if args.body_only:
        print(issue.get('body', ''))
        return

    # Full display mode
    print(f"\n{'='*80}")
    print(f"Issue #{issue['number']}: {issue['title']}")
    print(f"Status: {issue['state']}")
    print(f"URL: {issue['url']}")

    if issue.get('labels'):
        labels = ', '.join(issue['labels'])
        print(f"Labels: {labels}")

    print(f"Created: {issue['created_at']}")
    print(f"Updated: {issue['updated_at']}")
    print(f"{'='*80}")

    if issue.get('body'):
        print(f"\n📄 Full Description:\n")
        print(issue['body'])
    else:
        print(f"\n⚠️  This issue has no description/body content.")

    print(f"\n{'='*80}")


if __name__ == "__main__":
    main()
