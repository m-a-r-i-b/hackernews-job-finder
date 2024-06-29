# from dotenv import load_dotenv
# load_dotenv(".env")

# from criteria_filter import criteria_filter


import json
from agents.base.SmartAgentOutput import SmartAgentOutput
from const.mappings import LONG_RUNNING_STEPS, Step
from memory.blackboard.Blackboard import BlackBoard
from agents.base.SmartAgentOutput import SmartAgentObservation
from agents.base.Agent import Agent
from memory.blackboard.BlackboardData import State
from agents.type_classifier.agent import TypeClassifierAgent
from agents.feature_identification.agent import (
    FeatureIdentificationAgent,
)
from agents.required_value_identification.agent import (
    RequiredValueIdentificationAgent,
)
from agents.step_planner.agent import StepPlannerAgent
from agents.smart_contract_developer.agent import SmartContractDeveloperAgent
from agents.dumb.project_parked.agent import ProjectParkedAgent
from typing import List
import random

from agents.smart_contract_updater.agent import SmartContractUpdaterAgent
from agents.dumb.commit.agent import CommitAgent
from agents.smart_contract_deployment.agent import SmartContractDeploymentAgent


class ProjectManager:
    def __init__(self, db_connection):
        self.blackboard = BlackBoard(db_connection)
        self.STEP_TO_AGENT_MAPPING = {
            Step.Type_Classification: TypeClassifierAgent,
            Step.Next_Step_Planner: StepPlannerAgent,
            Step.Smartcontract_Development: SmartContractDeveloperAgent,
            Step.Project_Parked: ProjectParkedAgent,
            Step.Update_Smartcontract_Development: SmartContractUpdaterAgent,
            Step.Commit: CommitAgent,
            Step.Smartcontract_Deployment: SmartContractDeploymentAgent
        }

    def _initalize_project(self, project_id: str):
        self.blackboard._initialize_blackboard(project_id)

    def _get_current_step(self) -> Step:
        return self.blackboard.get_data().state.step

    def _get_current_state(self) -> State:
        return self.blackboard.get_data().state

    def _get_current_step_index(self) -> int:
        return self.blackboard.get_data().state.curr_step_index

    def _get_development_sequence(self) -> List[Step]:
        return self.blackboard.get_data().development_sequence

    def _move_to_next_step(self) -> Step:
        curr_step_index = self._get_current_step_index()
        next_step_index = curr_step_index + 1
        print("curr_step_index = ",curr_step_index)

        development_sequence = self._get_development_sequence()
        print("development_sequence = ",development_sequence)

        next_step = development_sequence[next_step_index]

        print("next_step = ",next_step)

        self.blackboard.update_state(State(step=next_step, curr_step_index=next_step_index, interactable=False))
        return next_step
        # Update state & state history

    def _initalize_agent_for_step(self, step) -> Agent:
        agent = self.STEP_TO_AGENT_MAPPING[step]
        return agent(self.blackboard)


    def _perform_post_step_specific_actions(self, finished_step: Step, output: SmartAgentOutput):

        is_project_parked = False
        data = json.loads(output.data.json())
        print("Data = ",data)

        if finished_step == Step.Next_Step_Planner:
            next_steps = data["next_steps"]
            next_steps.append(Step.Project_Parked)
            self.blackboard.append_development_sequence(next_steps)

        if finished_step == Step.Project_Parked:
            is_project_parked = True
            self.blackboard.append_development_sequence([Step.Next_Step_Planner])
            
        return is_project_parked
    



    def on_msg(self, user_msg, project_id):
        self._initalize_project(project_id)
        curr_state = self._get_current_state()
        curr_step = curr_state.step
        is_project_interactable = curr_state.interactable

        session_id = random.randint(100000, 999999)
        user_id = "marib"

        # TODO
        # Perhaps also add check about what mode project_manager is running in (receptionist or worker?)
        # Because if it's in worker mode, it should not be able to continue on long running step
        # if curr_step in LONG_RUNNING_STEPS:
        #     # TODO send some error code, so end-user is given a pop-up with this msg, instead of msg appearing in convo
        #     return f"We are still working on {curr_step}, please wait..."

        if not is_project_interactable:
            return "Please wait while we process your project..."

        current_observation: SmartAgentObservation = None
        is_project_parked = False

        self.blackboard.update_interaction_status(False)

        try:
            while (current_observation != SmartAgentObservation.TAKE_USER_INPUT) and (not is_project_parked):

                # TODO implement long running step
                # if curr_step in LONG_RUNNING_STEPS:
                #     self._submit_long_running_job()
                #     return "Alright, now hold tight while we do the work for you"

                agent = self._initalize_agent_for_step(curr_step)
                output: SmartAgentOutput = agent.run(
                    user_msg, user_id, project_id, session_id
                )
                current_observation = output.observation

                if current_observation == SmartAgentObservation.STEP_COMPLETED:
                    is_project_parked = self._perform_post_step_specific_actions(curr_step, output)
                    curr_step = self._move_to_next_step()
                    print("should exit loop = ",is_project_parked)
                    print("Not of exit loop = ", (not is_project_parked))

                    print("=====================================")
        finally:
            self.blackboard.update_interaction_status(True)

        return output.data.message
