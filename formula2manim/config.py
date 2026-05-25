"""Central configuration with environment-variable overrides."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DEFAULT_OUTPUT_DIR = Path(os.environ.get("F2M_OUTPUT_DIR", "./outputs"))
DEFAULT_QUALITY = os.environ.get("F2M_QUALITY", "m")
DEFAULT_FPS = int(os.environ.get("F2M_FPS", "30"))
DEFAULT_T_MIN = float(os.environ.get("F2M_T_MIN", "0.0"))
DEFAULT_T_MAX = float(os.environ.get("F2M_T_MAX", "5.0"))
DEFAULT_NUM_POINTS = int(os.environ.get("F2M_NUM_POINTS", "200"))
DEFAULT_AI_MODEL = os.environ.get("F2M_AI_MODEL", "deepseek-chat")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

QUALITY_MAP: dict[str, str] = {
    "l": "480p15",
    "m": "720p30",
    "h": "1080p60",
    "p": "1440p60",
    "k": "2160p60",
}
