from __openai.utils import OpenAIBase
from models.messages import (
    Message,
    OpenAIChatCompletionResponse,
    OpenAIChoice,
    OpenAIUsage
)
from config import settings
import asyncio

# Unit test to check if the OpenAIBase class is correctly implemented with Pydantic models

async def test_openai_base():
    # Arrange
    openai_base = OpenAIBase(settings.openai_api_key)

    messages = [
        Message(role="system", content="Hello, how can I help you today?"),
        Message(role="user", content="I want to book a flight.")
    ]

    # Act
    response = await openai_base.send_chat_completion(messages)

    print(response)


# Run the test
asyncio.run(test_openai_base())
