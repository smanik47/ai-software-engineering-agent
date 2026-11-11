
from types import SimpleNamespace
from unittest.mock import Mock

from backend.llm.llm_client import LLMClient


def test_generate_response():

    fake_client = Mock()

    fake_client.responses.create.return_value = SimpleNamespace(

        output_text="Dependency Injection is a design pattern.",

        model="test-model",

        usage=SimpleNamespace(
            input_tokens=20,
            output_tokens=15,
            total_tokens=35
        )
    )

    llm = LLMClient(
        client=fake_client,
        model="test-model"
    )

    result = llm.generate_response(
        "Explain dependency injection"
    )

    assert result["answer"] == (
        "Dependency Injection is a design pattern."
    )

    assert result["input_tokens"] == 20

    assert result["output_tokens"] == 15

    assert result["total_tokens"] == 35

    fake_client.responses.create.assert_called_once()
