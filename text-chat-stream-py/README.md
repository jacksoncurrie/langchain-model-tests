# Text Chat Stream Python

Streams a plain text chat request through LangChain's `ChatOpenAI` wrapper to a chat completions compatible endpoint.

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
