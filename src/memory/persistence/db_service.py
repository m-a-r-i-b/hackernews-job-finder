import json
from typing import Union

from aiohttp import ClientError
from memory.blackboard.BlackboardData import BlackBoardData
from dataclasses import asdict
import os

from enum import Enum


class OperationMode(str, Enum):
    File = "File"
    DB = "DB"

    def __str__(self) -> str:
        return str.__str__(self)


class Persistence:
    def __init__(self, db_connection):
        self.operation_mode = OperationMode.File

        if self.operation_mode == OperationMode.DB:
            self.table = db_connection.Table(os.getenv("BLACKBOARD_TABLE"))

        self.filename = "data.json"

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

        elif self.operation_mode == OperationMode.DB:
            try:
                response = self.table.get_item(Key={"project_id": project_id})
                if "Item" in response:
                    return response["Item"]
                else:
                    return None
            except ClientError as e:
                print(e.response["Error"]["Message"])
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

        elif self.operation_mode == OperationMode.DB:
            try:
                project_data_dict = asdict(project_data)
                self.table.put_item(
                    Item={"project_id": project_id, **project_data_dict}
                )
                return project_data_dict
            except ClientError as e:
                print(e.response["Error"]["Message"])
                return None
