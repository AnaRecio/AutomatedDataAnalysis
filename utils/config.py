import os
from dotenv import load_dotenv

# Debug logging
print("[DEBUG] Config file: Loading environment variables...")
print("[DEBUG] Config file: Current directory:", os.getcwd())
print("[DEBUG] Config file: .env file exists:", os.path.exists('.env'))
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        print("[DEBUG] Config file: .env contents:", f.read().strip())

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print("[DEBUG] Config file: OPENAI_API_KEY loaded:", bool(OPENAI_API_KEY))
if OPENAI_API_KEY:
    print("[DEBUG] Config file: API Key starts with:", OPENAI_API_KEY[:6])
