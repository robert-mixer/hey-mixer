"""
Simple logger for mixer-system-v2.
"""
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class MixerLogger:
    """Simple logger for mixer operations."""

    def __init__(self, project_root: Optional[Path] = None, agent_name: str = "mixer"):
        """
        Initialize logger.

        Args:
            project_root: Project root directory
            agent_name: Name of the agent using the logger
        """
        self.project_root = project_root or Path.cwd()
        self.agent_name = agent_name
        self.verbose = "--verbose" in sys.argv

    def _timestamp(self) -> str:
        """Get current timestamp."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def info(self, message: str):
        """Log info message (only if verbose)."""
        if self.verbose:
            print(f"[{self._timestamp()}] INFO ({self.agent_name}): {message}")

    def error(self, message: str):
        """Log error message (always shown)."""
        print(f"[{self._timestamp()}] ERROR ({self.agent_name}): {message}", file=sys.stderr)

    def warning(self, message: str):
        """Log warning message (always shown)."""
        print(f"[{self._timestamp()}] WARNING ({self.agent_name}): {message}")

    def debug(self, message: str):
        """Log debug message (only if verbose)."""
        if self.verbose:
            print(f"[{self._timestamp()}] DEBUG ({self.agent_name}): {message}")

    def log_api_call(self, service: str, operation: str, status: str):
        """
        Log API call (only if verbose).

        Args:
            service: Service name (github, linear)
            operation: Operation performed
            status: Status (success, error)
        """
        if self.verbose:
            print(f"[{self._timestamp()}] API ({self.agent_name}): {service}.{operation} -> {status}")