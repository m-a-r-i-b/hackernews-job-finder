import json
from dataclasses import asdict


class DatabaseService:
    def __init__(self):
        self.filename = "data.json"

    def load_project(self, project_id: str):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                if data:
                    return data.get(project_id, None)
                else:
                    return None
        except (FileNotFoundError, json.JSONDecodeError):
            return None


    def create_or_update_project(self, project_id: str, project_data):
        try:
            with open(self.filename, "r") as file:
                all_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            all_data = {}

        with open(self.filename, "w") as file:
            all_data[project_id] = project_data
            json.dump(all_data, file)
            return all_data[project_id]
