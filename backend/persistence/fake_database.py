from logging import exception
import time
from models import Criteria
from persistence.database_service import DatabaseService
import threading


class Database:
    def __init__(self):
        self._database_service = DatabaseService()
        self._table_data = self._database_service.load_table_data()
        self._table_data_updated = False
        self._persist_thread = threading.Thread(target=self._background_persist_data)
        self._persist_thread.start()


    def set_criteria(self, criteria: Criteria):
        self._table_data['criteria'] = criteria
        self._table_data_updated = True

    def get_criteria(self):
        return self._table_data.get('criteria')


    def set_experience(self, exp: str):
        self._table_data['experience'] = exp
        self._table_data_updated = True

    def get_experience(self):
        return self._table_data.get('experience')
    

    def create_thread(self, title: str, url: str, comments_dict):
        if 'threads' not in self._table_data:
            self._table_data['threads'] = {}
        self._table_data['threads'][url] = {'title': title , 'comments': comments_dict}
        self._table_data_updated = True

    def get_all_threads(self):
        return self._table_data.get('threads', {})

    def get_thread_by_url(self, url: str):
        return self._table_data.get('threads')[url]
    

    def update_threads_comment(self, url: str, comment_id: str, data):
        if url in self._table_data['threads']:
            if 'comments' not in self._table_data['threads'][url]:
                self._table_data['threads'][url]['comments'] = {}
            self._table_data['threads'][url]['comments'][comment_id].update(data)
        else:
            print(f'[ERROR] | thread id {url} not found...')
            print("table data =  ", self._table_data)

        self._table_data_updated = True


    def get_thread_comment(self, url: str, comment_id: str):
        return self._table_data.get(url)['comments'][comment_id]['text']
    

    def _background_persist_data(self):
        while True:
            self._persist_data()
            time.sleep(2)

            
    def _persist_data(self):
        if self._table_data_updated:
            print(f"Persisting table to db...")
            for key, value in self._table_data.items():
                self._table_data = self._database_service.create_or_update_table(key, value)
                self._table_data_updated = False


