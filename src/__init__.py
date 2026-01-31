"""Main package initialization and exports."""

import logging

__version__ = "0.1.0"
__author__ = "AI Repository Generator"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

try:
    from .main import app
    __all__ = ['app', '__version__', '__author__']
except ImportError:
    __all__ = ['__version__', '__author__']
