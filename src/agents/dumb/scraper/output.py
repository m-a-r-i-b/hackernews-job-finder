from agents.base.AgentOutput import (
    AgentOutput,
    AgentOutputData,
)


class CommitOutputData(AgentOutputData):
    repo_url: str

class CommitOutput(AgentOutput):
    data: CommitOutputData

