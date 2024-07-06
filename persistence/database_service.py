import json
from dataclasses import asdict


class DatabaseService:
    def __init__(self):
        self.filename = "data.json"

    def load_table_data(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                if data:
                    print("Table data exists...")
                    return data
                else:
                    print("Table data does not exist, returning empty {}...")
                    return {}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}


    def create_or_update_thread(self, thread_url: str, thread_data):
        try:
            with open(self.filename, "r") as file:
                all_data = json.load(file)
        except FileNotFoundError as e:
            print("[ERROR] | While creating/updating thread, could not find existing file..." , e)
            all_data = {}
        except (json.JSONDecodeError) as ej:
            print("[ERROR] | While creating/updating thread, Json decode error..." , e)
            all_data = {}

        with open(self.filename, "w") as file:
            all_data[thread_url] = thread_data
            json.dump(all_data, file)
            return all_data[thread_url]
