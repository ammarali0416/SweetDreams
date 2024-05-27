from .utils import OpenAIBase

from models.openai import Message, ChatCompletionResponse

class OutlineGenerator(OpenAIBase):
    def __init__(self, api_key: str, system_message_path: str):
        super().__init__(api_key)
        self.system_message = self.generate_system_message(system_message_path)
        self.msgArray = [
            Message(role="system", content=self.system_message),
            Message(role="user", content="BEGIN")
        ]
        self.outline = []
        self.outlineComplete = False

    def generate_system_message(self, path: str) -> str:
        # Implement the logic to read and generate the system message from the given path
        # For now, let's assume it reads a file and returns its content as a string
        with open(path, 'r') as file:
            return file.read()

    async def send_chat_completion(self) -> ChatCompletionResponse:
        return await super().send_chat_completion(self.msgArray, temperature=1, max_tokens=4096, top_p=1, frequency_penalty=0, presence_penalty=0)

    async def generate(self, returnvals: bool = False) -> dict:
        while not self.outlineComplete:
            response = await self.send_chat_completion()
            print(response.usage)
            self.msgArray.append(response.choices[0])
            self.outline.append(response.choices[0].content)

            if "<<OUTLINE COMPLETE>>" in response.choices[0].content:
                print("Outline complete")
                self.outlineComplete = True
            else:
                print("Outline not complete yet")
                self.msgArray.append(Message(role="user", content="NEXT"))

        if returnvals:
            return {"msgArray": self.msgArray, "usage": response.usage}