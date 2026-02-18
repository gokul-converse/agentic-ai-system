# import logging

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s | %(levelname)s | %(message)s"
# )

# logger = logging.getLogger("agentic-ai")


# app/utils/logger.py

import logging

from app.config.logging import setup_logging

setup_logging()

logger = logging.getLogger("agentic-ai")
