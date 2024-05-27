from __openai.utils import OpenAIBase
from __openai.planning import BookPlanner
from models.openai import (
    Message,
    ChatCompletion,
    Choice,
    Usage
)
from config import settings
import asyncio

# Unit test to check if the OpenAIBase class is correctly implemented with Pydantic models
def test_openai_base():
    # Arrange
    openai_base = OpenAIBase(settings.openai_api_key)

    messages = [
        Message(role="system", content="Hello, how can I help you today?"),
        Message(role="user", content="I want to book a flight.")
    ]

    # Act
    response = openai_base.send_chat_completion(messages)

    print(response)

def test_openai_bookplanner():
    # Arrange
    book_planner = BookPlanner(settings.openai_api_key, settings.openai_assistant_id)

    # Act
    thread_id = book_planner.get_thread()
    print(thread_id)

    message = Message(role="user", content="I am running unit tests on you, please output a complete book plan.")

    reply = book_planner.handle_chat_interaction(message)

    print(reply.content)

    message = Message(role="user", content="Approved.")

    reply = book_planner.handle_chat_interaction(message)

    print(reply.content)

    bookPlan = book_planner.get_book_plan()

    print('this is the book plan', bookPlan)
    

    

print("Running test_openai_bookplanner()...")
test_openai_bookplanner()
