from __openai.planning import BookPlanner
from models.openai import (
    Message,
    ChatCompletion,
    Choice,
    Usage
)
from typing import Optional, Union
from config import settings

def planning_convo(user_message: Message, thread_id: Optional[str] = None) -> Message:
    if not thread_id:
        book_planner = BookPlanner(api_key=settings.openai_api_key, assistant_id=settings.openai_assistant_id)
    else:
        book_planner = BookPlanner(api_key=settings.openai_api_key, assistant_id=settings.openai_assistant_id, thread_id=thread_id)
    
    thread_id = book_planner.get_thread()
