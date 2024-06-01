
from typing import List, Dict
import json
from sqlmodel import Session
from config import settings

from models.openai import Message, ChatCompletion
from models.database import BookPlan, ChapterOutlines, Chapter

from __openai.utils import OpenAIBase
from __openai.prompts.prompt_writing import systemMessage as AuthorPrompt
from __openai.prompts.prompt_summarizing import systemMessage as SummarizerPrompt

from database.crud import (
    get_bookplan,
    get_chapter_outlines
    )
from database.database import engine

class Summarizer(OpenAIBase):
    def __init__(self, api_key: str):
        super().__init__(api_key)

    def send_chat_completion(self, chapter: str) -> ChatCompletion:
        system_message = SummarizerPrompt.format(chapter=chapter)
        return super().send_chat_completion(
            messages=[
            Message(role="system", content=system_message),
            ],
            model="gpt-3.5-turbo-0125",
            temperature=1,
            max_tokens=4096,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={"type": "text"}
        )

class Author(OpenAIBase):
    def __init__(self, api_key: str, bookplan_id: str):
        super().__init__(api_key)
        self.system_message: str = AuthorPrompt
        self.chapters: List[Chapter] = []
        self.bookplan_id = bookplan_id

    def send_chat_completion(self, message: Message) -> ChatCompletion:
        return super().send_chat_completion(
            messages=[
                Message(role="system", content=self.system_message),
                Message(role="user", content=message.content)
            ],
            temperature=1,
            max_tokens=4096,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={"type": "json_object"}
        )

    def write(self) -> None:
        with Session(engine) as db:
            plan: BookPlan = get_bookplan(db=db, bookplan_id=self.bookplan_id)
            outlines: List[ChapterOutlines] = get_chapter_outlines(db=db, bookplan_id=self.bookplan_id)
        
        prior_summaries = []
        
        for i, chapter_outline in enumerate(outlines):
            print(f"Now writing: Chapter {i + 1}")
            message_content = json.dumps({
                "bookPlan": plan.Book_Plan,
                "chapterOutline": chapter_outline.Chapter_Outline_JSON,
                "priorSummaries": prior_summaries
            })
            print(f"Chapter {i + 1} message: {message_content}")
            
            message = Message(role="user", content=message_content)

            response = self.send_chat_completion(message)
            chapter = Chapter(ChapterOutline_ID=chapter_outline.ChapterOutline_ID, 
                              BookPlan_ID=chapter_outline.BookPlan_ID,
                              Chapter_Num=chapter_outline.Chapter_Num,
                              Chapter=json.loads(response.choices.message.content)['Chapter'])
            self.chapters.append(chapter)
   
            summary = Summarizer(settings.openai_api_key).send_chat_completion(response.choices.message.content)
            summary_text = summary.choices.message.content
            print(f"Chapter {i + 1} Summary: {summary_text}")
            
            summary_key = f"Chapter {i + 1}"
            prior_summaries.append({summary_key: summary_text})
        
