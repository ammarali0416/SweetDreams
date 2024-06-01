from pydantic import BaseModel
from typing import List, Optional, Dict

class Message(BaseModel):
    role: str
    content: str
    thread_id: Optional[str] = None

class OutlineCompleteMessage(Message):
    status: str
    outline: Dict

class Choice(BaseModel):
    index: int
    message: Message
    logprobs: Optional[Dict] = None
    finish_reason: str

class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ChatCompletion(BaseModel):
    id: str
    object: str
    created: int
    model: str
    system_fingerprint: str
    choices: Choice
    usage: Usage

class Thread(BaseModel):
    id: str
    object: str
    created_at: int
    metadata: Optional[Dict] = None

class ThreadMessageContent(BaseModel):
    type: str
    text: Dict[str, List]

class ThreadMessage(BaseModel):
    id: str
    object: str
    created_at: int
    thread_id: str
    role: str
    content: List[ThreadMessageContent]
    assistant_id: str
    run_id: str
    attachments: Optional[List] = None
    metadata: Optional[Dict] = None