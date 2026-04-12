# Embedding Similarity Python

Compares one source sentence against several candidate sentences using LangChain's `OpenAIEmbeddings` wrapper, then ranks them by cosine similarity.

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
