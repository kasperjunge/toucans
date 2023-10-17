from dataclasses import asdict
from typing import Any

from jinja2 import Template
from litellm import completion

from .config import ChatAPIConfig
from .serialize import (
    deserialize_default_or_latest_chat_api_config,
    serialize_chat_api_config,
)
from .utils import extract_template_params, flatten_list


class PromptFunction:
    """Prompt function class."""

    def __init__(
        self,
        model: str,
        messages: list[str],
        temperature: float = 0.7,
        output_schema: dict = None,
        max_tokens: int = None,
        **kwargs,
    ):
        self.config = ChatAPIConfig(
            model=model,
            temperature=temperature,
            messages=messages,
            functions=[output_schema] if output_schema else [],
            function_call={"name": output_schema["name"]} if output_schema else None,
            max_tokens=max_tokens,
            **kwargs,
        )

        self.params = flatten_list([extract_template_params(m) for m in messages])

    @classmethod
    def from_dir(cls, load_dir):
        config = deserialize_default_or_latest_chat_api_config(load_dir)
        return cls(
            model=config.model,
            messages=config.messages,
            temperature=config.temperature,
            output_schema=config.functions,
            max_tokens=config.max_tokens,
        )

    def __call__(self, **kwargs: Any):
        invalid_keys = [key for key in kwargs if key not in self.params]
        if invalid_keys:
            raise ValueError(f"Invalid parameters found: {', '.join(invalid_keys)}")

        rendered_messages = []
        for message in self.config.messages:
            template = Template(message["content"])
            rendered_content = template.render(**kwargs)
            rendered_messages.append(
                {"role": message["role"], "content": rendered_content}
            )

        request = asdict(self.config)
        request = {k: v for k, v in request.items() if v is not None}
        request["messages"] = rendered_messages
        return completion(**request)

    def push_to_dir(self, save_dir: str):
        serialize_chat_api_config(self.config, save_dir)
