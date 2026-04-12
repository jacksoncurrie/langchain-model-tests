# Text Completion Python

Calls a text completion compatible endpoint through LangChain's `OpenAI` LLM wrapper and prints the returned completion text.

```bash
uv sync
uv run python main.py
```

You can use variables for the local env:

```bash
cp example.env .env # To use local environment variables
```

Config precedence:

- shell-passed env vars
- this folder's [.env](./.env)
- the root [.env](../.env)
