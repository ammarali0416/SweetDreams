from openai import OpenAI
from typing import List
from models.messages import (
    Message,
    OpenAIChatCompletionResponse,
    OpenAIChoice,
    OpenAIUsage
)

class OpenAIBase:
    def __init__(self, api_key: str):
        self.openai = OpenAI(api_key = api_key)

    async def send_chat_completion(self, messages: List[Message], model: str = "gpt-4o", **kwargs):
        response = self.openai.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )

        # Ensure the response is a dictionary
        returned_msg: Message = Message(role=response.choices[0].message.role,
                                        content=response.choices[0].message.content)

        choice: OpenAIChoice = OpenAIChoice(index=response.choices[0].index,
                                            message=returned_msg,
                                            logprobs=response.choices[0].logprobs,
                                            finish_reason=response.choices[0].finish_reason)
        
        usage: OpenAIUsage = OpenAIUsage(prompt_tokens=response.usage.prompt_tokens,
                                        completion_tokens=response.usage.completion_tokens,
                                        total_tokens=response.usage.total_tokens)
        
        return OpenAIChatCompletionResponse(id=str(response.id),
                                            object=str(response.object),
                                            created=int(response.created),
                                            model=str(response.model),
                                            system_fingerprint=str(response.system_fingerprint),
                                            choices=choice,
                                            usage=usage)
