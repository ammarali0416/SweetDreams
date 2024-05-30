from fastapi import APIRouter, HTTPException, Depends
from typing import Union, Annotated, List, Dict
from sqlmodel import Session

from models.openai import OutlineCompleteMessage, Message
from models.database import BookPlan, ChapterOutlines

from __openai.service import (
    planning_convo,
    generate_chapter_outlines)

from database.database import get_session

from database.crud import (
    add_bookplan,
    add_chapters)

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
    
@router.get("/chapter_outlines/{thread_id}",
            summary="Get the chapter outlines for a book plan.",
            response_model=list[ChapterOutlines],
            description="Get the chapter outlines for a book plan, using the book plan corresponding with the supplied thread_id.")
def get_chapter_outlines(thread_id: str, db:db_dep) -> List[ChapterOutlines]:
    """
    Get the chapter outlines for a book plan.
    """
    chapter_outlines: List[Dict] = generate_chapter_outlines(thread_id)

    return add_chapters(db=db, thread_id=thread_id, chapters=chapter_outlines)
