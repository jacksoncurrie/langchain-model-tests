from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import OpenAI
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
        "model": os.getenv("TEXT_COMPLETION_MODEL", "gpt-3.5-turbo-instruct"),
    }


def main() -> None:
    config = get_config()
    llm = OpenAI(
        model=config["model"],
        temperature=0,
        max_tokens=1024,
        api_key=SecretStr(config["api_key"]),
        base_url=config["base_url"],
    )
    prompt = "I like soup because"

    completion = llm.invoke(prompt)

    print("Text completion example")
    print("-----------------------")
    print(f"Base URL: {config['base_url']}")
    print(f"Model: {config['model']}")
    print(f"Prompt: {prompt}")
    print(f"Completion: {completion.strip() if completion else '(empty)'}")


if __name__ == "__main__":
    main()
