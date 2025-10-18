"""
Linear API client for Mixer System
"""
from typing import List, Dict, Any, Optional
import requests
from .logger import MixerLogger


class LinearClient:
    """Client for interacting with Linear API"""

    API_URL = "https://api.linear.app/graphql"

    def __init__(self, api_key: str, workspace: str, team_id: str, logger: Optional[MixerLogger] = None):
        """
        Initialize Linear client

        Args:
            api_key: Linear API key
            workspace: Workspace identifier
            team_id: Team ID (e.g., "TEAM")
            logger: Logger instance
        """
        self.api_key = api_key
        self.workspace = workspace
        self.team_id = team_id
        self.logger = logger or MixerLogger()
        self.headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }

    def _query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute GraphQL query

        Args:
            query: GraphQL query string
            variables: Query variables

        Returns:
            Response data

        Raises:
            requests.HTTPError: If request fails
        """
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        response = requests.post(
            self.API_URL,
            json=payload,
            headers=self.headers,
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        if "errors" in data:
            error_msg = data["errors"][0].get("message", "Unknown error")
            self.logger.error(f"Linear API error: {error_msg}")
            raise Exception(f"Linear API error: {error_msg}")

        return data.get("data", {})

    def test_connection(self) -> bool:
        """
        Test Linear connection and authentication

        Returns:
            True if connection successful, False otherwise
        """
        query = """
        query {
            viewer {
                id
                name
                email
            }
        }
        """

        try:
            data = self._query(query)
            viewer = data.get("viewer", {})
            self.logger.info(f"Linear connection successful: {viewer.get('name')} ({viewer.get('email')})")
            return True

        except Exception as e:
            self.logger.error(f"Linear connection failed: {e}")
            return False

    def get_team_id(self) -> Optional[str]:
        """
        Get team's internal ID from team key

        Returns:
            Team internal ID or None if not found
        """
        query = """
        query ($teamKey: String!) {
            team(id: $teamKey) {
                id
                key
                name
            }
        }
        """

        try:
            data = self._query(query, {"teamKey": self.team_id})
            team = data.get("team", {})
            return team.get("id")

        except Exception as e:
            self.logger.error(f"Failed to get team ID: {e}")
            return None

    def create_issue(
        self,
        title: str,
        description: str,
        label_name: Optional[str] = None,
        status: str = "Todo",
        priority: int = 3,
        parent_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Create a Linear issue

        Args:
            title: Issue title
            description: Issue description (markdown)
            label_name: Label to add (e.g., "goal", "plan")
            status: Status name (e.g., "Todo", "In Progress", "Done")
            priority: Priority 0-4 (0=none, 1=urgent, 2=high, 3=medium, 4=low)
            parent_id: Optional parent issue ID for linking

        Returns:
            Issue data dict if successful, None otherwise
        """
        # Get team internal ID
        team_internal_id = self.get_team_id()
        if not team_internal_id:
            self.logger.error("Failed to get team internal ID")
            return None

        # Get label ID if label specified
        label_id = None
        if label_name:
            label_id = self._get_or_create_label(label_name)

        # Get status ID
        status_id = self._get_workflow_state_id(status)
        if not status_id:
            self.logger.warning(f"Status '{status}' not found, using team default")

        query = """
        mutation ($input: IssueCreateInput!) {
            issueCreate(input: $input) {
                success
                issue {
                    id
                    identifier
                    title
                    url
                    state {
                        name
                    }
                }
            }
        }
        """

        variables = {
            "input": {
                "teamId": team_internal_id,
                "title": title,
                "description": description,
                "priority": priority
            }
        }

        if label_id:
            variables["input"]["labelIds"] = [label_id]

        if status_id:
            variables["input"]["stateId"] = status_id

        # Add parent linking if specified
        if parent_id:
            # If parent_id is an identifier like "AUTH-123", get the internal ID
            if "-" in parent_id:
                parent = self.get_issue(parent_id)
                if parent:
                    variables["input"]["parentId"] = parent["id"]
            else:
                variables["input"]["parentId"] = parent_id

        try:
            data = self._query(query, variables)
            result = data.get("issueCreate", {})

            if result.get("success"):
                issue = result.get("issue", {})
                self.logger.info(f"Created Linear issue: {issue.get('identifier')} - {title}")
                self.logger.log_api_call("linear", "issueCreate", "success")
                return issue
            else:
                self.logger.error("Failed to create Linear issue")
                return None

        except Exception as e:
            self.logger.error(f"Failed to create Linear issue: {e}")
            self.logger.log_api_call("linear", "issueCreate", "error")
            return None

    def _get_or_create_label(self, label_name: str) -> Optional[str]:
        """
        Get or create label by name

        Args:
            label_name: Label name

        Returns:
            Label ID or None if failed
        """
        # Get team internal ID
        team_internal_id = self.get_team_id()
        if not team_internal_id:
            return None

        # First, try to get existing label
        query = """
        query ($teamId: String!) {
            team(id: $teamId) {
                labels {
                    nodes {
                        id
                        name
                    }
                }
            }
        }
        """

        try:
            data = self._query(query, {"teamId": team_internal_id})
            labels = data.get("team", {}).get("labels", {}).get("nodes", [])

            for label in labels:
                if label.get("name", "").lower() == label_name.lower():
                    return label.get("id")

            # Label doesn't exist, create it
            create_query = """
            mutation ($input: IssueLabelCreateInput!) {
                issueLabelCreate(input: $input) {
                    success
                    issueLabel {
                        id
                        name
                    }
                }
            }
            """

            create_data = self._query(create_query, {
                "input": {
                    "teamId": team_internal_id,
                    "name": label_name
                }
            })

            result = create_data.get("issueLabelCreate", {})
            if result.get("success"):
                label_id = result.get("issueLabel", {}).get("id")
                self.logger.info(f"Created label: {label_name}")
                return label_id

        except Exception as e:
            self.logger.error(f"Failed to get/create label: {e}")

        return None

    def _get_workflow_state_id(self, state_name: str) -> Optional[str]:
        """
        Get workflow state ID by name

        Args:
            state_name: State name (e.g., "Todo", "In Progress")

        Returns:
            State ID or None if not found
        """
        team_internal_id = self.get_team_id()
        if not team_internal_id:
            return None

        query = """
        query ($teamId: String!) {
            team(id: $teamId) {
                states {
                    nodes {
                        id
                        name
                    }
                }
            }
        }
        """

        try:
            data = self._query(query, {"teamId": team_internal_id})
            states = data.get("team", {}).get("states", {}).get("nodes", [])

            for state in states:
                if state.get("name", "").lower() == state_name.lower():
                    return state.get("id")

        except Exception as e:
            self.logger.error(f"Failed to get workflow state: {e}")

        return None

    def get_issue(self, issue_id: str) -> Optional[Dict[str, Any]]:
        """
        Get issue by identifier (e.g., "TEAM-123")

        Args:
            issue_id: Issue identifier

        Returns:
            Issue data or None if not found
        """
        query = """
        query ($issueId: String!) {
            issue(id: $issueId) {
                id
                identifier
                title
                description
                url
                state {
                    name
                }
                labels {
                    nodes {
                        name
                    }
                }
                parent {
                    id
                    identifier
                    title
                }
                children {
                    nodes {
                        id
                        identifier
                        title
                        state {
                            name
                        }
                    }
                }
            }
        }
        """

        try:
            data = self._query(query, {"issueId": issue_id})
            return data.get("issue")

        except Exception as e:
            self.logger.error(f"Failed to get issue {issue_id}: {e}")
            return None

    def update_issue_status(self, issue_id: str, status: str) -> bool:
        """
        Update issue status

        Args:
            issue_id: Issue identifier
            status: New status name

        Returns:
            True if successful, False otherwise
        """
        state_id = self._get_workflow_state_id(status)
        if not state_id:
            self.logger.error(f"Status '{status}' not found")
            return False

        query = """
        mutation ($issueId: String!, $stateId: String!) {
            issueUpdate(id: $issueId, input: { stateId: $stateId }) {
                success
            }
        }
        """

        try:
            data = self._query(query, {"issueId": issue_id, "stateId": state_id})
            success = data.get("issueUpdate", {}).get("success", False)

            if success:
                self.logger.info(f"Updated issue {issue_id} status to {status}")

            return success

        except Exception as e:
            self.logger.error(f"Failed to update issue status: {e}")
            return False

    def add_comment(self, issue_id: str, comment: str) -> bool:
        """
        Add comment to issue

        Args:
            issue_id: Issue identifier
            comment: Comment text (markdown)

        Returns:
            True if successful, False otherwise
        """
        query = """
        mutation ($input: CommentCreateInput!) {
            commentCreate(input: $input) {
                success
            }
        }
        """

        try:
            data = self._query(query, {
                "input": {
                    "issueId": issue_id,
                    "body": comment
                }
            })

            success = data.get("commentCreate", {}).get("success", False)
            if success:
                self.logger.info(f"Added comment to issue {issue_id}")

            return success

        except Exception as e:
            self.logger.error(f"Failed to add comment: {e}")
            return False

    def get_issues_by_label_and_status(self, label: str, status: str) -> List[Dict[str, Any]]:
        """
        Get issues filtered by label and status.

        Args:
            label: Label name (e.g., "goal" or "plan")
            status: Status name (e.g., "todo", "doing", "done")

        Returns:
            List of matching issues
        """
        # Get the team's internal ID
        team_internal_id = self.get_team_id()
        if not team_internal_id:
            return []

        # Map status names
        status_map = {
            "draft": "Draft",
            "todo": "Todo",
            "doing": "In Progress",
            "done": "Done",
            "closed": "Canceled"
        }
        linear_status = status_map.get(status.lower(), status)

        query = """
        query ($teamId: String!, $label: String!, $status: String!) {
            issues(
                filter: {
                    team: { id: { eq: $teamId } }
                    labels: { name: { eq: $label } }
                    state: { name: { eq: $status } }
                }
            ) {
                nodes {
                    id
                    identifier
                    title
                    description
                    url
                    state {
                        name
                    }
                    labels {
                        nodes {
                            name
                        }
                    }
                    parent {
                        id
                        identifier
                        title
                    }
                    children {
                        nodes {
                            id
                            identifier
                            title
                        }
                    }
                }
            }
        }
        """

        try:
            data = self._query(query, {
                "teamId": team_internal_id,
                "label": label,
                "status": linear_status
            })
            return data.get("issues", {}).get("nodes", [])

        except Exception as e:
            self.logger.error(f"Failed to get issues by label and status: {e}")
            return []

    def link_issues(self, child_id: str, parent_id: str) -> bool:
        """
        Link a child issue to a parent issue.

        Args:
            child_id: Child issue identifier
            parent_id: Parent issue identifier

        Returns:
            True if successful, False otherwise
        """
        # Get the parent issue's internal ID
        parent = self.get_issue(parent_id)
        if not parent:
            self.logger.error(f"Parent issue {parent_id} not found")
            return False

        query = """
        mutation ($childId: String!, $parentId: String!) {
            issueUpdate(id: $childId, input: { parentId: $parentId }) {
                success
            }
        }
        """

        try:
            data = self._query(query, {
                "childId": child_id,
                "parentId": parent["id"]
            })

            success = data.get("issueUpdate", {}).get("success", False)
            if success:
                self.logger.info(f"Linked {child_id} to parent {parent_id}")

            return success

        except Exception as e:
            self.logger.error(f"Failed to link issues: {e}")
            return False

    def close_issue(self, issue_id: str, comment: str = None) -> bool:
        """
        Close/cancel an issue.

        Args:
            issue_id: Issue identifier
            comment: Optional closing comment

        Returns:
            True if successful, False otherwise
        """
        if comment:
            self.add_comment(issue_id, comment)

        return self.update_issue_status(issue_id, "Canceled")
