
from openai import OpenAI

from backend.config import settings


class LLMClient:

    def __init__(self, client=None, model=None):

        if client is None:

            if not settings.OPENAI_API_KEY:
                raise ValueError(
                    "OPENAI_API_KEY is not configured"
                )

            client = OpenAI(
                api_key=settings.OPENAI_API_KEY,
                timeout=settings.LLM_TIMEOUT,
                max_retries=settings.MAX_RETRIES
            )

        self.client = client

        self.model = model or settings.OPENAI_MODEL

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


    def get_agent_decision(
            self,
            user_input,
            observation,
            decision_schema,
            instructions
    ):

        prompt = f"""
        USER TASK:
        {user_input}
    
        PREVIOUS OBSERVATION:
        {observation}
    
        Based on the user task and observation,
        decide the next action.
        """

        return self.generate_structured_response(
            user_input=prompt,
            response_schema=decision_schema,
            instructions=instructions
        )


    def generate_structured_response(
            self,
            user_input,
            response_schema,
            instructions=None
    ):

        response = self.client.responses.parse(

            model=self.model,

            instructions=instructions or
                         "Return a structured response.",

            input=user_input,

            text_format=response_schema
        )

        return {
            "data": response.output_parsed,

            "model": response.model,

            "input_tokens": response.usage.input_tokens,

            "output_tokens": response.usage.output_tokens
        }



