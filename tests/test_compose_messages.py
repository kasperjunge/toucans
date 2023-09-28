import pytest
from jinja2 import Template

from toucans.prompt import compose_messages

# Will the API answer if only a system message is sent?

prompt = "Test prompt."
template = "Test template {{ foo }} {{ bar }}."
template_with_no_args = "Test template."
system_message = "Test system message."
system_message_with_args = "Test system message with args {{ foo }} {{ bar }}."
test_args = {"foo": "egg", "bar": "spam"}
rendered_template = Template(template).render(**test_args)
rendered_system_message_with_args = Template(system_message_with_args).render(
    **test_args
)


def test_prompt():
    messages = compose_messages(prompt=prompt)
    assert len(messages) == 1
    assert isinstance(messages, list)
    assert isinstance(messages[0], dict)
    assert "Human" in messages[0]
    assert messages[0]["Human"] == prompt


def test_template():
    messages = compose_messages(
        template=template,
        template_args=test_args,
    )
    assert len(messages) == 1
    assert isinstance(messages, list)
    assert isinstance(messages[0], dict)
    assert "Human" in messages[0]
    assert messages[0]["Human"] == rendered_template


def test_system_message_only():
    messages = compose_messages(
        system_message=system_message,
    )
    assert len(messages) == 1
    assert isinstance(messages, list)
    assert isinstance(messages[0], dict)
    assert "System" in messages[0]
    assert messages[0]["System"] == system_message


def test_prompt_and_system_message():
    messages = compose_messages(
        prompt=prompt,
        system_message=system_message,
    )
    assert isinstance(messages, list)
    assert len(messages) == 2
    assert isinstance(messages[0], dict)
    assert isinstance(messages[1], dict)
    assert "System" in messages[0]
    assert "Human" in messages[1]
    assert messages[0]["System"] == system_message
    assert messages[1]["Human"] == prompt


def test_prompt_and_system_message_with_args():
    messages = compose_messages(
        prompt=prompt,
        system_message=system_message_with_args,
        system_message_args=test_args,
    )
    assert isinstance(messages, list)
    assert len(messages) == 2
    assert isinstance(messages[0], dict)
    assert isinstance(messages[1], dict)
    assert "System" in messages[0]
    assert "Human" in messages[1]
    assert messages[0]["System"] == rendered_system_message_with_args
    assert messages[1]["Human"] == prompt


def test_template_and_system_message():
    messages = compose_messages(
        template=template,
        template_args=test_args,
        system_message=system_message,
    )
    assert isinstance(messages, list)
    assert len(messages) == 2
    assert isinstance(messages[0], dict)
    assert isinstance(messages[1], dict)
    assert "System" in messages[0]
    assert "Human" in messages[1]
    assert messages[0]["System"] == system_message
    assert messages[1]["Human"] == rendered_template


def test_template_and_system_message_with_args():
    messages = compose_messages(
        template=template,
        template_args=test_args,
        system_message=system_message_with_args,
        system_message_args=test_args,
    )
    assert isinstance(messages, list)
    assert len(messages) == 2
    assert isinstance(messages[0], dict)
    assert isinstance(messages[1], dict)
    assert "System" in messages[0]
    assert "Human" in messages[1]
    assert messages[0]["System"] == rendered_system_message_with_args
    assert messages[1]["Human"] == rendered_template


# ---------------------------------------------------------------------------- #
#                                 Failure Tests                                #
# ---------------------------------------------------------------------------- #


def test_prompt_template_fail():
    with pytest.raises(ValueError):
        compose_messages(prompt, template, test_args)


def test_render_template_with_no_args():
    with pytest.raises(ValueError):
        compose_messages(
            template=template_with_no_args,
            template_args=test_args,
        )


def test_render_system_message_with_no_args():
    with pytest.raises(ValueError):
        compose_messages(
            template=system_message,
            system_message_args=test_args,
        )


# ---------------------------------------------------------------------------- #
#                                     TODO                                     #
# ---------------------------------------------------------------------------- #


# def test_only_system_message_args_fail():
#     with pytest.raises(ValueError):
#         compose_messages(system_message_args=test_args)


# def test_only_template_args_fail():
#     with pytest.raises(ValueError):
#         compose_messages(template_args=test_args)


# def test_template_no_args_fail():
#     with pytest.raises(ValueError):
#         compose_messages(template=template_with_no_args, template_args=test_args)


# def test_system_message_args_missing_fail():
#     with pytest.raises(ValueError):
#         compose_messages(
#             template=template,
#             system_message=system_message_with_args,
#             system_message_args=test_args,
#         )


# def test_template_or_system_message_args_missing_fail():
#     with pytest.raises(ValueError):
#         compose_messages(
#             template=template,
#             system_message=system_message_with_args,
#             template_args=test_args,
#         )


# def test_template_and_system_message_requires_args_fail():
#     with pytest.raises(ValueError):
#         compose_messages(template=template, system_message=system_message_with_args)


# def test_system_message_requires_args_fail():
#     with pytest.raises(ValueError):
#         compose_messages(system_message=system_message_with_args)
