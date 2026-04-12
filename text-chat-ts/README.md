# Text Chat TS

Sends a plain text chat request through LangChain's `ChatOpenAI` wrapper to a chat completions compatible endpoint.

```bash
npm install
npm run build
npm start
```

Dev mode:

```bash
npm run dev
```

You can use variables for the local env:

```bash
cp example.env .env # To use local environment variables
```

Config precedence:

- shell-passed env vars
- this folder's [.env](./.env)
- the root [.env](../.env)
