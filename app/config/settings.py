import logging
import os

import logfire
from dotenv import load_dotenv

load_dotenv()

SETUP = os.getenv("SETUP")

logfire.configure(
    environment=SETUP
)

logging.basicConfig(
    level=logging.INFO,
    handlers=[logfire.LogfireLoggingHandler()]
)

logger = logging.getLogger()