"""
Configuration loader for mixer-system-v2.
Loads configuration from config.yaml in the project root.
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigLoader:
    """Load and manage mixer configuration."""

    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize config loader.

        Args:
            project_root: Root directory of project. If None, uses current directory.
        """
        self.project_root = project_root or Path.cwd()
        # Look for config.yaml in the project root
        self.config_path = self.project_root / "config.yaml"
        self._config: Optional[Dict[str, Any]] = None

    def exists(self) -> bool:
        """Check if config exists."""
        return self.config_path.exists()

    def load(self) -> Dict[str, Any]:
        """
        Load configuration from config.yaml.

        Returns:
            Configuration dictionary

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file is invalid YAML
        """
        if not self.exists():
            raise FileNotFoundError(
                f"No configuration found at {self.config_path}\n"
                "Please create config.yaml with:\n"
                "  github.repo: your GitHub repository\n"
                "  linear.workspace: your Linear workspace\n"
                "  linear.team_id: your Linear team ID"
            )

        with open(self.config_path, 'r') as f:
            self._config = yaml.safe_load(f) or {}

        return self._config

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get config value by dot-notation path.

        Args:
            key_path: Dot-separated path (e.g., "github.repo")
            default: Default value if key not found

        Returns:
            Configuration value or default

        Example:
            config.get("github.repo") -> "username/repo"
            config.get("linear.team_id") -> "TEAM-ABC"
        """
        if self._config is None:
            self.load()

        keys = key_path.split('.')
        value = self._config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def get_env_token(self, service: str) -> Optional[str]:
        """
        Get authentication token from environment.

        Args:
            service: Service name ("github" or "linear")

        Returns:
            Token string or None if not set
        """
        if service == "github":
            # First try GITHUB_TOKEN
            token = os.getenv("GITHUB_TOKEN")
            if token:
                return token
            # Try alternative names
            return os.getenv("GH_TOKEN")

        elif service == "linear":
            # First try LINEAR_API_KEY
            token = os.getenv("LINEAR_API_KEY")
            if token:
                return token
            # Try alternative names
            return os.getenv("LINEAR_TOKEN")

        else:
            raise ValueError(f"Unknown service: {service}")

    def validate(self) -> tuple[bool, list[str]]:
        """
        Validate configuration.

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        try:
            if not self._config:
                self.load()
        except Exception as e:
            return False, [f"Failed to load config: {e}"]

        # Check required fields
        required_fields = [
            ("github.repo", "GitHub repository (e.g., 'username/repo')"),
            ("linear.workspace", "Linear workspace name"),
            ("linear.team_id", "Linear team ID")
        ]

        for field, description in required_fields:
            if self.get(field) is None:
                errors.append(f"Missing {description}: {field}")

        # Check environment tokens
        if not self.get_env_token("github"):
            errors.append("GitHub token not set in environment (GITHUB_TOKEN)")

        if not self.get_env_token("linear"):
            errors.append("Linear API key not set in environment (LINEAR_API_KEY)")

        return len(errors) == 0, errors