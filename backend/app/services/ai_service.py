from openai import OpenAI
from app.config import settings


def test_openai_connection():
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is missing from .env")

    client = OpenAI(
        api_key=settings.OPENAI_API_KEY,
        timeout=20.0,
        max_retries=1,
    )

    response = client.responses.create(
        model=settings.OPENAI_MODEL,
        instructions="You are a helpful AI assistant.",
        input="Reply with exactly: VoxCare AI connected successfully.",
        max_output_tokens=50,
    )

    return response.output_text