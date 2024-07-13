from agents.is_remote.agent import IsRemoteAgent
from agents.keyword.agent import KeywordAgent
from agents.role.agent import RoleAgent
from agents.contact_info.agent import ContactInfoAgent
from agents.cover_letter.agent import CoverLetterAgent
from const import Step


STEP_TO_AGENT_MAPPING = {
    Step.IS_REMOTE_WORK_ALLOWED: IsRemoteAgent,
    Step.EXTRACT_KEYWORDS: KeywordAgent,
    Step.EXTRACT_ROLES: RoleAgent,
    Step.EXTRACT_CONTACT_INFO: ContactInfoAgent,
    Step.GENERATE_COVER_LETTER: CoverLetterAgent,
}