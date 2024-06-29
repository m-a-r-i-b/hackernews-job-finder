from agents.base.AgentOutput import (
    AgentObservation,
    AgentOutput,
    AgentOutputData,
)
from langchain_core.pydantic_v1 import Field, root_validator
from const.smart_contracts import SmartContractType
from typing import Optional


class TypeClassifierOutputData(AgentOutputData):
    smart_contract_type: Optional[SmartContractType] = Field(
        description="the type of smart contract", default=None
    )


class TypeClassifierOutput(AgentOutput):
    data: TypeClassifierOutputData

    @root_validator(pre=True)
    def check_smart_contract_type(cls, values):
        observation = values.get("observation")
        data = values.get("data", {})
        smart_contract_type = data.get("smart_contract_type")

        if (
            observation == AgentObservation.STEP_COMPLETED
            and smart_contract_type is None
        ):
            raise ValueError(
                f"smart_contract_type must be provided if observation is {AgentObservation.STEP_COMPLETED}"
            )

        return values
