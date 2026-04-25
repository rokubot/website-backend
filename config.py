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


MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "roku")
FRONTEND_URLS = [
    "http://localhost:5173",
    "https://beta.rokubot.com",
    "https://rokubot.com",
    "http://localhost:8080"
]
