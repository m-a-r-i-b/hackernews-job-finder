
import random
from agents.base import Agent
from agents.base.AgentOutput import AgentOutput


class ScraperAgent(Agent):
    def __init__(
        self,
        *args,
    ):
        super().__init__()

    def run(
        self, user_msg: str, user_id: str, project_id: str, session_id: str
    ) -> AgentOutput:
        
        if self.repo_url is None:
            repo_url = self._create_repo_and_push_contract(user_id)
        else:
            repo_url = self._push_updated_contract(repo_url, user_id)
            
        
        return CommitOutput(observation=AgentObservation.STEP_COMPLETED, data=CommitOutputData(message="Project Committed Successfully!", repo_url=repo_url))


    def _create_repo_and_push_contract(self, user_id: str):
        # TODO : Implement this
        repo_url = str(random.randint(0, 9))
        return repo_url 


    def _push_updated_contract(self, repo_url: str, user_id: str):
        repo_url += "Updateed "
        return repo_url