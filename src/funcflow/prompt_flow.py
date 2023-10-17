from .llm_config import LLMConfig
from .prompt_function import PromptFunction


class PromptFlow:
    def __init__(self, prompt_functions: list[PromptFunction]) -> None:
        self.prompt_functions = prompt_functions
