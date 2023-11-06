import asyncio
import logging
from dataclasses import asdict

import aiohttp
from jinja2 import Template
from litellm import acompletion, completion

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
        messages: list[dict[str, str]],
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

    def __call__(self, **kwargs):
        request = self._prep_request(**kwargs)
        return completion(**request)

    def _prep_request(self, **kwargs):
        request = asdict(self.config)
        request = {k: v for k, v in request.items() if v is not None}
        request["messages"] = self._render_messages(**kwargs)
        return request

    def _render_messages(
        self,
        **kwargs,
    ) -> list[dict[str, str]]:
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

        return rendered_messages

    def batch_call(
        self,
        batch_args: list[dict],
        num_retries: int = 3,
        concurrency_limit: int = 10,
        timeout: int = None,
    ):
        return asyncio.run(
            self._run_batch_async(
                batch_args,
                num_retries,
                concurrency_limit,
                timeout,
            )
        )

    async def _run_batch_async(
        self,
        batch_args: list[dict],
        num_retries: int = 3,
        concurrency_limit: int = 10,
        timeout: int = None,
    ):
        counter = [0]
        total = len(batch_args)

        tasks = []
        sem = asyncio.Semaphore(concurrency_limit)

        async with aiohttp.ClientSession() as session:
            for batch_arg in batch_args:
                async with sem:
                    task = asyncio.create_task(
                        self._run_task(
                            batch_arg,
                            num_retries,
                            counter,
                            total,
                        )
                    )
                    tasks.append(task)
            if timeout:
                return await asyncio.gather(*tasks, timeout=timeout)
            else:
                return await asyncio.gather(*tasks)

    async def _run_task(
        self,
        batch_arg,
        num_retries,
        counter,
        total,
    ):
        request = self._prep_request(batch_arg)

        for attempt in range(num_retries + 1):
            try:
                response = await acompletion(**request)
                counter[0] += 1
                print(f"Progress: {counter[0]}/{total} completed")
                return response
            except Exception as e:
                if attempt == num_retries:
                    logging.error(
                        f"Request failed after {num_retries} retries with. Error: {e}"
                    )
                    return None
                continue
        return None

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

    def push_to_dir(self, save_dir: str):
        serialize_chat_api_config(self.config, save_dir)
