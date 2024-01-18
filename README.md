
<h1 align="center">
<img src="static/img/logo.png" width="250">
</h1>

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

qa_func = PromptFunction(
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
completion = qa_func(
    role="Software Developer", 
    question="What is clean code?"
)
````

### Save Prompt Function
To save the initialized PromptFunction to a directory or the [toucans hub](https://github.com/kasperjunge/toucans-hub):

````python
# Push to dir (not implemented yet)
qa_func.push_to_dir("./qa/")

# Push to toucans hub
qa_func.push_to_hub("juunge/qa")
````

### Load Saved Prompt Function
To load a saved PromptFunction from a directory or the [toucans hub](https://github.com/kasperjunge/toucans-hub):

````python
# Load from dir (not implemented yet)
qa_func = PromptFunction.from_dir("./qa/")

# Load from toucans hub
qa_func = PromptFunction.from_hub("juunge/qa")
````

Loading from [Toucans Hub](https://github.com/kasperjunge/toucans-hub) requires that you run a hub and connect to it by setting the HUB_API_URL environment variable.
