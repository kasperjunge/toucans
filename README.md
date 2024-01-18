<h1 align="center">
<img src="static/img/logo.png" width="250">
</h1>

No bullshit prompt engineering using jinja2 for dynamic prompt templating and LiteLLM to seamlessly use a wide range of LLM providers.

## Getting Started

### Installation

````
pip install toucans
````

### Usage

Initialize a PromptFunction:

````python
from toucans import PromptFunction

sentiment = PromptFunction(
    model="gpt-4",
    temperature=0.7,
    messages=[
        {"role": "system", "content": "You are a helpful mood-sensitive agent."},
        {"role": "user", "content": "Determine the sentiment of the sentence: {{ sentence }}"},
    ],
)
````

### Generate Completion

Generate a completion by calling the PromptFunction with a sentence:

````python
completion = sentiment(sentence="I'm so happy!")
````

### Batch Generate Completions in Parallel

````python
batch_args = [
    {"sentence": "Toucans is nice Python package!"}, 
    {"sentence": "I hate bloated prompt engineering frameworks!"}
]

completion_batch = sentiment.batch_call(batch_args=batch_args)
````

### Local PromptFunction Serialization

Save/load the PromptFunction to a directory:

````python
# Push to dir (not implemented yet)
sentiment.push_to_dir("./sentiment/")

# Load from dir (not implemented yet)
sentiment = PromptFunction.from_dir("./sentiment/")
````

### Toucans Hub

Push/pull the PromptFunction from the [toucans hub](https://github.com/kasperjunge/toucans-hub):

````python
# Push to hub
sentiment.push_to_hub("juunge/sentiment")

# Load from hub
sentiment = PromptFunction.from_hub("juunge/sentiment/")

````

For now,loading from the [Toucans Hub](https://github.com/kasperjunge/toucans-hub) requires hosting an instance of it yourself and  set the HUB_API_URL environment variable.
