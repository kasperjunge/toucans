import json
import os
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Union

from .config import ChatAPIConfig

# ---------------------------------------------------------------------------- #
#                                   Serialize                                  #
# ---------------------------------------------------------------------------- #


def serialize_chat_api_config(config: ChatAPIConfig, base_save_dir: str):
    # Generate the hash for the current configuration
    config_hash = config.unique_hash()  # assuming you named the method unique_hash

    # Define the save directory based on the hash
    save_dir = os.path.join(base_save_dir, config_hash)

    # If directory with the hash name doesn't exist, create it
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

        # Serialize main config without messages to JSON
        config_data = asdict(config)
        messages = config_data.pop("messages")  # Remove messages and store separately
        with open(os.path.join(save_dir, "config.json"), "w") as json_file:
            json.dump(config_data, json_file, indent=4)

        # Serialize messages to separate files
        message_dir = os.path.join(save_dir, "messages")
        os.makedirs(message_dir, exist_ok=True)

        for idx, message in enumerate(messages):
            role = message["role"]
            content = message["content"]
            filename = f"{idx}_{role}.txt"
            with open(os.path.join(message_dir, filename), "w") as txt_file:
                txt_file.write(content)
    else:
        print(f"Configuration with hash {config_hash} already exists.")


# ---------------------------------------------------------------------------- #
#                                  Deserialize                                 #
# ---------------------------------------------------------------------------- #


def deserialize_default_or_latest_chat_api_config(base_save_dir: str) -> ChatAPIConfig:
    # First, check if there's a default directory
    load_dir = get_default_config_directory(base_save_dir)

    # If not, get the latest directory
    if load_dir is None:
        load_dir = get_latest_config_directory(base_save_dir)

    # Deserialize the ChatAPIConfig from the chosen directory
    return deserialize_chat_api_config(load_dir)


def deserialize_chat_api_config(load_dir: str) -> ChatAPIConfig:
    # Load main config from JSON
    with open(os.path.join(load_dir, "config.json"), "r") as json_file:
        config_data = json.load(json_file)

    # Load messages from separate files
    messages = []
    message_dir = os.path.join(load_dir, "messages")

    # Sort filenames to ensure messages are loaded in the correct order
    filenames = sorted(os.listdir(message_dir), key=lambda s: int(s.split("_")[0]))
    for filename in filenames:
        role = filename.split("_")[1].split(".")[0]
        with open(os.path.join(message_dir, filename), "r") as txt_file:
            content = txt_file.read()
            messages.append({"role": role, "content": content})

    config_data["messages"] = messages
    return ChatAPIConfig(**config_data)


def get_latest_config_directory(base_save_dir: str) -> str:
    subdirs = [
        os.path.join(base_save_dir, d)
        for d in os.listdir(base_save_dir)
        if os.path.isdir(os.path.join(base_save_dir, d))
    ]
    latest_dir = max(subdirs, key=os.path.getmtime)
    return latest_dir


def get_default_config_directory(base_save_dir: str) -> Optional[str]:
    default_dir = os.path.join(base_save_dir, "default")
    if os.path.exists(default_dir) and os.path.isdir(default_dir):
        return default_dir
    return None
