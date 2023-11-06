# Toucans 🍉
Toucans is a streamlined library designed for agile and flexible prompt engineering, leveraging jinja2 for dynamic prompt templating and litellm to seamlessly connect with a wide range of language model providers.

## Getting Started
### Installation
````
pip install toucans
````

### Initialize Prompt Function
To initialize a PromptFunction:

````python
from toucans import PromptFunction

pfunc = PromptFunction(
    model="gpt-4",
    temperature=0.7,
    messages=[
        {"role": "system", "content": "You are a helpful {{ role }}."},
        {"role": "user", "content": "Answer the following question: {{ question }}"},
    ],
)
````

### Generate Completion
Generate a completion by calling the PromptFunction with the desired role and question:

````python
completion = pfunc(
    role="Software Developer", 
    question="What is clean code?"
)
````

### Save Prompt Function
To save the initialized PromptFunction to a directory:

````python
pfunc.push_to_dir("./prompt_save_dir/")
````

### Load Saved Prompt Function
To load a saved PromptFunction from a directory:

````python
pfunc = PromptFunction.from_dir("./prompt_save_dir/")
````

By following these steps, you can easily initialize, save, and load a PromptFunction for your needs.