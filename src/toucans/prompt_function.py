import asyncio
import json
import logging
import os
from dataclasses import asdict
from typing import List, Optional

import aiohttp
import requests
from jinja2 import Template
from litellm import acompletion, completion

from .completion_config import CompletionConfig
from .utils import extract_template_params, flatten_list


class PromptFunction:
    """Prompt function class."""

    def __init__(
        self,
        model: str,
        messages: List[dict],
        temperature: float = 0.7,
        max_tokens: Optional[float] = None,
        response_format: Optional[dict] = None,
        seed: Optional[int] = None,
        tools: Optional[List] = None,
        tool_choice: Optional[str] = None,
        **kwargs,
    ):
        self.completion_config = CompletionConfig(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=tools,
            tool_choice=tool_choice,
            response_format=response_format,
            seed=seed,
            **kwargs,
        )

        self.params = flatten_list([extract_template_params(m) for m in messages])

    def __call__(self, **kwargs):
        request = self._prep_request(**kwargs)
        return completion(**request)

    def _prep_request(self, **kwargs):
        request = asdict(self.completion_config)
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
        for message in self.completion_config.messages:
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

    def push_to_hub(self, name: str):
        """
        Pushes the current instance to the Hub, creating a new entry or updating an existing one.
        """
        api_url = os.getenv("HUB_API_URL")
        if not api_url:
            raise ValueError("HUB_API_URL environment variable not set")

        endpoint = f"{api_url}/prompt-functions/"

        data = {
            "name": name,
            "hash_id": self.completion_config.unique_hash(),
            "completion_config": asdict(self.completion_config),
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(endpoint, data=json.dumps(data), headers=headers)

        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to push to hub: {response.text}")
        return response.json()

    @classmethod
    def from_hub(cls, name: str):
        """
        Retrieves a PromptFunction instance from the Hub by its name.
        """
        api_url = os.getenv("HUB_API_URL")
        if not api_url:
            raise ValueError("HUB_API_URL environment variable not set")

        response = requests.get(f"{api_url}/prompt-functions/{name}")

        if response.status_code != 200:
            raise Exception(f"Failed to fetch from hub: {response.text}")

        data = response.json()
        model = data["completion_config"].pop("model")
        messages = data["completion_config"].pop("messages")
        return cls(model=model, messages=messages, **data["completion_config"])
