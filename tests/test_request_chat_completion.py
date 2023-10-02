from unittest.mock import patch

import pytest

from toucans.prompt.chat_completion_request import request_chat_completion

from .utils import MOCK_OPENAI_CHAT_COMPLETION_RESPONSE, TEST_FUNCTION, TEST_MESSAGES


def test_invalid_model():
    with pytest.raises(ValueError):
        request_chat_completion("gpt-2", 0.5, TEST_MESSAGES)


# Test for invalid temperature
def test_invalid_temperature():
    with pytest.raises(ValueError):
        request_chat_completion("gpt-4", 3, TEST_MESSAGES)


# Test for empty messages
def test_empty_messages():
    with pytest.raises(ValueError):
        request_chat_completion("gpt-4", 0.5, [])


# Test for invalid message structure
def test_invalid_message_structure():
    with pytest.raises(ValueError):
        request_chat_completion("gpt-4", 0.5, [{"role": "system"}])


# Test for invalid message role
def test_invalid_message_role():
    with pytest.raises(ValueError):
        request_chat_completion(
            "gpt-4", 0.5, [{"role": "alien", "content": "this is a test"}]
        )


# Test for invalid function name
def test_invalid_function_name():
    with pytest.raises(ValueError):
        request_chat_completion(
            "gpt-4", 0.5, TEST_MESSAGES, [{"description": "Get the current weather"}]
        )


# Test that valid args don't raise exceptions
def test_valid_args():
    try:
        with patch("openai.ChatCompletion.create") as mock_create:
            mock_create.return_value = MOCK_OPENAI_CHAT_COMPLETION_RESPONSE
            request_chat_completion("gpt-4", 0.5, TEST_MESSAGES)
            request_chat_completion("gpt-4", 0.5, TEST_MESSAGES, [TEST_FUNCTION])
    except Exception as e:
        pytest.fail(f"An exception {e} was raised during the test.")


def test_basic_request_chat_completion():
    with patch("openai.ChatCompletion.create") as mock_create:
        mock_create.return_value = MOCK_OPENAI_CHAT_COMPLETION_RESPONSE
        result = request_chat_completion(
            model="gpt-3.5-turbo",
            temperature=0.5,
            messages=TEST_MESSAGES,
        )
        assert result == MOCK_OPENAI_CHAT_COMPLETION_RESPONSE


def test_basic_request_chat_completion_with_function():
    with patch("openai.ChatCompletion.create") as mock_create:
        mock_create.return_value = MOCK_OPENAI_CHAT_COMPLETION_RESPONSE
        result = request_chat_completion(
            model="gpt-3.5-turbo",
            temperature=0.5,
            messages=TEST_MESSAGES,
            functions=[TEST_FUNCTION],
        )
        assert result == MOCK_OPENAI_CHAT_COMPLETION_RESPONSE
