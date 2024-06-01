from __openai.planning import BookPlanner
from __openai.outlining import OutlineGenerator
from models.openai import (
    Message,
    OutlineCompleteMessage,
    ChatCompletion,
    Choice,
    Usage
)

from typing import Optional, Union, List, Dict
from config import settings

def planning_convo(user_message: Message, thread_id: Optional[str] = None) -> Union[Message, OutlineCompleteMessage]:
    # Thread ID is used to continue the conversation in the existing thread and is optionally sent by the client.
    if not thread_id: # If there is no thread_id, create a new thread. New conversations with the user will be created as new threads.
        book_planner = BookPlanner(api_key=settings.openai_api_key, assistant_id=settings.openai_assistant_id)
    else: # If there is a thread_id, continue the conversation in the existing thread.
        book_planner = BookPlanner(api_key=settings.openai_api_key, assistant_id=settings.openai_assistant_id, thread_id=thread_id)
    # Ensure the book_planner is initialized with the correct thread_id
    thread_id = book_planner.get_thread()

    # Handle the chat interaction with the user
    bot_reply = book_planner.handle_chat_interaction(user_message)

    # If the bot reply is a complete outline, return the outline
    if '"status": "Summary Complete"' in bot_reply.content:
        outline = book_planner.get_book_plan()
        return OutlineCompleteMessage(role=bot_reply.role, content=bot_reply.content, thread_id=bot_reply.thread_id, status="Summary Complete", outline=outline)
    
    return bot_reply

def generate_chapter_outlines(bookplan_id: int) -> List[Dict]:
    outline_generator = OutlineGenerator(api_key=settings.openai_api_key, bookplan_id=bookplan_id)

    outline_generator.generate(returnvals=False)

    return outline_generator.outline

