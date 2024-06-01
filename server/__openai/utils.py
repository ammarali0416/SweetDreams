from openai import OpenAI
from typing import List
from models.openai import (
    Message,
    ChatCompletion,
    Choice,
    Usage
)

class OpenAIBase:
    def __init__(self, api_key: str):
        self.openai = OpenAI(api_key = api_key)

    def send_chat_completion(self, messages: List[Message], model: str = "gpt-4o", **kwargs) -> ChatCompletion:
        response = self.openai.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )

        returned_msg: Message = Message(role=response.choices[0].message.role,
                                        content=response.choices[0].message.content)

        choice: Choice = Choice(index=response.choices[0].index,
                                            message=returned_msg,
                                            logprobs=response.choices[0].logprobs,
                                            finish_reason=response.choices[0].finish_reason)
        
        usage: Usage = Usage(prompt_tokens=response.usage.prompt_tokens,
                                        completion_tokens=response.usage.completion_tokens,
                                        total_tokens=response.usage.total_tokens)
        
        return ChatCompletion(id=str(response.id),
                              object=str(response.object),
                              created=int(response.created),
                              model=str(response.model),
                              system_fingerprint=str(response.system_fingerprint),
                              choices=choice,
                              usage=usage)
