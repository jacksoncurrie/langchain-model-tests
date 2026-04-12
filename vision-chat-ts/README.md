# Vision Chat TS

Sends a text plus image request through LangChain's `ChatOpenAI` wrapper to a chat completions compatible endpoint.

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

Set `VISION_IMAGE_PATH` to either:

- an `http/https` URL
- a relative or absolute local path (for example [sample-cat.jpg](./sample-cat.jpg))

Config precedence:

- shell-passed env vars
- this folder's [.env](./.env)
- the root [.env](../.env)
