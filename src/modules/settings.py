"""Settings management for EDINET Viewer."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv, set_key


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"


def load_environment() -> None:
    """Load environment variables from the .env file."""
    load_dotenv(ENV_PATH)


def get_edinet_api_key() -> Optional[str]:
    """Return the EDINET API key from environment variables if set."""
    load_environment()
    return os.getenv("EDINET_API_KEY")


def save_edinet_api_key(api_key: str) -> None:
    """Save the EDINET API key to the .env file."""
    load_environment()
    ENV_PATH.touch(exist_ok=True)
    set_key(str(ENV_PATH), "EDINET_API_KEY", api_key)
