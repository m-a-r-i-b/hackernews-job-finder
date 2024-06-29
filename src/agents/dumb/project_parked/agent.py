
from agents.base.DumbAgent import DumbAgent
from agents.base.AgentOutput import AgentObservation, AgentOutput, AgentOutputData


class ProjectParkedAgent(DumbAgent):
    def __init__(
        self, *args
    ):
        super().__init__()

    def run(
        self, *args
    ) -> AgentOutput:
        
        return AgentOutput(observation=AgentObservation.STEP_COMPLETED, data=AgentOutputData(message="Project is parked."))
