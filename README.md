# Toucans 🍉

## Usage Examples 👩‍💻
How to use toucans for swift prompt development.
### Vanilla
```python
prompt = Prompt(model="gpt-4")
response = prompt("What is the meaning of life?")
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


