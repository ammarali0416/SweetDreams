from pydantic import BaseModel
from typing import List, Optional, Dict

class Message(BaseModel):
    role: str
    content: str

class OpenAIChoice(BaseModel):
    index: int
    message: Message
    logprobs: Optional[Dict] = None
    finish_reason: str

class OpenAIUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class OpenAIChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    system_fingerprint: str
    choices: OpenAIChoice
    usage: OpenAIUsage