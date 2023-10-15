"""Test creation of messages for OpenAI chat completion API with all combinations of input."""

import pytest

from toucans.messages import create_messages

from .utils import (
    PROMPT,
    PROMPT_TEMPLATE,
    RENDERED_PROMPT_TEMPLATE,
    RENDERED_SYSTEM_MESSAGE_TEMPLATE,
    SYSTEM_MESSAGE,
    SYSTEM_MESSAGE_TEMPLATE,
    TEST_ARGS,
)


def test_prompt():
    messages = create_messages(prompt=PROMPT)
    assert len(messages) == 1
    assert isinstance(messages, list)
    assert isinstance(messages[0], dict)
    assert "role" in messages[0]
    assert "content" in messages[0]
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == PROMPT


def test_template():
    messages = create_messages(
        prompt_template=PROMPT_TEMPLATE,
        prompt_template_args=TEST_ARGS,
    )
    assert len(messages) == 1
    assert isinstance(messages, list)
    assert isinstance(messages[0], dict)
    assert "role" in messages[0]
    assert "content" in messages[0]
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == RENDERED_PROMPT_TEMPLATE


def test_system_message_only():
    messages = create_messages(
        system_message=SYSTEM_MESSAGE,
    )
    assert len(messages) == 1
    assert isinstance(messages, list)
    assert isinstance(messages[0], dict)
    assert "role" in messages[0]
    assert "content" in messages[0]
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == SYSTEM_MESSAGE


def PROMPT_and_system_message():
    messages = create_messages(
        prompt=PROMPT,
        system_message=SYSTEM_MESSAGE,
    )
    assert isinstance(messages, list)
    assert len(messages) == 2
    assert isinstance(messages[0], dict)
    assert isinstance(messages[1], dict)
    assert "role" in messages[0]
    assert "role" in messages[1]
    assert "content" in messages[0]
    assert "content" in messages[1]
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == SYSTEM_MESSAGE
    assert messages[1]["role"] == "user"
    assert messages[1]["content"] == PROMPT


def test_prompt_and_system_message_template():
    messages = create_messages(
        prompt=PROMPT,
        system_message_template=SYSTEM_MESSAGE_TEMPLATE,
        system_message_template_args=TEST_ARGS,
    )
    assert isinstance(messages, list)
    assert len(messages) == 2
    assert isinstance(messages[0], dict)
    assert isinstance(messages[1], dict)
    assert "role" in messages[0]
    assert "role" in messages[1]
    assert "content" in messages[0]
    assert "content" in messages[1]
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == RENDERED_SYSTEM_MESSAGE_TEMPLATE
    assert messages[1]["role"] == "user"
    assert messages[1]["content"] == PROMPT


def test_template_and_system_message():
    messages = create_messages(
        prompt_template=PROMPT_TEMPLATE,
        prompt_template_args=TEST_ARGS,
        system_message=SYSTEM_MESSAGE,
    )
    assert isinstance(messages, list)
    assert len(messages) == 2
    assert isinstance(messages[0], dict)
    assert isinstance(messages[1], dict)
    assert "role" in messages[0]
    assert "role" in messages[1]
    assert "content" in messages[0]
    assert "content" in messages[1]
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == SYSTEM_MESSAGE
    assert messages[1]["role"] == "user"
    assert messages[1]["content"] == RENDERED_PROMPT_TEMPLATE


def test_prompt_template_and_system_message_template():
    messages = create_messages(
        prompt_template=PROMPT_TEMPLATE,
        prompt_template_args=TEST_ARGS,
        system_message_template=SYSTEM_MESSAGE_TEMPLATE,
        system_message_template_args=TEST_ARGS,
    )
    assert isinstance(messages, list)
    assert len(messages) == 2
    assert isinstance(messages[0], dict)
    assert isinstance(messages[1], dict)
    assert "role" in messages[0]
    assert "role" in messages[1]
    assert "content" in messages[0]
    assert "content" in messages[1]
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == RENDERED_SYSTEM_MESSAGE_TEMPLATE
    assert messages[1]["role"] == "user"
    assert messages[1]["content"] == RENDERED_PROMPT_TEMPLATE


# ---------------------------------------------------------------------------- #
#                                 Failure Tests                                #
# ---------------------------------------------------------------------------- #


def test_prompt_and_prompt_template_fail():
    with pytest.raises(ValueError):
        create_messages(PROMPT, PROMPT_TEMPLATE, TEST_ARGS)


def test_render_template_with_no_args():
    with pytest.raises(ValueError):
        create_messages(
            prompt_template=PROMPT,
            prompt_template_args=TEST_ARGS,
        )


def test_render_system_message_with_no_args():
    with pytest.raises(ValueError):
        create_messages(
            prompt_template=SYSTEM_MESSAGE,
            system_message_template_args=TEST_ARGS,
        )


def test_only_system_message_template_args_fail():
    with pytest.raises(ValueError):
        create_messages(system_message_template_args=TEST_ARGS)


def test_only_template_args_fail():
    with pytest.raises(ValueError):
        create_messages(prompt_template_args=TEST_ARGS)


def test_system_message_template_args_missing_fail():
    with pytest.raises(ValueError):
        create_messages(
            prompt_template=PROMPT_TEMPLATE,
            system_message=SYSTEM_MESSAGE_TEMPLATE,
            system_message_template_args=TEST_ARGS,
        )


def test_template_or_system_message_template_args_missing_fail():
    with pytest.raises(ValueError):
        create_messages(
            prompt_template=PROMPT_TEMPLATE,
            system_message=SYSTEM_MESSAGE_TEMPLATE,
            prompt_template_args=TEST_ARGS,
        )


def test_template_and_system_message_requires_args_fail():
    with pytest.raises(ValueError):
        create_messages(
            prompt_template=PROMPT_TEMPLATE, system_message=SYSTEM_MESSAGE_TEMPLATE
        )


def test_system_message_requires_args_fail():
    with pytest.raises(ValueError):
        create_messages(system_message=SYSTEM_MESSAGE_TEMPLATE)
