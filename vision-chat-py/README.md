# Vision Chat Python

Sends a text plus image request through LangChain's `ChatOpenAI` wrapper to a chat completions compatible endpoint.

```bash
uv sync
uv run python main.py
```

You can use variables for the local env:

```bash
cp example.env .env # To use local environment variables
```

Set `VISION_IMAGE_PATH` to either:

- an `http/https` URL
- a relative local path (for example [sample-cat.jpg](./sample-cat.jpg))

Config precedence:

- shell-passed env vars
- this folder's [.env](./.env)
- the root [.env](../.env)
