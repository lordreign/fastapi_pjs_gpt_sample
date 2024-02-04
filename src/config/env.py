import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, "..", ".env"))


def check_openai_api_key():
    assert os.getenv("OPENAI_API_KEY") is not None, "OPENAI_API_KEY is not set in .env file"
