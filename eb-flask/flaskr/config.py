"""Configuration file."""

import os
from pathlib import Path

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = Path.resolve(Path(__file__).parent)
