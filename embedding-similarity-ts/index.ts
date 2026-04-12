import path from "node:path";
import { fileURLToPath } from "node:url";
import dotenv from "dotenv";
import { OpenAIEmbeddings } from "@langchain/openai";

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
    model: process.env.EMBEDDING_MODEL || "text-embedding-3-small",
  };
}

function cosineSimilarity(a: number[], b: number[]): number {
  if (a.length !== b.length) {
    throw new Error(`Vector length mismatch: ${a.length} !== ${b.length}`);
  }

  let dot = 0;
  let normA = 0;
  let normB = 0;

  for (let i = 0; i < a.length; i += 1) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }

  if (normA === 0 || normB === 0) {
    throw new Error("Cannot compare zero-length vector norms.");
  }

  return dot / (Math.sqrt(normA) * Math.sqrt(normB));
}

async function main(): Promise<void> {
  const config = getConfig();

  const embeddings = new OpenAIEmbeddings({
    model: config.model,
    apiKey: config.apiKey,
    configuration: {
      baseURL: config.baseURL,
    },
  });

  const sourceSentence = "The cat sat on the mat.";
  const candidateSentences = [
    "A kitten is sitting on a rug.",
    "A cat is resting on a mat.",
    "There is a dog playing in the yard.",
    "The stock market closed higher today.",
  ];

  const sourceEmbedding = await embeddings.embedQuery(sourceSentence);
  const candidateEmbeddings =
    await embeddings.embedDocuments(candidateSentences);

  const ranked = candidateSentences
    .map((sentence, index) => ({
      sentence,
      similarity: cosineSimilarity(sourceEmbedding, candidateEmbeddings[index]),
    }))
    .sort((a, b) => b.similarity - a.similarity);

  console.log("Embedding similarity example");
  console.log("----------------------------");
  console.log(`Base URL: ${config.baseURL}`);
  console.log(`Model: ${config.model}`);
  console.log(`Source sentence: ${sourceSentence}`);
  console.log("");
  ranked.forEach((item, index) => {
    console.log(
      `${index + 1}. ${item.similarity.toFixed(6)}  ${item.sentence}`,
    );
  });
}

main().catch((error: unknown) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
