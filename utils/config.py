# utils/config.py

import os
from dotenv import load_dotenv

# Optional debug flag for logging during development
DEBUG = True

# Load environment variables from .env file
if DEBUG:
    print("[DEBUG] Config: Loading environment variables from .env...")

load_dotenv()

# Load API keys from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Debug logging to confirm API keys were loaded
if DEBUG:
    print("[DEBUG] OPENAI_API_KEY loaded:", bool(OPENAI_API_KEY))
    print("[DEBUG] SERPER_API_KEY loaded:", bool(SERPER_API_KEY))
    if OPENAI_API_KEY:
        print("[DEBUG] OPENAI_API_KEY starts with:", OPENAI_API_KEY[:8])
    if SERPER_API_KEY:
        print("[DEBUG] SERPER_API_KEY starts with:", SERPER_API_KEY[:8])

# Ensure that required API keys are set; fail fast otherwise
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")
if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY not found in environment variables.")

