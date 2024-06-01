from .utils import OpenAIBase
from models.openai import Message, Thread
from typing import Optional
import time
import json

class BookPlanner(OpenAIBase):
    def __init__(self, api_key: str, assistant_id: str, thread_id: Optional[str] = None):
        super().__init__(api_key)
        self.thread_id: Optional[str] = thread_id
        self.myThread: Optional[Thread] = None
        self.assistant_id = assistant_id

    def get_thread(self) -> str: # Thread ID
        if not self.myThread and not self.thread_id:
            new_thread = self.openai.beta.threads.create()
            print(f"New thread created with ID: {new_thread.id}")
            self.myThread = Thread(id=new_thread.id,
                                   object=new_thread.object,
                                   created_at=new_thread.created_at,
                                   metadata=new_thread.metadata)
            self.thread_id = self.myThread.id
        elif self.thread_id:
            new_thread = self.openai.beta.threads.retrieve(self.thread_id)
            print(f"Thread retrieved with ID: {new_thread.id}")
            self.myThread = Thread(id=new_thread.id,
                                   object=new_thread.object,
                                   created_at=new_thread.created_at,
                                   metadata=new_thread.metadata)
            self.thread_id = self.myThread.id
        return self.myThread.id

    def add_user_message(self, message: Message) -> None:
        #print(f"Adding user message: {message}")
        response = self.openai.beta.threads.messages.create(thread_id=self.myThread.id, role=message.role, content=message.content)
        #print(response)

    def get_bot_reply(self) -> Message:
        #print('Creating run..')
        myRun = self.openai.beta.threads.runs.create(thread_id=self.myThread.id, assistant_id=self.assistant_id)  # Replace with actual assistant_id
        #print(f"Run ID: {myRun.id}")

        keepRetrievingRun = None
        while myRun.status in ["queued", "in_progress"]:
            keepRetrievingRun = self.openai.beta.threads.runs.retrieve(thread_id=self.thread_id, run_id=myRun.id)
            if keepRetrievingRun.status == "completed":
                #print("\n")
                allMessages = self.openai.beta.threads.messages.list(thread_id=self.thread_id)
                bot_msg = Message(role=allMessages.data[0].role,
                                  content=allMessages.data[0].content[0].text.value,
                                  thread_id=self.thread_id)
                return bot_msg
            elif keepRetrievingRun.status in ["queued", "in_progress"]:
                time.sleep(1)
            else:
                #print(f"Run status: {keepRetrievingRun.status}")
                break

    def handle_chat_interaction(self, user_message: Message) -> Message:
        self.add_user_message(message=user_message)
        bot_reply = self.get_bot_reply()
        return bot_reply

    def get_book_plan(self) -> Optional[dict]:
        messages = self.openai.beta.threads.messages.list(self.thread_id)
        assistantMessages = [msg for msg in messages.data if msg.role == 'assistant']

        for message in assistantMessages:
            text = message.content[0].text.value
            startIndex = text.find('{')
            endIndex = text.rfind('}')

            if startIndex != -1 and endIndex != -1:
                jsonString = text[startIndex:endIndex + 1]
                try:
                    potentialBookPlan = json.loads(jsonString)
                    if 'bookPlan' in potentialBookPlan and 'title' in potentialBookPlan['bookPlan']:
                        return potentialBookPlan
                except json.JSONDecodeError as error:
                    print("Error parsing potential book plan JSON:", error)
        print("No book plan found in the conversation.")
        return None
