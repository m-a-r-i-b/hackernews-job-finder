from logging import exception
import time
from models import Criteria
from persistence.database_service import DatabaseService
import threading


class Database:
    def __init__(self):
        self.database_service = DatabaseService()
        self._table_data = self.database_service.load_table_data()
        self._table_data_updated = {}
        self._persist_thread = threading.Thread(target=self._background_persist_data)
        self._persist_thread.start()


    def set_criteria(self, criteria: Criteria):
        self._table_data['criteria'] = criteria
        self._table_data_updated['criteria'] = True

    def get_criteria(self):
        return self._table_data.get('criteria')


    def set_experience(self, exp: str):
        self._table_data['experience'] = exp
        self._table_data_updated['experience'] = True

    def get_experience(self):
        return self._table_data.get('experience')
    

    def create_thread(self, thread_url: str, data):
        self._table_data[thread_url] = data
        self._table_data_updated[thread_url] = True

    def update_thread(self, thread_url: str, data):
        if thread_url in self._table_data:
            # Update existing dictionary with new data
            self._table_data[thread_url].update(data)
        else:
            # If thread_url does not exist, just set it
            self._table_data[thread_url] = data

        self._table_data_updated[thread_url] = True

    def get_thread(self, thread_url: str):
        return self._table_data.get(thread_url)
    

    def update_threads_comment(self, thread_url: str, comment_id: str, data):
        if thread_url in self._table_data:
            self._table_data[thread_url][comment_id].update(data)
        else:
            print('[ERROR] | thread id {thread_url} not found...')
            return

        self._table_data_updated[thread_url] = True

    def get_thread_comment(self, thread_url: str, comment_id: str):
        return self._table_data.get(thread_url)[comment_id]
    

    def _background_persist_data(self):
        while True:
            self._persist_data()
            time.sleep(2)

            
    def _persist_data(self):
        for thread_url, data in self._table_data.items():
            if self._table_data_updated.get(thread_url, False):
                print(f"Updating {thread_url}...")
                self.database_service.create_or_update_thread(thread_url, data)
                self._table_data_updated[thread_url] = False


