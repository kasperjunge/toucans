# Toucans

## Usage Examples 👩‍💻
How to use toucans for swift prompt development.
### Vanilla
```python
prompt = Prompt(model="gpt-3.5-turbo")
response = prompt("Hej med dig!")
```

### Template
```python
template = "Determine sentiment: {{ sentence }}"
prompt = Prompt(
    model="gpt-4",
    template=template,
)
out = prompt(sentence="I love toucans!")
```


