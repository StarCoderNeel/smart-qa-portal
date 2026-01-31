"""Application constants and configuration."""

import os
from pathlib import Path

# Application metadata
APP_VERSION = "0.1.0"
APP_NAME = "Generated Application"
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Paths
BASE_DIR = Path(__file__).parent.parent
SRC_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# API Configuration
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "100"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Database (if applicable)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
