from __openai.utils import OpenAIBase
from __openai.planning import BookPlanner 
from __openai.outlining import OutlineGenerator

from models.openai import (
    Message,
    ChatCompletion,
    Choice,
    Usage
)
from config import settings
import asyncio

# Unit test to check if the OpenAIBase class is correctly implemented with Pydantic models
def test_openai_base_send_chat_completion():
    # Arrange
    openai_base = OpenAIBase(settings.openai_api_key)

    messages = [
        Message(role="assistant", content="I'm going to take over the world! >:D"),
        Message(role="user", content="Lol why did you say that fam?."),
        Message(role="assistant", content="I'm just kidding, I'm here to help you with your tasks."),
        Message(role="user", content="Oh, okay. Can you help me with my homework?")
    ]

    # Act
    response = openai_base.send_chat_completion(messages)

    assert isinstance(response, ChatCompletion)
    assert isinstance(response.choices, Choice)
    assert isinstance(response.usage, Usage)
    assert isinstance(response.choices.message, Message)
    assert isinstance(response.choices.message.content, str)
    #print(response.choices.message.content)

def test_openai_outlining():
    # Arrange
    outliner = OutlineGenerator(api_key=settings.openai_api_key, thread_id='thread_7ZRKB713hLura3A4K1wx1Rrc')
    
    # Act
    assert outliner.system_message is not None
    assert isinstance(outliner.system_message, str)
    assert len(outliner.msgArray) == 2
    assert outliner.msgArray[0].content == outliner.system_message

    # Act
    outliner.generate(returnvals=True)
    #print(outliner.outline)
    print(type(outliner.outline))
    for outline in outliner.outline:
        print(outline)
    print(type(outliner.outline[0]))
    #print(outliner.system_message)

"""def test_openai_bookplanner():
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

    print('type of book plan', type(bookPlan))
"""
