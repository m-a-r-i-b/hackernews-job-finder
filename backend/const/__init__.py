from enum import Enum



class Step(str, Enum):
    IS_REMOTE_WORK_ALLOWED = "IS_REMOTE_WORK_ALLOWED"
    EXTRACT_KEYWORDS = "EXTRACT_KEYWORDS"
    EXTRACT_ROLES = "EXTRACT_ROLES"
    EXTRACT_CONTACT_INFO = "EXTRACT_CONTACT_INFO"
    GENERATE_COVER_LETTER = "GENERATE_COVER_LETTER"

    def __str__(self) -> str:
        return str.__str__(self)
    


RAW_COMMENTS_DIR="raw_comments"
CRITERIA_FILTERED_COMMENTS="criteria_filtered_comments"
CRITERIA_FILE_PATH="criteria"

USER_MSG_KEY = "user_msg"
FORMAT_INSTRUCTIONS_KEY = "format_instructions"
FORMAT_INSTRUCTIONS_PLACEHOLDER = "{" + FORMAT_INSTRUCTIONS_KEY + "}"

AGENT_MAX_RETRIES = 5
AGENT_INITIAL_RETRY_DELAY = 2


class AgentBrainModel(str, Enum):
    GPT_4_Turbo = "gpt-4-turbo"
    GPT_4_Omni = "gpt-4o"
    GPT_3_5_Turbo_0125 = "gpt-3.5-turbo-0125"

    Claude_Opus = "claude-3-opus-20240229"
    Claude_Sonnet = "claude-3-sonnet-20240229"

    def __str__(self) -> str:
        return str.__str__(self)


GPT_MODELS = [
    AgentBrainModel.GPT_3_5_Turbo_0125,
    AgentBrainModel.GPT_4_Turbo,
    AgentBrainModel.GPT_4_Omni,
]
ANTHROPIC_MODELS = [AgentBrainModel.Claude_Opus, AgentBrainModel.Claude_Sonnet]



EXECUTION_PLAN = [
    Step.IS_REMOTE_WORK_ALLOWED,
    Step.EXTRACT_ROLES,
    Step.EXTRACT_KEYWORDS,
    Step.EXTRACT_CONTACT_INFO,
    Step.GENERATE_COVER_LETTER
]