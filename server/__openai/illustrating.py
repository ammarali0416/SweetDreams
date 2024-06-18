from typing import List, Dict, Tuple
import ast
from sqlmodel import Session
from config import settings

from models.openai import Message, ChatCompletion
from models.database import BookPlan

from __openai.utils import OpenAIBase
from __openai.prompts.prompt_illustrations import (
    guidelines,
    chapters_images,
    cover
)

from database.crud import get_illustration_context, get_bookplan
from database.database import engine

class Illustrator(OpenAIBase):
    def __init__(self, api_key: str, bookplan_id: int):
        super().__init__(api_key)
        self.bookplan_id: int = bookplan_id
        self.overall_context: str = None
        self.character_context: str = None
        self.chapter_contexts: List[Tuple[int, str, str]] = []
        self.plot: str = None

        self.overall_prompt: str = None
        self.cover_prompt: str = None


    def get_illustration_details(self) -> None:
        with Session(engine) as session:
            overall_context, character_context, chapter_contexts  = get_illustration_context(session, self.bookplan_id)
            self.overall_context = overall_context
            self.character_context = character_context
            self.chapter_contexts = chapter_contexts
            book_plan: BookPlan = get_bookplan(session, self.bookplan_id)
        
        book_plan = ast.literal_eval(book_plan.Book_Plan)
        plot = book_plan['bookPlan']['plot']
            

    def overall_style_prompt(self) -> None:
        sys_msg: str = guidelines.format(IllustrativeStyle=self.overall_context, MainCharacters=self.character_context)

        res: ChatCompletion = super().send_chat_completion(
            messages=[
                Message(role="system", content=sys_msg)
            ],
            temperature=1,
            max_tokens=4096,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={"type": "json_object"}
        )

        self.overall_prompt = res.choices.message.content
    
    def cover_style_prompt(self) -> None:
        sys_msg: str = cover.format(OverallStyle=self.overall_prompt, Plot=self.plot)

        res: ChatCompletion = super().send_chat_completion(
            messages=[
                Message(role="system", content=sys_msg)
            ],
            temperature=1,
            max_tokens=4096,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={"type": "text"}
        )

        self.cover_prompt = res.choices.message.content