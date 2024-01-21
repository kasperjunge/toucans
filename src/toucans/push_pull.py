import json
import os
from dataclasses import asdict
from typing import Optional

import requests

from .completion_config import CompletionConfig


class DirectoryPushPullMixin:
    """Add .from_dir and push_to_dir to the PromptFunction class."""

    @classmethod
    def from_dir(cls, load_dir):
        """Load prompt function from a directory."""

        config_path = os.path.join(load_dir, "config.json")
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"No config file found in {load_dir}")

        with open(config_path, "r") as file:
            config_data = json.load(file)

        return cls(**config_data)

    def push_to_dir(self, save_dir: str):
        """Push prompt function to a directory."""

        os.makedirs(save_dir, exist_ok=True)

        config_path = os.path.join(save_dir, "config.json")  # Example file name
        with open(config_path, "w") as file:
            config_data = asdict(self.completion_config)
            json.dump(config_data, file, indent=4)


class HubPushPullMixin:
    """Add .from_hub and push_to_hub to the PromptFuncntion class."""

    @classmethod
    def from_hub(cls, name: str):
        """Load prompt function from the toucans hub."""
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

    def push_to_hub(self, name: str):
        """Push prompt function to the toucans hub."""
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


# # ---------------------------------------------------------------------------- #
# #                                   Serialize                                  #
# # ---------------------------------------------------------------------------- #


# class CompletionConfigSerializer:
#     """Serialization mixin class for PromptFunction"""

#     @classmethod
#     def from_dir(cls, load_dir):
#         config = deserialize_default_or_latest_completion_config(load_dir)

#         return cls(**asdict(config))

#     def push_to_dir(self, save_dir: str):
#         """Push promp function to directory. If the directory does not exist
#         a new directory is created. If the is changed a new version will be
#         saved in the directory."""
#         serialize_completion_config(self.completion_config, save_dir)


# def serialize_completion_config(config: CompletionConfig, base_save_dir: str):
#     config_hash = config.unique_hash()
#     save_dir = os.path.join(base_save_dir, config_hash)

#     # If directory with the hash name doesn't exist, create it
#     if not os.path.exists(save_dir):
#         os.makedirs(save_dir)

#         # Serialize main config without messages to JSON
#         config_data = asdict(config)
#         messages = config_data.pop("messages")  # Remove messages and store separately
#         with open(os.path.join(save_dir, "config.json"), "w") as json_file:
#             json.dump(config_data, json_file, indent=4)

#         # Serialize messages to separate files
#         message_dir = os.path.join(save_dir, "messages")
#         os.makedirs(message_dir, exist_ok=True)

#         for idx, message in enumerate(messages):
#             role = message["role"]
#             content = message["content"]
#             filename = f"{idx}_{role}.txt"
#             with open(os.path.join(message_dir, filename), "w") as txt_file:
#                 txt_file.write(content)
#     else:
#         print(f"Configuration with hash {config_hash} already exists.")


# # ---------------------------------------------------------------------------- #
# #                                  Deserialize                                 #
# # ---------------------------------------------------------------------------- #


# def deserialize_default_or_latest_completion_config(
#     base_save_dir: str,
# ) -> CompletionConfig:
#     # First, check if there's a default directory
#     load_dir = get_default_config_directory(base_save_dir)

#     # If not, get the latest directory
#     if load_dir is None:
#         load_dir = get_latest_config_directory(base_save_dir)

#     # Deserialize the CompletionConfig from the chosen directory
#     return deserialize_completion_config(load_dir)


# def deserialize_completion_config(load_dir: str) -> CompletionConfig:
#     # Load main config from JSON
#     with open(os.path.join(load_dir, "config.json"), "r") as json_file:
#         config_data = json.load(json_file)

#     # Load messages from separate files
#     messages = []
#     message_dir = os.path.join(load_dir, "messages")

#     # Sort filenames to ensure messages are loaded in the correct order
#     filenames = sorted(os.listdir(message_dir), key=lambda s: int(s.split("_")[0]))
#     for filename in filenames:
#         role = filename.split("_")[1].split(".")[0]
#         with open(os.path.join(message_dir, filename), "r") as txt_file:
#             content = txt_file.read()
#             messages.append({"role": role, "content": content})

#     config_data["messages"] = messages
#     return CompletionConfig(**config_data)


# def get_latest_config_directory(base_save_dir: str) -> str:
#     subdirs = [
#         os.path.join(base_save_dir, d)
#         for d in os.listdir(base_save_dir)
#         if os.path.isdir(os.path.join(base_save_dir, d))
#     ]
#     latest_dir = max(subdirs, key=os.path.getmtime)
#     return latest_dir


# def get_default_config_directory(base_save_dir: str) -> Optional[str]:
#     default_dir = os.path.join(base_save_dir, "default")
#     if os.path.exists(default_dir) and os.path.isdir(default_dir):
#         return default_dir
#     return None
