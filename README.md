# LangChain Model Tests

Small standalone templates for testing an OpenAI-compatible API across common request styles, including streaming chat, using LangChain's OpenAI integrations.

Each folder is self-contained and copyable:

- its own config files
- its own ignore rules
- its own package manager setup

There is also a shared root default env:

```bash
cp example.env .env # To use root environment variables
```

Folders:

- [embedding-similarity-ts](./embedding-similarity-ts)
- [embedding-similarity-py](./embedding-similarity-py)
- [text-chat-ts](./text-chat-ts)
- [text-chat-py](./text-chat-py)
- [text-chat-stream-ts](./text-chat-stream-ts)
- [text-chat-stream-py](./text-chat-stream-py)
- [text-completion-ts](./text-completion-ts)
- [text-completion-py](./text-completion-py)
- [vision-chat-ts](./vision-chat-ts)
- [vision-chat-py](./vision-chat-py)

Each folder can be used on its own:

TypeScript:

```bash
cd text-chat-ts

npm install
npm run build
npm start
```

Python:

```bash
cd text-chat-py

uv sync
uv run python main.py
```

Env precedence is:

1. values passed in from the shell
2. the folder-local `.env`
3. the root `.env`
