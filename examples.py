from toucans import Prompt

# ---------------------------------------------------------------------------- #
#                                    Vanilla                                   #
# ---------------------------------------------------------------------------- #

prompt = Prompt(model="gpt-3.5-turbo")
out = prompt("Hej med dig!")


# ---------------------------------------------------------------------------- #
#                                   Template                                   #
# ---------------------------------------------------------------------------- #

template = "Answer the following qustions: {question}"
prompt = Prompt(
    model="gpt-3.5-turbo",
    template=template,
)
out = prompt(question="What is the meaning of life?")


# ---------------------------------------------------------------------------- #
#                                System Message                                #
# ---------------------------------------------------------------------------- #

system_message = "You are a helpful assistant."
prompt = Prompt(
    model="gpt-3.5-turbo",
    system_message=system_message,
)
out = prompt("What is the meaning of life?")


# ---------------------------------------------------------------------------- #
#                           Template + System Message                          #
# ---------------------------------------------------------------------------- #

system_message = "You are a helpful chatbot."
template = "Answer the following qustions: {question}"
prompt = Prompt(
    model="gpt-3.5-turbo",
    template=template,
    system_message=system_message,
)
out = prompt(question="What is the meaning of life?")


# ---------------------------------------------------------------------------- #
#                   Template + System Message + Output Schema                  #
# ---------------------------------------------------------------------------- #

system_message = "You are a helpful chatbot."
template = "Answer the following qustions: {question}"
output_schema = {
    "function_name": "The answer!",
    "description": "Use this to answer",
    "properties": {
        "answer": {"type": "string"},
    },
    "required": ["answer"],
}
prompt = Prompt(
    model="gpt-3.5-turbo",
    template=template,
    system_message=system_message,
    output_schema=output_schema,
)
out = prompt(question="What is the meaning of life?")
