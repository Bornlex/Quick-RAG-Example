import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Tuple, Union
from sklearn.metrics.pairwise import cosine_similarity

from src import utils


load_dotenv()


class LLM:
    def __init__(self):
        self._openai_api_key = os.getenv('OPENAI_API_KEY')
        self._model = os.getenv('TOKENIZER_MODEL')
        self._max_length = 256

    def with_client(fn):
        def wrapper(self, *args, **kwargs):
            client = OpenAI()
            client.api_key = self._openai_api_key
            result = fn(self, client, *args, **kwargs)
            del client
            return result

        return wrapper

    def _sim(self, query, documents) -> float:
        query = query[:self._max_length]
        documents = [d[:self._max_length] for d in documents]
        return cosine_similarity([query] * len(documents), documents)[0]

    @with_client
    def get_embeddings(self, client: OpenAI, string: str) -> Tuple[Union[list[float], None], str]:
        try:
            response = client.embeddings.create(
                model=self._model,
                input=string,
                encoding_format='float',
                dimensions=self._max_length
            )
            embeddings = response.data[0].embedding
            return embeddings, ""
        except Exception as e:
            return None, utils.format_exception(e)
