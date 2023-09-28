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
#                    Compose OpenAI Chat Completion Messages                   #
# ---------------------------------------------------------------------------- #


def validate_compose_messages_args(
    prompt, template, template_args, system_message, system_message_args
):
    """Validates the input arguments for the compose_messages function."""

    if prompt and template:
        raise ValueError("Cannot provide both prompt and template together!")

    if template_args and not template:
        raise ValueError("Template args provided without a corresponding template!")

    if template and not extract_template_args(template) and template_args:
        raise ValueError(
            "Template provided doesn't require args, but template args given!"
        )

    if system_message_args and not system_message:
        raise ValueError(
            "System message args provided without a corresponding system message!"
        )

    if template and extract_template_args(template) and not template_args:
        raise ValueError("Template requires args but none provided!")

    if (
        system_message
        and extract_template_args(system_message)
        and not system_message_args
    ):
        raise ValueError("System message requires args but none provided!")


def compose_messages(
    prompt: str = None,
    template: str = None,
    template_args: dict = None,
    system_message: str = None,
    system_message_args: str = None,
):
    """Compose messages for OpenAI chat completion."""

    validate_compose_messages_args(
        prompt,
        template,
        template_args,
        system_message,
        system_message_args,
    )

    messages = []

    # System Message
    if system_message:
        if system_message_args:
            rendered_system_message = Template(system_message).render(
                **system_message_args
            )
            messages.append({"role": "system", "content": rendered_system_message})
        else:
            messages.append({"role": "system", "content": system_message})

    # Template
    if template:
        rendered_template = Template(template).render(**template_args)
        messages.append({"role": "user", "content": rendered_template})

    # Prompt
    if prompt:
        messages.append({"role": "user", "content": prompt})

    return messages


# ---------------------------------------------------------------------------- #
#                    Compose OpenAI Chat Completion Request                    #
# ---------------------------------------------------------------------------- #
import openai


def compose_chat_completion_request(
    model: str,
    temperature: float,
    messages: list,
    functions: list = None,
) -> dict:
    kwargs = {"model": model, "temperature": temperature, "messages": messages}
    if functions:
        kwargs["functions"] = functions
        kwargs["function_call"] = functions[0]["name"]
    return openai.ChatCompletion.create(**kwargs)


# ---------------------------------------------------------------------------- #
#                                    Utility                                   #
# ---------------------------------------------------------------------------- #


def detect_template_fields():
    return
