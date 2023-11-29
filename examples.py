from toucans import PromptFunction

# ---------------------------------------------------------------------------- #
#                      Initialize and save Prompt Function                     #
# ---------------------------------------------------------------------------- #

# init prompt function
prompt_func = PromptFunction(
    model="gpt-4",
    temperature=0.7,
    messages=[
        {"role": "system", "content": "You are a helpful {{ role }}."},
        {"role": "user", "content": "Answer the following question: {{ question }}"},
    ],
)

# generate completion
completion = prompt_func(role="Software Developer", question="What is clean code?")

# save to directory
prompt_func.push_to_dir("./prompt_save_dir/")

# ---------------------------------------------------------------------------- #
#                          Load saved Prompt Function                          #
# ---------------------------------------------------------------------------- #

# load from directory
prompt_func = PromptFunction.from_dir("./prompt_save_dir/")
