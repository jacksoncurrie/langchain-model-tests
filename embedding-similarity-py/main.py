from __future__ import annotations

import math
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from pydantic import SecretStr

EXAMPLE_DIR = Path(__file__).resolve().parent
REPO_ROOT = EXAMPLE_DIR.parent


def get_config() -> dict[str, str]:
    load_dotenv(EXAMPLE_DIR / ".env")
    load_dotenv(REPO_ROOT / ".env")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "sk-your-openai-api-key-here":
        raise RuntimeError(
            "Missing OPENAI_API_KEY. Update the root or local .env file before running this example."
        )

    return {
        "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        "api_key": api_key,
        "model": os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
    }


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError(f"Vector length mismatch: {len(a)} != {len(b)}")

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if norm_a == 0 or norm_b == 0:
        raise ValueError("Cannot compare zero-length vector norms.")
    return dot / (norm_a * norm_b)


def main() -> None:
    config = get_config()
    embeddings = OpenAIEmbeddings(
        model=config["model"],
        api_key=SecretStr(config["api_key"]),
        base_url=config["base_url"],
        check_embedding_ctx_length=False,
    )

    source_sentence = "The cat sat on the mat."
    candidate_sentences = [
        "A kitten is sitting on a rug.",
        "A cat is resting on a mat.",
        "There is a dog playing in the yard.",
        "The stock market closed higher today.",
    ]

    source_embedding = embeddings.embed_query(source_sentence)
    candidate_embeddings = embeddings.embed_documents(candidate_sentences)

    ranked = sorted(
        (
            {
                "sentence": sentence,
                "similarity": cosine_similarity(source_embedding, candidate_embeddings[index]),
            }
            for index, sentence in enumerate(candidate_sentences)
        ),
        key=lambda item: item["similarity"],
        reverse=True,
    )

    print("Embedding similarity example")
    print("----------------------------")
    print(f"Base URL: {config['base_url']}")
    print(f"Model: {config['model']}")
    print(f"Source sentence: {source_sentence}")
    for index, item in enumerate(ranked, start=1):
        print(f"{index}. {item['similarity']:.6f} {item['sentence']}")


if __name__ == "__main__":
    main()
