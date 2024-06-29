from agents.base.AgentOutput import (
    AgentOutput,
)
from typing import List


class FilterAgentOutput(AgentOutput):
    decision: bool
    decision_reason: str
    met_optional_criteria: List[str]
    met_optional_criteria_reason: List[str]


