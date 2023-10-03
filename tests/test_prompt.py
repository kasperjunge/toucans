import os
import unittest.mock as mock

from litellm import mock_completion

from toucans import Prompt

from .utils import MOCK_OPENAI_CHAT_COMPLETION_RESPONSE, TEST_PROMPT

TEST_MODEL = "gpt-4"
os.environ["OPENAI_API_KEY"] = "st-23mnosdf0sdfaåndfn"


def test_vanilla():
    with mock.patch(
        "toucans.prompt.litellm.completion",
        return_value=mock_completion,
    ):
        prompt = Prompt(model=TEST_MODEL)
        reponse = prompt(TEST_PROMPT)
