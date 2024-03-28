import os
from typing import Tuple, Union
from dotenv import load_dotenv
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient

from src import utils


class ClientWrapper:
    def __init__(self):
        load_dotenv()
        self._mongo_database = "marchespublics"
        self._consultations_collection = 'consultations'
        self._mongo_user = os.getenv('MONGO_USER')
        self._mongo_pass = os.getenv('MONGO_PASS')
        self._mongo_host = os.getenv('MONGO_HOST')
        self._mongo_name = os.getenv('MONGO_NAME')
        self._limit = int(os.getenv('MONGO_LIMIT'))
        self._mongo_uri = f'mongodb+srv://{self._mongo_user}:{self._mongo_pass}@{self._mongo_host}?retryWrites=true&w=majority&appName={self._mongo_name}'

    def _get_client(self):
        return MongoClient(self._mongo_uri, server_api=ServerApi('1'))

    def _clean(self, documents):
        results = []
        for d in documents:
            if '_id' in d:
                del d['_id']
            if 'vector' in d:
                del d['vector']
            results.append(d)
        return results

    def _search_text(self, query: str) -> list:
        processed = f'.*{query}.*'
        client = self._get_client()
        raw_results = client[self._mongo_database][self._consultations_collection].find({
            'objet': {
                '$regex': processed
            }
        }).limit(self._limit)

        results = self._clean(raw_results)
        client.close()

        return results

    def _search_vector(self, query: list[float]) -> list:
        client = self._get_client()
        raw_results = client[self._mongo_database][self._consultations_collection].aggregate([{
            '$vectorSearch': {
                'index': 'vectorindex',
                'path': 'vector',
                'queryVector': query,
                'numCandidates': 150,
                'limit': self._limit
            }
        }, {
            '$set': {
                'score': {
                    '$meta': 'vectorSearchScore'
                }
            }
        }, {
            '$unset': '_id'
        }])

        results = self._clean(raw_results)
        client.close()

        return results

    def search(self, query: Union[str, list[float]], method: str = 'text') -> list:
        if method == utils.SearchParameters.vector_method:
            return self._search_vector(query)
        else:
            return self._search_text(query)

    def ping(self) -> Tuple[bool, str]:
        client = self._get_client()
        try:
            client.admin.command('ping')
            return True, ""
        except Exception as e:
            return False, utils.format_exception(e)
        finally:
            client.close()

    def _update_document(self, procedure_id: str, document_update: dict) -> int:
        client = self._get_client()
        result = client[self._mongo_database][self._consultations_collection].update_one(
            {'id': procedure_id},
            {'$set': document_update}
        )
        return result.modified_count

    def update_vector(self, procedure_id: str, vector: list) -> int:
        return self._update_document(procedure_id, {'vector': vector})


if __name__ == '__main__':
    c = ClientWrapper()
    print('.success' if c.ping() else '.failed')
    r = c.search("Ascenseur")
    print([x for x in r])
