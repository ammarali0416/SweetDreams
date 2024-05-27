from fastapi import APIRouter, HTTPException, Depends
from typing import Union, Annotated
from sqlmodel import Session

from models.openai import OutlineCompleteMessage, Message
from models.database import BookPlan

from __openai.service import planning_convo
from database.database import get_session
from database.crud import add_bookplan

router = APIRouter(
    prefix="/openai",
    tags=["openai"]
)

db_dep = Annotated[Session, Depends(get_session)]

@router.post("/chat",
             summary="Send a message to the OpenAI editor in chief assistant.",
             response_model= Union[OutlineCompleteMessage, Message],
             description="Send a message to the OpenAI editor in chief assistant.")
def open_ai_assistant_chat(message: Message, db:db_dep) -> Union[OutlineCompleteMessage, Message]:
    """
    Send a message to the OpenAI editor in chief assistant.
    """
    response: Message | OutlineCompleteMessage = planning_convo(user_message= message, thread_id=message.thread_id)
    
    if isinstance(response, OutlineCompleteMessage):
        add_bookplan(db=db, thread_id=response.thread_id, book_plan=str(response.outline))
        return response
    else:
        return response