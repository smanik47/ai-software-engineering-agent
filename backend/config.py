
import os

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Settings:

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Keep model configurable rather than hardcoding it.
    OPENAI_MODEL = os.getenv(
        "OPENAI_MODEL"
    )

    LLM_TIMEOUT = 60

    MAX_RETRIES = 2


settings = Settings()
