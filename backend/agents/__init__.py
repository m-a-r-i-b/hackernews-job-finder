from agents.is_remote.agent import IsRemoteAgent
from const import Step


STEP_TO_AGENT_MAPPING = {
    Step.IS_REMOTE_WORK_ALLOWED: IsRemoteAgent,
}