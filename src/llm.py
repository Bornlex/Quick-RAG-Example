import os
from groq import Groq
from dotenv import load_dotenv


load_dotenv()


class GroqClient:
    def __init__(self):
        self._api_key = os.getenv('GROQ_API_KEY')
        self._model = os.getenv('GROQ_MODEL')
        self._client = Groq(api_key=self._api_key)

    def completion(self, content: str) -> str:
        response = self._client.chat.completions.create(
            messages=[{
                'role': 'user',
                'content': content
            }],
            model=self._model
        )
        return response.choices[0].message.content
