from toucans import PromptFunction

# ---------------------------------------------------------------------------- #
#                      Initialize and save Prompt Function                     #
# ---------------------------------------------------------------------------- #

# init prompt function
pfunc = PromptFunction(
    model="gpt-4",
    temperature=0.7,
    messages=[
        {"role": "system", "content": "You are a helpful {{ role }}."},
        {"role": "user", "content": "Answer the following question: {{ question }}"},
    ],
)

# generate completion
completion = pfunc(role="Software Developer", question="What is clean code?")

# save to directory
pfunc.push_to_dir("./prompt_save_dir/")

# ---------------------------------------------------------------------------- #
#                          Load saved Prompt Function                          #
# ---------------------------------------------------------------------------- #

# load from directory
pfunc = PromptFunction.from_dir("./prompt_save_dir/")
