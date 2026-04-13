from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
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
        "model": os.getenv("TEXT_CHAT_MODEL", "gpt-4.1-mini"),
    }


def main() -> None:
    config = get_config()
    llm = ChatOpenAI(
        model=config["model"],
        temperature=0,
        api_key=SecretStr(config["api_key"]),
        base_url=config["base_url"],
        max_retries=0,
    )
    prompt = "Explain why carrots are healthy."

    print("Text chat stream example")
    print("------------------------")
    print(f"Base URL: {config['base_url']}")
    print(f"Model: {config['model']}")
    print(f"Prompt: {prompt}")
    print("Response: ", end="", flush=True)

    saw_content = False

    for chunk in llm.stream([{"role": "user", "content": prompt}]):
        content = chunk.text
        if content:
            saw_content = True
            print(content, end="", flush=True)

    if not saw_content:
        print("(empty)", end="")

    print()


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        try:
            sys.stdout.close()
        finally:
            raise SystemExit(0)
