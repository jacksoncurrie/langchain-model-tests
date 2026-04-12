import path from "node:path";
import { fileURLToPath } from "node:url";
import dotenv from "dotenv";
import { ChatOpenAI } from "@langchain/openai";

function getConfig() {
  const runtimeDir = path.dirname(fileURLToPath(import.meta.url));
  const projectDir =
    path.basename(runtimeDir) === "dist"
      ? path.resolve(runtimeDir, "..")
      : runtimeDir;
  const repoRoot = path.resolve(projectDir, "..");

  dotenv.config({ path: path.join(projectDir, ".env") });
  dotenv.config({ path: path.join(repoRoot, ".env") });

  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey || apiKey === "sk-your-openai-api-key-here") {
    throw new Error(
      "Missing OPENAI_API_KEY. Update the root or local .env file before running this example.",
    );
  }

  return {
    baseURL: process.env.OPENAI_BASE_URL || "https://api.openai.com/v1",
    apiKey,
    model: process.env.TEXT_CHAT_MODEL || "gpt-4.1-mini",
  };
}

async function main(): Promise<void> {
  const config = getConfig();

  const llm = new ChatOpenAI({
    model: config.model,
    temperature: 0,
    apiKey: config.apiKey,
    configuration: {
      baseURL: config.baseURL,
    },
  });

  const prompt = "Explain in one short sentence why carrots are healthy.";

  const response = await llm.invoke([{ role: "user", content: prompt }]);

  console.log("Text chat example");
  console.log("-----------------");
  console.log(`Base URL: ${config.baseURL}`);
  console.log(`Model: ${config.model}`);
  console.log(`Prompt: ${prompt}`);
  console.log(`Response: ${response.text.trim() || "(empty)"}`);
}

main().catch((error: unknown) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
