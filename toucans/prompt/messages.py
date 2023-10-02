from jinja2 import Template

from ..utils import extract_template_args


def validate_args(
    prompt,
    template,
    template_args,
    system_message,
    system_message_args,
):
    """Validates the input arguments for the create_messages function."""

    if prompt and template:
        raise ValueError("Cannot provide both prompt and template together!")

    if template_args and not template:
        raise ValueError("Template args provided without a corresponding template!")

    if template and not extract_template_args(template) and template_args:
        raise ValueError(
            "Template provided doesn't require args, but template args given!"
        )

    if system_message_args and not system_message:
        raise ValueError(
            "System message args provided without a corresponding system message!"
        )

    if template and extract_template_args(template) and not template_args:
        raise ValueError("Template requires args but none provided!")

    if (
        system_message
        and extract_template_args(system_message)
        and not system_message_args
    ):
        raise ValueError("System message requires args but none provided!")


def create_messages(
    prompt: str = None,
    template: str = None,
    template_args: dict = None,
    system_message: str = None,
    system_message_args: str = None,
):
    """Create messages for OpenAI chat completion."""

    validate_args(
        prompt,
        template,
        template_args,
        system_message,
        system_message_args,
    )

    messages = []

    # System Message
    if system_message:
        if system_message_args:
            rendered_system_message = Template(system_message).render(
                **system_message_args
            )
            messages.append({"role": "system", "content": rendered_system_message})
        else:
            messages.append({"role": "system", "content": system_message})

    # Template
    if template:
        rendered_template = Template(template).render(**template_args)
        messages.append({"role": "user", "content": rendered_template})

    # Prompt
    if prompt:
        messages.append({"role": "user", "content": prompt})

    return messages
