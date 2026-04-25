import base64
import os
import secrets
from dotenv import load_dotenv

load_dotenv()

DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID", "")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET", "")
DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI", "http://localhost:8080/api/auth/callback")

# Session secret needs to be 32 url-safe base64-encoded bytes
_session_secret_env = os.getenv("SESSION_SECRET")
if _session_secret_env:
    SESSION_SECRET = _session_secret_env.encode('utf-8')
else:
    # Generate one for dev if not provided
    SESSION_SECRET = base64.urlsafe_b64encode(secrets.token_bytes(32))

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "roku")
FRONTEND_URLS = [
    "http://localhost:5173",
    "https://beta.rokubot.com",
    "https://rokubot.com",
    "http://localhost:8080"
]
