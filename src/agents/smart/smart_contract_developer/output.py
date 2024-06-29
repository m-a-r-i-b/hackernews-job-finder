from agents.base.AgentOutput import (
    AgentObservation,
    AgentOutput,
    AgentOutputData,
)
from langchain_core.pydantic_v1 import root_validator
from typing import Optional


class SmartContractDeveloperOutputData(AgentOutputData):
    smart_contract: Optional[str]


class SmartContractDeveloperOutput(AgentOutput):
    data: SmartContractDeveloperOutputData

    @root_validator(pre=True)
    def check_smart_contract_type(cls, values):
        observation = values.get("observation")
        data = values.get("data", {})
        smart_contract = data.get("smart_contract")

        if (
            observation == AgentObservation.STEP_COMPLETED
            and smart_contract is None
        ):
            raise ValueError(
                f"smart_contract must be provided if observation is {AgentObservation.STEP_COMPLETED}"
            )

        return values
