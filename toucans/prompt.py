import os
import re

from jinja2 import Template
from openai import ChatCompletion

from .utils import extract_template_args


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

        # set api key
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", None)
        if not self.openai_api_key:
            raise ValueError(
                "No OpenAI API key provided and none found in environment variables."
            )


# ---------------------------------------------------------------------------- #
#                    Compose OpenAI Chat Completion Request                    #
# ---------------------------------------------------------------------------- #


def compose_messages(
    prompt: str = None,
    template: str = None,
    template_args: dict = None,
    system_message: str = None,
    system_message_args: str = None,
):
    """Compose messages for OpenAI chat completion."""

    # Check valid args
    if prompt and template:
        raise ValueError("SOME GREAT ERROR MESSAGE HERE!")

    if template and not extract_template_args(template):
        raise ValueError("SOME GREAT ERROR MESSAGE HERE!")

    if system_message_args and not extract_template_args(system_message):
        raise ValueError("SOME GREAT ERROR MESSAGE HERE!")

    messages = []

    # System Message
    if system_message:
        if system_message_args:
            rendered_system_message = Template(system_message).render(
                **system_message_args
            )
            messages.append({"System": rendered_system_message})
        else:
            messages.append({"System": system_message})

    # Template
    if template:
        rendered_template = Template(template).render(**template_args)
        messages.append({"Human": rendered_template})

    # Prompt
    if prompt:
        messages.append({"Human": prompt})

    return messages


def compose_chat_completion_request(messages: list) -> dict:
    return


# ---------------------------------------------------------------------------- #
#                                    Utility                                   #
# ---------------------------------------------------------------------------- #


def detect_template_fields():
    return
