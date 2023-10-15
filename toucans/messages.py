from jinja2 import Template

from .utils import extract_template_args


def create_messages(
    prompt: str = None,
    prompt_template: str = None,
    prompt_template_args: dict = None,
    system_message: str = None,
    system_message_template: str = None,
    system_message_template_args: str = None,
):
    """Create messages for OpenAI chat completion."""

    validate_args(
        prompt,
        prompt_template,
        prompt_template_args,
        system_message,
        system_message_template,
        system_message_template_args,
    )

    messages = []
    if system_message_template:
        if system_message_template_args:
            rendered_system_message = Template(system_message_template).render(
                **system_message_template_args
            )
            messages.append({"role": "system", "content": rendered_system_message})

    if system_message:
        messages.append({"role": "system", "content": system_message})

    if prompt_template:
        rendered_prompt_template = Template(prompt_template).render(
            **prompt_template_args
        )
        messages.append({"role": "user", "content": rendered_prompt_template})

    if prompt:
        messages.append({"role": "user", "content": prompt})

    return messages


def validate_args(
    prompt,
    prompt_template,
    prompt_template_args,
    system_message,
    system_message_template,
    system_message_template_args,
):
    """Validates the input arguments for the create_messages function."""

    if system_message and system_message_template:
        raise ValueError(
            "Cannot provide both system_message and system_message_template together!"
        )
    if prompt and prompt_template:
        raise ValueError("Cannot provide both prompt and prompt_template together!")

    if prompt_template_args and not prompt_template:
        raise ValueError("Template args provided without a corresponding template!")

    if (
        prompt_template
        and not extract_template_args(prompt_template)
        and prompt_template_args
    ):
        raise ValueError(
            "Template provided doesn't require args, but template args given!"
        )

    if system_message_template_args and not system_message_template:
        raise ValueError(
            "System message args provided without a corresponding system message!"
        )

    if (
        prompt_template
        and extract_template_args(prompt_template)
        and not prompt_template_args
    ):
        raise ValueError("Template requires args but none provided!")

    if (
        system_message
        and extract_template_args(system_message)
        and not system_message_template_args
    ):
        raise ValueError("System message requires args but none provided!")
