
from openai import OpenAI

from backend.config import settings


class LLMClient:

    def __init__(self):

        if not settings.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is not configured"
            )

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            timeout=settings.LLM_TIMEOUT,
            max_retries=settings.MAX_RETRIES
        )

        self.model = settings.OPENAI_MODEL

    def generate_response(self, user_input, instructions=None):

        response = self.client.responses.create(

            model=self.model,

            instructions=instructions or
                         "You are a helpful AI assistant.",

            input=user_input
        )

        return {
            "answer": response.output_text,

            "model": response.model,

            "input_tokens": response.usage.input_tokens,

            "output_tokens": response.usage.output_tokens,

            "total_tokens": response.usage.total_tokens
        }
