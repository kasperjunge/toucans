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

    # Serialize system_message as a .txt file if available
    if prompt.system_message:
        (directory_path / "system_message.txt").write_text(prompt.system_message)

    # Serialize template as a .txt file if available
    if prompt.template:
        (directory_path / "template.txt").write_text(prompt.template)

    # Serialize output_schema if available
    if prompt.output_schema:
        (directory_path / "output_schema.json").write_text(
            json.dumps(prompt.output_schema)
        )

    # Serialize functions only if the list is not empty
    if prompt.functions:
        (directory_path / "functions.json").write_text(json.dumps(prompt.functions))
