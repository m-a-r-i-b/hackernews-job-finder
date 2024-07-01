import copy
import json
from logging import exception
from memory.blackboard.BlackboardData import BlackBoardData, State
from memory.persistence.db_service import Persistence
from const import Step
from typing import List, Dict, Any
import copy


class BlackBoard:
    def __init__(self, project_id):
        self._data: BlackBoardData
        self.persistence_service = Persistence()
        self.project_id = project_id
        self._read_or_create_project()

        

    def _read_or_create_project(self):
        try:
            project_data = self.persistence_service.load_project(self.project_id)
            if project_data is None or not project_data:
                print("Creating new project...")
                project_data = self.persistence_service.create_or_update_project(
                    self.project_id, BlackBoardData()
                )

            blackboard_data = BlackBoardData.from_json(project_data)
            self._data = blackboard_data
            return self._data
        except exception:
            pass

    def _persist_data_to_database(self, data: BlackBoardData):
        new_json_data = self.persistence_service.create_or_update_project(
            self.project_id, data
        )
        blackboard_data = BlackBoardData.from_json(new_json_data)
        self._data = blackboard_data

    def get_data(self) -> BlackBoardData:
        return copy.deepcopy(self._data)

    def get_information(self, step: Step):
        data = self.get_data()
        step_info = data.information.get(step, {})
        if isinstance(step_info, dict):
            return step_info
        else:
            return json.loads(step_info)

    def get_completed_steps(self) -> List[Step]:
        state_history = self.get_data().state_history
        completed_steps = [state["step"] for state in state_history]
        return completed_steps


    def update_information(self, step_information: Dict[str, Any], step: Step = None):
        data = self.get_data()
        if step is None:
            step = data.state.step
      
        data.information[step] = step_information
        self._persist_data_to_database(data)

    def update_state(self, new_state: State):
        data = self.get_data()
        curr_state = copy.deepcopy(data.state)
        data.state_history.append(curr_state)
        data.state = new_state
        self._persist_data_to_database(data)

