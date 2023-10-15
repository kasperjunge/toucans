import asyncio
import logging
import os
import pathlib
from typing import Any

import aiohttp
import openai
from litellm import acompletion, completion

from .messages import create_messages
from .serialize import deserialize_from_dir, serialize_to_dir
from .utils import extract_template_args


class Prompt:
    """Prompt object."""

    def __init__(
        self,
        model: str,
        temperature: float = 0.7,
        system_message: str = None,
        system_message_template: str = None,
        prompt_template: str = None,
        output_schema: dict = None,
        api_key: str = None,
    ):
        self.model = model
        self.temperature = temperature
        self.system_message = system_message
        self.system_message_template = system_message_template
        self.prompt_template = prompt_template
        self.output_schema = output_schema
        self.functions = []
        self.function_call = ""
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", None)
        self._validate_init_args()

        self.prompt_template_args = (
            extract_template_args(self.prompt_template)
            if self.prompt_template
            else None
        )
        self.system_message_template_args = (
            extract_template_args(self.system_message_template)
            if self.system_message_template
            else None
        )

        if self.output_schema:
            self.functions = [self.output_schema]
            self.function_call = self.output_schema["name"]

    def _validate_init_args(self):
        if not self.api_key:
            raise ValueError(
                "No OpenAI API key provided and none found in environment variables."
            )

        if self.system_message and self.system_message_template:
            raise ValueError(
                "Cannot provide both system_message and system_message_template together!"
            )

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Call OpenAI chat completion API with the configured prompt setup."""

        prompt = args[0] if args else None

        prompt_template_args = None
        if self.prompt_template_args:
            prompt_template_args = {
                key: kwargs.get(key, None) for key in self.prompt_template_args
            }

        system_message_template_args = None
        if self.system_message_template_args:
            system_message_template_args = {
                key: kwargs.get(key, None) for key in self.system_message_template_args
            }

        messages = create_messages(
            prompt=prompt,
            prompt_template=self.prompt_template,
            prompt_template_args=prompt_template_args,
            system_message=self.system_message,
            system_message_template=self.system_message_template,
            system_message_template_args=system_message_template_args,
        )

        return completion(
            model=self.model,
            temperature=self.temperature,
            messages=messages,
            functions=self.functions,
            function_call={"name": self.function_call},
        )

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

    async def _run_task(
        self,
        batch_arg,
        num_retries,
        counter,
        total,
    ):
        # create messages
        prompt_template_args = None
        if self.prompt_template_args:
            prompt_template_args = {
                key: batch_arg.get(key, None) for key in self.prompt_template_args
            }

        system_message_template_args = None
        if self.system_message_template_args:
            system_message_template_args = {
                key: batch_arg.get(key, None)
                for key in self.system_message_template_args
            }
        messages = create_messages(
            prompt=None,
            prompt_template=self.prompt_template,
            prompt_template_args=prompt_template_args,
            system_message=self.system_message,
            system_message_template=self.system_message_template,
            system_message_template_args=system_message_template_args,
        )
        for attempt in range(num_retries + 1):
            try:
                response = await acompletion(
                    model=self.model,
                    temperature=self.temperature,
                    messages=messages,
                    functions=self.functions,
                    function_call={"name": self.function_call},
                )
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
        return

    def push_to_dir(self, directory_path: pathlib.Path):
        serialize_to_dir(directory_path=directory_path, prompt=self)

    @classmethod
    def from_dir(cls, directory_path: pathlib.Path):
        return cls(**deserialize_from_dir(directory_path))

    def get_init_args(self) -> dict:
        return {
            "model": self.model,
            "temperature": self.temperature,
            "system_message": self.system_message,
            "system_message_template": self.system_message_template,
            "prompt_template": self.prompt_template,
            "output_schema": self.output_schema,
        }
