import base64
import os
import secrets
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

PORT = os.getenv("PORT", 8080)
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")


# Session secret needs to be 32 url-safe base64-encoded bytes
SESSION_SECRET = base64.urlsafe_b64decode(os.getenv("SESSION_SECRET"))


DATABASE_URL = os.getenv("DATABASE_URL")
_frontend_urls_env = os.getenv("FRONTEND_URLS")
if _frontend_urls_env:
    FRONTEND_URLS = [url.strip() for url in _frontend_urls_env.split(",") if url.strip()]
else:
    FRONTEND_URLS = [
        "https://beta.rokubot.com",
        "https://rokubot.com",
    ]
