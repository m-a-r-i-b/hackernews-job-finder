import json
from typing import Union
from memory.blackboard.BlackboardData import BlackBoardData
from dataclasses import asdict
from enum import Enum


class OperationMode(str, Enum):
    File = "File"
    DB = "DB"

    def __str__(self) -> str:
        return str.__str__(self)


class Persistence:
    def __init__(self):
        self.operation_mode = OperationMode.File

        self.filename = "project_state_data.json"

    def load_project(self, project_id: str) -> Union[BlackBoardData, None]:
        if self.operation_mode == OperationMode.File:
            try:
                with open(self.filename, "r") as file:
                    data = json.load(file)
                    if data:
                        return data.get(project_id, None)
                    else:
                        return None
            except (FileNotFoundError, json.JSONDecodeError):
                return None


    def create_or_update_project(
        self, project_id: str, project_data: BlackBoardData
    ) -> BlackBoardData:
        if self.operation_mode == OperationMode.File:
            try:
                with open(self.filename, "r") as file:
                    all_data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                all_data = {}

            with open(self.filename, "w") as file:
                project_data_dict = asdict(project_data)
                # project_data_json_string = json.dumps(project_data_dict)
                all_data[project_id] = project_data_dict
                json.dump(all_data, file)
                return all_data[project_id]
