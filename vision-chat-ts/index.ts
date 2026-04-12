import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import dotenv from "dotenv";
import { ChatOpenAI } from "@langchain/openai";

function getMimeType(filePath: string): string {
  const extension = path.extname(filePath).toLowerCase();
  if (extension === ".jpg" || extension === ".jpeg") return "image/jpeg";
  if (extension === ".png") return "image/png";
  if (extension === ".webp") return "image/webp";
  throw new Error(
    `Unsupported image extension "${extension || "(none)"}". Supported: .jpg, .jpeg, .png, .webp`,
  );
}

async function getConfig() {
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

  let imagePath = process.env.VISION_IMAGE_PATH || "./sample-cat.jpg";
  let imageUrl = imagePath;

  if (!imagePath.startsWith("http://") && !imagePath.startsWith("https://")) {
    const imageFilePath = path.resolve(projectDir, imagePath);
    if (!fs.existsSync(imageFilePath)) {
      throw new Error(`Image file not found: ${imageFilePath}`);
    }
    const imageBytes = await fsp.readFile(imageFilePath);
    const mimeType = getMimeType(imageFilePath);
    imagePath = imageFilePath;
    imageUrl = `data:${mimeType};base64,${imageBytes.toString("base64")}`;
  }

  return {
    baseURL: process.env.OPENAI_BASE_URL || "https://api.openai.com/v1",
    apiKey,
    model: process.env.VISION_CHAT_MODEL || "gpt-4.1-mini",
    imageLabel: imagePath,
    imageUrl,
  };
}

async function main(): Promise<void> {
  const config = await getConfig();

  const llm = new ChatOpenAI({
    model: config.model,
    temperature: 0,
    apiKey: config.apiKey,
    configuration: {
      baseURL: config.baseURL,
    },
  });

  const prompt =
    "What animal is in this image? Answer with one short sentence.";

  const response = await llm.invoke([
    {
      role: "user",
      content: [
        { type: "text", text: prompt },
        { type: "image_url", image_url: { url: config.imageUrl } },
      ],
    },
  ]);

  console.log("Vision chat example");
  console.log("-------------------");
  console.log(`Base URL: ${config.baseURL}`);
  console.log(`Model: ${config.model}`);
  console.log(`Image input: ${config.imageLabel}`);
  console.log(`Prompt: ${prompt}`);
  console.log(`Response: ${response.text.trim() || "(empty)"}`);
}

main().catch((error: unknown) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
