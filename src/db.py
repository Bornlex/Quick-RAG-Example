import os
from typing import Tuple
from dotenv import load_dotenv
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient


class ClientWrapper:
    def __init__(self):
        load_dotenv()
        self._mongo_database = "marchespublics"
        self._consultations_collection = 'consultations'
        self._mongo_user = os.getenv('MONGO_USER')
        self._mongo_pass = os.getenv('MONGO_PASS')
        self._mongo_host = os.getenv('MONGO_HOST')
        self._mongo_name = os.getenv('MONGO_NAME')
        self._limit = os.getenv('MONGO_LIMIT')
        self._mongo_uri = f'mongodb+srv://{self._mongo_user}:{self._mongo_pass}@{self._mongo_host}?retryWrites=true&w=majority&appName={self._mongo_name}'

    def _get_client(self):
        return MongoClient(self._mongo_uri, server_api=ServerApi('1'))

    def search(self, query: str) -> list:
        processed = f'.*{query}.*'
        client = self._get_client()
        raw_results = client[self._mongo_database][self._consultations_collection].find({
            'objet': {
                '$regex': processed
            }
        }).limit(30)
        results = []
        for r in raw_results:
            del r['_id']
            results.append(r)

        client.close()
        return results

    def ping(self) -> Tuple[bool, str]:
        client = self._get_client()
        try:
            client.admin.command('ping')
            return True, ""
        except Exception as e:
            return False, f"{type(e).__name__}: {str(e)}"
        finally:
            client.close()


if __name__ == '__main__':
    c = ClientWrapper()
    print('.success' if c.ping() else '.failed')
    r = c.search("Ascenseur")
    print([x for x in r])
