# Toucans 🍉

## Usage Examples 👩‍💻
How to use toucans for swift prompt development.
### Vanilla
```python
prompt = Prompt(model="gpt-4")
response = prompt("What is the meaning of life?")
```

### Prompt Template
```python
prompt_template = "Determine sentiment: {{ sentence }}"
prompt = Prompt(
    model="gpt-4",
    prompt_template=prompt_template,
)
out = prompt(sentence="I love toucans!")
```
### System Message Template
```python
system_message_template = "You are a helpful {{ role }}."
prompt = Prompt(
    model="gpt-4",
    system_message_template=system_message_template,
)
out = prompt(role="evil clown")
```

### Prompt Template + System Message Template
```python
prompt_template = "Determine sentiment: {{ sentence }}"
system_message_template = "You are a helpful {{ role }}."
prompt = Prompt(
    model="gpt-4",
    system_message_template=system_message_template,
)
out = prompt(role="evil clown", "This is a little wierd..")
```

### Prompt Template + Output Schema
```python
prompt_template = "Determine sentiment: {{ sentence }}"
output_schema = {
    "name": "sentiment",
    "description": "Determine sentiment of a sentence.",
    "parameters": {
        "type": "object",
        "properties": {
            "sentiment": {
                "type": "string",
                "description": "The sentiment of the sentence.",
                "enum": ["positive", "neutral","negative"]
            }
        }
    }
}
prompt = Prompt(
    model="gpt-4",
    prompt_template=prompt_template,
    output_schema=
)
out = prompt(sentence="I love toucans!")