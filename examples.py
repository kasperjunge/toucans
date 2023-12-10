from dotenv import load_dotenv

from toucans import PromptFunction

load_dotenv()

name = "Q&A"

# ---------------------------------------------------------------------------- #
#                                     Push                                     #
# ---------------------------------------------------------------------------- #

prompt = PromptFunction(
    model="gpt-4",
    temperature=0.7,
    messages=[
        {"role": "system", "content": "You are a helpful {{ role }}."},
        {"role": "user", "content": "Answer the following question: {{ question }}"},
    ],
)


prompt.push_to_hub(name)

# completion = prompt(role="Software Developer", question="What is clean code?")


# ---------------------------------------------------------------------------- #
#                                     Pull                                     #
# ---------------------------------------------------------------------------- #

prompt = PromptFunction.from_hub(name)
