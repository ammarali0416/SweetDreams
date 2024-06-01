from __openai.utils import OpenAIBase
from __openai.prompts.prompt_outlining import systemMessage as prompt

from models.openai import Message, ChatCompletion
from models.database import BookPlan

from database.crud import get_bookplan
from database.database import engine

from sqlmodel import Session
from typing import List, Dict

class OutlineGenerator(OpenAIBase):
    def __init__(self, api_key: str, bookplan_id: int):
        super().__init__(api_key)
        self.bookplan_id = bookplan_id
        self.system_message = self.generate_system_message(bookplan_id)
        self.msgArray = [
            Message(role="system", content=self.system_message),
            Message(role="user", content="BEGIN")
        ]
        self.outline: List[Dict] = []
        self.outlineComplete: bool = False

    def generate_system_message(self, bookplan_id: int) -> str:
        with Session(engine) as db:
            book_plan = get_bookplan(db=db, bookplan_id=bookplan_id)
            return prompt + book_plan.Book_Plan

    def send_chat_completion(self) -> ChatCompletion:
        return super().send_chat_completion(self.msgArray, temperature=1, max_tokens=4096, top_p=1, frequency_penalty=0, presence_penalty=0, response_format={'type': "json_object"})

    def generate(self, returnvals: bool = False) -> dict | None:
        while not self.outlineComplete:
            print(self.msgArray[-1])
            response = self.send_chat_completion()
            print(response.usage)
            self.msgArray.append(response.choices.message)
            self.outline.append(response.choices.message.content)

            if "<<OUTLINE COMPLETE>>" in response.choices.message.content:
                print("Outline complete")
                self.outlineComplete = True
            else:
                print("Outline not complete yet")
                self.msgArray.append(Message(role="user", content="NEXT"))

        if returnvals:
            return {"msgArray": self.msgArray, "usage": response.usage}