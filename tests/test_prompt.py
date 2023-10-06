import os

import pytest

from toucans import Prompt

from .utils import PROMPT_TEMPLATE, TEST_MODEL, TEST_PROMPT

os.environ["OPENAI_API_KEY"] = "..."


def test_prompt_and_prompt_template_fail():
    prompt = Prompt(
        model=TEST_MODEL,
        prompt_template=PROMPT_TEMPLATE,
    )

    with pytest.raises(ValueError):
        out = prompt(TEST_PROMPT)

    with pytest.raises(ValueError):
        out = prompt(TEST_PROMPT, foo="foo", bar="bar")
