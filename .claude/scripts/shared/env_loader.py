"""
Environment loader for mixer-system-v2.
Loads environment variables from .env file.
"""
import os
from pathlib import Path
from dotenv import load_dotenv


def ensure_env_loaded():
    """
    Load environment variables from .env file.
    Looks for .env in the current directory.
    """
    # Try current directory first
    env_path = Path.cwd() / '.env'

    if env_path.exists():
        load_dotenv(env_path)
        return True

    # Try parent directory (in case we're in a subdirectory)
    env_path = Path.cwd().parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        return True

    # Try the mixer-system-v2 root
    # This handles the case where script is run from anywhere
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent
    env_path = project_root / '.env'

    if env_path.exists():
        load_dotenv(env_path)
        return True

    return False


def get_env_var(key: str, default: str = None) -> str:
    """
    Get an environment variable.

    Args:
        key: Environment variable name
        default: Default value if not found

    Returns:
        Environment variable value or default
    """
    return os.getenv(key, default)