import os
import re
from typing import Any

from openai import ChatCompletion


class Prompt:
    """Prompt object."""

    @classmethod
    def from_hub(cls, identifier: str, api_key: str, version: str):
        return NotImplemented()

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

        # set api key
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", None)
        if not self.openai_api_key:
            raise ValueError(
                "No OpenAI API key provided and none found in environment variables."
            )

        # detect fields
        self.template_fields = self._detect_template_fields()
        self.system_message_fields = self._detect_system_message_fields()
        self.fields = self.template_fields + self.system_message_fields

    def _detect_template_fields(self):
        if self.template:
            return re.findall(r"\{(.*?)\}", self.template)
        else:
            return []

    def _detect_system_message_fields(self):
        if self.system_message:
            return re.findall(r"\{(.*?)\}", self.system_message)
        else:
            return []

    def _format_template(self, **kwargs) -> str:
        missing_fields = [
            field for field in self.template_fields if field not in kwargs
        ]
        if missing_fields:
            raise ValueError(f"Missing fields template: {', '.join(missing_fields)}")
        return self.template.format(**kwargs)

    def _format_system_message(self, **kwargs) -> str:
        missing_fields = [
            field for field in self.system_message_fields if field not in kwargs
        ]
        if missing_fields:
            raise ValueError(
                f"Missing system message fields: {', '.join(missing_fields)}"
            )
        return self.system_message.format(**kwargs)

    def __call__(self, *args, **kwargs):
        """Call prompt."""

        # render prompt
        if self.template:
            template_kwargs = {
                k: v for k, v in kwargs.items() if k in self.template_fields
            }
            prompt = self._format_template(**template_kwargs)
        else:
            prompt = args[0]

        # render system message
        if self.system_message:
            system_message_kwargs = {
                k: v for k, v in kwargs.items() if k in self.system_message_fields
            }
            system_message = (
                self._format_system_message(**system_message_kwargs)
                if self.system_message_fields
                else self.system_message
            )

        # compose messages

        # ChatCompletion.create(model=self.model, messages=)
        pass
