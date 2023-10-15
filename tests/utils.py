from jinja2 import Template

# Test variables
TEST_MODEL = "gpt-4"
TEST_PROMPT = "Test prompt."
PROMPT_TEMPLATE = "Test prompt template {{ foo }} {{ bar }}."
PROMPT = "Test prompt."
SYSTEM_MESSAGE = "Test system message."
SYSTEM_MESSAGE_TEMPLATE = "Test system message with args {{ foo }} {{ bar }}."
TEST_ARGS = {"foo": "egg", "bar": "spam"}
RENDERED_PROMPT_TEMPLATE = Template(PROMPT_TEMPLATE).render(**TEST_ARGS)
RENDERED_SYSTEM_MESSAGE_TEMPLATE = Template(SYSTEM_MESSAGE_TEMPLATE).render(**TEST_ARGS)


TEST_MESSAGES = [
    {"role": "system", "content": SYSTEM_MESSAGE},
    {"role": "user", "content": TEST_PROMPT},
]

TEST_FUNCTION = {
    "name": "get_current_weather",
    "description": "Get the current weather",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA",
            },
            "format": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "The temperature unit to use. Infer this from the users location.",
            },
        },
        "required": ["location", "format"],
    },
}

MOCK_OPENAI_CHAT_COMPLETION_RESPONSE = {
    "id": "chatcmpl-123",
    "object": "chat.completion",
    "created": 1677652288,
    "model": "gpt-3.5-turbo-0613",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "\n\nHello there, how may I assist you today?",
            },
            "finish_reason": "stop",
        }
    ],
    "usage": {"prompt_tokens": 9, "completion_tokens": 12, "total_tokens": 21},
}
