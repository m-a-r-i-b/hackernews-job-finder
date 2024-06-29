from typing import Dict, List
from const import EXECUTION_PLAN, Step
from dataclasses import dataclass, field


@dataclass
class State:
    curr_step: Step = EXECUTION_PLAN[0]
    curr_step_index: int = 0


@dataclass
class BlackBoardData:
    execution_plan: List[Step] = field(
        default_factory=lambda: EXECUTION_PLAN
    )
    state: State = State()
    state_history: List[State] = field(default_factory=list)
    information: Dict[Step, any] = field(default_factory=dict)
    

    @classmethod
    def from_json(cls, json_dict) -> "BlackBoardData":
        return cls(
            execution_plan=json_dict.get("execution_plan", []),
            state=State(**json_dict.get("state", {})),
            state_history=json_dict.get("state_history", []),
            information=json_dict.get("information", {}),
        )
