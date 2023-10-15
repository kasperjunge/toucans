import json
import pathlib


def serialize_to_dir(directory_path, prompt):
    if not isinstance(directory_path, pathlib.Path):
        directory_path = pathlib.Path(directory_path)

    directory_path.mkdir(parents=True, exist_ok=True)

    # Serialize model and temperature in a single JSON file named model_args.json
    model_args = {
        "model": prompt.model,
        "temperature": prompt.temperature,
    }
    (directory_path / "model_args.json").write_text(json.dumps(model_args))

    # txt files
    if prompt.system_message:
        (directory_path / "system_message.txt").write_text(prompt.system_message)

    if prompt.system_message_template:
        (directory_path / "system_message_template.txt").write_text(
            prompt.system_message_template
        )

    if prompt.prompt_template:
        (directory_path / "prompt_template.txt").write_text(prompt.prompt_template)

    # Serialize output_schema if available
    if prompt.output_schema:
        (directory_path / "output_schema.json").write_text(
            json.dumps(prompt.output_schema)
        )

    # Serialize functions only if the list is not empty
    if prompt.functions:
        (directory_path / "functions.json").write_text(json.dumps(prompt.functions))


def deserialize_from_dir(directory_path):
    if not isinstance(directory_path, pathlib.Path):
        directory_path = pathlib.Path(directory_path)

    # Initialize an empty dictionary to hold the initial arguments
    init_args = {}

    # Deserialize model and temperature from model_args.json
    model_args_path = directory_path / "model_args.json"
    if model_args_path.exists():
        with open(model_args_path, "r") as f:
            model_args = json.load(f)
        init_args.update(model_args)

    # Deserialize text files
    system_message_path = directory_path / "system_message.txt"
    if system_message_path.exists():
        init_args["system_message"] = system_message_path.read_text()

    system_message_template_path = directory_path / "system_message_template.txt"
    if system_message_template_path.exists():
        init_args["system_message_template"] = system_message_template_path.read_text()

    prompt_template_path = directory_path / "prompt_template.txt"
    if prompt_template_path.exists():
        init_args["prompt_template"] = prompt_template_path.read_text()

    # Deserialize output_schema
    output_schema_path = directory_path / "output_schema.json"
    if output_schema_path.exists():
        with open(output_schema_path, "r") as f:
            init_args["output_schema"] = json.load(f)

    # Deserialize functions
    functions_path = directory_path / "functions.json"
    if functions_path.exists():
        with open(functions_path, "r") as f:
            init_args["functions"] = json.load(f)

    return init_args
