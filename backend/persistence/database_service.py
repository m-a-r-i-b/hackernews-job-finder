import json
from dataclasses import asdict


EMPTY_TABLE = {'threads': {}}

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
                    return EMPTY_TABLE
        except (FileNotFoundError, json.JSONDecodeError):
            return EMPTY_TABLE


    def create_or_update_table(self, key: str, value):
        try:
            with open(self.filename, "r") as file:
                all_data = json.load(file)
        except FileNotFoundError as e:
            print("[ERROR] | While creating/updating thread, could not find existing file..." , e)
            all_data = EMPTY_TABLE
        except (json.JSONDecodeError) as ej:
            # print("[ERROR] | While creating/updating thread, Json decode error or perhaps an empty file..." , ej)
            all_data = EMPTY_TABLE

        with open(self.filename, "w") as file:
            all_data[key] = value
            json.dump(all_data, file)
            return all_data[key]
