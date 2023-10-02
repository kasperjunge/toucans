import os
from typing import Any

from litellm import completion

from ..utils import extract_template_args
from .messages import create_messages


class Prompt:
    """Prompt object."""

    def __init__(
        self,
        model: str,
        temperature: float = 0.7,
        system_message: str = None,
        template: str = None,
        output_schema: dict = None,
        api_key: str = None,
    ):
        self.model = model
        self.temperature = temperature
        self.system_message = system_message
        self.template = template
        self.output_schema = output_schema
        self.functions = []
        self.function_call = ""

        self.template_args = (
            extract_template_args(self.template) if self.template else None
        )
        self.system_message_args = (
            extract_template_args(self.system_message) if self.system_message else None
        )

        if self.output_schema:
            self.functions = [self.output_schema]
            self.function_call = self.output_schema["name"]

        # set api key
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", None)
        if not self.api_key:
            raise ValueError(
                "No OpenAI API key provided and none found in environment variables."
            )

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Call OpenAI chat completion API with the configured prompt setup."""

        prompt = args[0] if args else None

        template_args = None
        if self.template_args:
            template_args = {key: kwargs.get(key, None) for key in self.template_args}

        # Extract system message args from kwargs, set to None if not present
        system_message_args = None
        if self.system_message_args:
            system_message_args = {
                key: kwargs.get(key, None) for key in self.system_message_args
            }

        messages = create_messages(
            prompt=prompt,
            template=self.template,
            template_args=template_args,
            system_message=self.system_message,
            system_message_args=system_message_args,
        )

        return completion(
            model=self.model,
            temperature=self.temperature,
            messages=messages,
            functions=self.functions,
            function_call=self.function_call,
        )
