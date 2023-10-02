import openai

VALID_MODELS = ["gpt-4", "gpt-4-32k", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"]


def validate_args(
    model: str,
    temperature: float,
    messages: list,
    functions: list = None,
):
    if model not in VALID_MODELS:
        raise ValueError(
            f"The model '{model}' is not supported. Please use one of the following: {', '.join(VALID_MODELS)}"
        )
    if not (0 <= temperature <= 2):
        raise ValueError(
            f"The 'temperature' must be a float between 0 and 2, inclusive. You provided {temperature}."
        )
    if not messages:
        raise ValueError("The 'messages' list cannot be empty.")

    for msg in messages:
        if not all(key in msg for key in ("role", "content")):
            raise ValueError(
                "Each message dictionary must contain both 'role' and 'content' keys."
            )

        if msg["role"] not in ["user", "system"]:
            raise ValueError(
                f"Invalid role '{msg['role']}' in message list. Expected 'user' or 'system'."
            )

    if functions:
        if not all("name" in func for func in functions):
            raise ValueError(
                "Each function dictionary in 'functions' must contain a 'name' key."
            )


def request_chat_completion(
    model: str,
    temperature: float,
    messages: list,
    functions: list = None,
) -> dict:
    validate_args(model, temperature, messages, functions)

    kwargs = {"model": model, "temperature": temperature, "messages": messages}
    if functions:
        kwargs["functions"] = functions
        kwargs["function_call"] = functions[0]["name"]
    return openai.ChatCompletion.create(**kwargs)
