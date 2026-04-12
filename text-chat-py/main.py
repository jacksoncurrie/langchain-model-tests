from __future__ import annotations

import os
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
    prompt = "Explain in one short sentence why carrots are healthy."

    response = llm.invoke([{"role": "user", "content": prompt}])
    model_name = response.response_metadata.get("model_name", config["model"])

    print("Text chat example")
    print("-----------------")
    print(f"Base URL: {config['base_url']}")
    print(f"Model: {model_name}")
    print(f"Prompt: {prompt}")
    print(f"Response: {response.text.strip() or '(empty)'}")


if __name__ == "__main__":
    main()
