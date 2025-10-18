"""
GitHub API client for Mixer System
"""
from typing import List, Dict, Any, Optional
from github import Github, GithubException
from .logger import MixerLogger


class GitHubClient:
    """Client for interacting with GitHub API"""

    def __init__(self, token: str, repo: str, logger: Optional[MixerLogger] = None):
        """
        Initialize GitHub client

        Args:
            token: GitHub personal access token
            repo: Repository in format "username/repo"
            logger: Logger instance
        """
        self.token = token
        self.repo_name = repo
        self.logger = logger or MixerLogger()
        self.client = Github(token)
        self.repo = self.client.get_repo(repo)

    def get_open_issues(self) -> List[Dict[str, Any]]:
        """
        Get all open issues (stash items)

        Returns:
            List of issue dictionaries with relevant fields
        """
        self.logger.info(f"Fetching open issues from {self.repo_name}")

        try:
            issues = self.repo.get_issues(state='open')
            issue_list = []

            for issue in issues:
                # Skip pull requests (they appear as issues in GitHub API)
                if issue.pull_request:
                    continue

                issue_data = {
                    'number': issue.number,
                    'title': issue.title,
                    'body': issue.body or "",
                    'url': issue.html_url,
                    'created_at': issue.created_at,
                    'updated_at': issue.updated_at,
                    'labels': [label.name for label in issue.labels],
                    'state': issue.state
                }
                issue_list.append(issue_data)

            self.logger.info(f"Found {len(issue_list)} open issues")
            self.logger.log_api_call("github", f"repos/{self.repo_name}/issues", "success")
            return issue_list

        except GithubException as e:
            self.logger.error(f"GitHub API error: {e.status} - {e.data}")
            self.logger.log_api_call("github", f"repos/{self.repo_name}/issues", "error")
            raise

    def get_issue(self, issue_number: int) -> Optional[Dict[str, Any]]:
        """
        Get specific issue by number

        Args:
            issue_number: Issue number

        Returns:
            Issue dictionary or None if not found
        """
        try:
            issue = self.repo.get_issue(issue_number)

            return {
                'number': issue.number,
                'title': issue.title,
                'body': issue.body or "",
                'url': issue.html_url,
                'created_at': issue.created_at,
                'updated_at': issue.updated_at,
                'labels': [label.name for label in issue.labels],
                'state': issue.state
            }

        except GithubException as e:
            self.logger.error(f"Failed to get issue #{issue_number}: {e}")
            return None

    def close_issue(self, issue_number: int, comment: Optional[str] = None) -> bool:
        """
        Close an issue

        Args:
            issue_number: Issue number to close
            comment: Optional comment to add before closing

        Returns:
            True if successful, False otherwise
        """
        try:
            issue = self.repo.get_issue(issue_number)

            if comment:
                issue.create_comment(comment)
                self.logger.info(f"Added comment to issue #{issue_number}")

            issue.edit(state='closed')
            self.logger.info(f"Closed issue #{issue_number}")
            self.logger.log_api_call("github", f"repos/{self.repo_name}/issues/{issue_number}", "success")
            return True

        except GithubException as e:
            self.logger.error(f"Failed to close issue #{issue_number}: {e}")
            self.logger.log_api_call("github", f"repos/{self.repo_name}/issues/{issue_number}", "error")
            return False

    def add_comment(self, issue_number: int, comment: str) -> bool:
        """
        Add comment to an issue

        Args:
            issue_number: Issue number
            comment: Comment text

        Returns:
            True if successful, False otherwise
        """
        try:
            issue = self.repo.get_issue(issue_number)
            issue.create_comment(comment)
            self.logger.info(f"Added comment to issue #{issue_number}")
            return True

        except GithubException as e:
            self.logger.error(f"Failed to add comment to issue #{issue_number}: {e}")
            return False

    def create_issue(self, title: str, body: str, labels: Optional[List[str]] = None) -> Optional[int]:
        """
        Create a new issue

        Args:
            title: Issue title
            body: Issue body
            labels: Optional list of label names

        Returns:
            Issue number if successful, None otherwise
        """
        try:
            issue = self.repo.create_issue(
                title=title,
                body=body,
                labels=labels or []
            )
            self.logger.info(f"Created issue #{issue.number}: {title}")
            return issue.number

        except GithubException as e:
            self.logger.error(f"Failed to create issue: {e}")
            return None

    def get_repo_info(self) -> Dict[str, Any]:
        """
        Get repository information

        Returns:
            Repository info dictionary
        """
        try:
            return {
                'name': self.repo.name,
                'full_name': self.repo.full_name,
                'description': self.repo.description,
                'url': self.repo.html_url,
                'open_issues_count': self.repo.open_issues_count,
                'default_branch': self.repo.default_branch
            }
        except GithubException as e:
            self.logger.error(f"Failed to get repo info: {e}")
            return {}

    def test_connection(self) -> bool:
        """
        Test GitHub connection and authentication

        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Try to get repo info
            _ = self.repo.name
            self.logger.info(f"GitHub connection successful: {self.repo_name}")
            return True

        except GithubException as e:
            self.logger.error(f"GitHub connection failed: {e}")
            return False
