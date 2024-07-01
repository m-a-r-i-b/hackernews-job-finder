# from dotenv import load_dotenv
# load_dotenv(".env")

# from criteria_filter import criteria_filter


import argparse
import json
import os
from typing import List

from dotenv import load_dotenv
from const import Step
from memory.blackboard.Blackboard import BlackBoard
from memory.blackboard.BlackboardData import State
from step_functions.do_filtering import do_filtering
from step_functions.do_scraping import do_scraping


class ProjectManager:
    def __init__(self, project_id):
        self.blackboard = BlackBoard(project_id)

        self.STEP_TO_STEP_FUNC_MAPPING = {
            Step.Scraping: do_scraping,
            Step.Filtering: do_filtering,
        }

 
    def _get_current_step(self) -> Step:
        return self.blackboard.get_data().state.step


    def _get_current_state(self) -> State:
        return self.blackboard.get_data().state


    def _get_current_step_index(self) -> int:
        return self.blackboard.get_data().state.curr_step_index


    def _get_execution_plan(self) -> List[Step]:
        return self.blackboard.get_data().execution_plan


    def _move_to_next_step(self) -> Step:
        curr_step_index = self._get_current_step_index()
        next_step_index = curr_step_index + 1
        print("curr_step_index = ",curr_step_index)

        execution_plan = self._get_execution_plan()
        print("execution_plan = ",execution_plan)

        next_step = execution_plan[next_step_index]
        print("next_step = ",next_step)

        self.blackboard.update_state(State(step=next_step, curr_step_index=next_step_index, interactable=False))
        return next_step


    def _get_func_for_step(self, step) -> any:
        return self.STEP_TO_STEP_FUNC_MAPPING[step]


    def start_execution_loop(self):
        curr_state = self._get_current_state()
        curr_step = curr_state.step

        while True:
            self._get_func_for_step(curr_step)()
            if curr_state.curr_step_index == len(self._get_execution_plan()) - 1:
                print("Project completed!")
                break
            curr_step = self._move_to_next_step()
            


def main():
    # Parse command-line arguments and handle potential errors
    parser = argparse.ArgumentParser(description="Script to process a thread link.")
    parser.add_argument("--thread_link", type=str, help="The URL of the thread to process.")
    args = parser.parse_args()

    # Try to load the thread link from the .env file if no CLI argument is provided
    if not args.thread_link:
        load_dotenv()  # Load environment variables from .env file
        thread_link = os.getenv("THREAD_LINK")

        if not thread_link:
            print("Error: Thread link not provided either as a CLI argument or in the .env file.")
            exit(1)  # Exit with an error code
    

    ProjectManager(thread_link).start_execution_loop()


if __name__ == "__main__":
    main()