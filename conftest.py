"""Tell pytest to look in the python directory for test modules."""

import logging
import sys
from pathlib import Path

logging.raiseExceptions = False

sys.path.insert(0, str(Path(__file__).parent / "python"))
