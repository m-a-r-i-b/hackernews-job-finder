from const import AgentBrainModel
from const import GPT_MODELS, ANTHROPIC_MODELS
from langchain_openai import ChatOpenAI
from const import FORMAT_INSTRUCTIONS_KEY, USER_MSG_KEY
from langchain_core.output_parsers import JsonOutputParser
import time
from pydantic import ValidationError
from const import AGENT_INITIAL_RETRY_DELAY, AGENT_MAX_RETRIES


class Agent():
    def __init__(
        self,
        brain_model: AgentBrainModel,
        prompt,
        output_pydantic_class,
    ):
        self.brain_model = brain_model
        self.brain = self._initialize_brain()
        self.prompt = prompt
        self.output_pydantic_class = output_pydantic_class
        self.output_parser = JsonOutputParser(pydantic_object=output_pydantic_class)

    def _initialize_brain(self):
        if self.brain_model in GPT_MODELS:
            return ChatOpenAI(model=self.brain_model)
        elif self.brain_model in ANTHROPIC_MODELS:
            return None
        else:
            raise ValueError("Invalid agent type provided.")

   
    def run(self, user_msg: str):
        if self.brain_model in GPT_MODELS:
            agent_output, attempts = self._runGPT(user_msg)
            return agent_output
        elif self.brain_model in ANTHROPIC_MODELS:
            return self._runAnthropic(user_msg)
        else:
            raise ValueError("Invalid agent type provided.")


    def _runGPT(self, user_msg: str):

        retry_delay = AGENT_INITIAL_RETRY_DELAY
        attempt = 0
        last_exception = None

        while attempt < AGENT_MAX_RETRIES:
            try:
                # If there was an exception in the previous attempt, add it to the prompt, so AI can learn from it
                if last_exception:
                    self.prompt.append(("ai", last_exception))

                chain = self.prompt | self.brain | self.output_parser

                raw_result = chain.invoke(
                    {
                        USER_MSG_KEY: user_msg,
                        FORMAT_INSTRUCTIONS_KEY: self.output_parser.get_format_instructions(),
                    }
                )

                output = self.output_pydantic_class(**raw_result)
                return output, attempt

            except (ValidationError, KeyError) as e:
                print(
                    f"Attempt {attempt + 1}/{AGENT_MAX_RETRIES} failed with error: {e}"
                )
                last_exception = str(e)
            except Exception as e:
                print(
                    f"An unexpected error occurred on attempt {attempt + 1}/{AGENT_MAX_RETRIES}: {e}"
                )
                last_exception = str(e)

            attempt += 1
            if attempt < AGENT_MAX_RETRIES:
                retry_delay += attempt
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise RuntimeError(
                    "Max retries reached. Unable to cast result into Pydantic model."
                )

        raise RuntimeError(
            "Failed to cast result into Pydantic model after maximum retries."
        )

    def _runAnthropic(self, user_msg: str):
        # TODO
        print("Running Anthropic...", self.brain_model, self.brain)
