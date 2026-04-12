from __future__ import annotations

import base64
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

EXAMPLE_DIR = Path(__file__).resolve().parent
REPO_ROOT = EXAMPLE_DIR.parent


def get_mime_type(file_path: Path) -> str:
    extension = file_path.suffix.lower()
    mime_type = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }.get(extension)
    if mime_type is None:
        raise RuntimeError(
            f'Unsupported image extension "{extension or "(none)"}". Supported: .jpg, .jpeg, .png, .webp'
        )
    return mime_type


def get_config() -> dict[str, str]:
    load_dotenv(EXAMPLE_DIR / ".env")
    load_dotenv(REPO_ROOT / ".env")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "sk-your-openai-api-key-here":
        raise RuntimeError(
            "Missing OPENAI_API_KEY. Update the root or local .env file before running this example."
        )

    image_path = os.getenv("VISION_IMAGE_PATH", "sample-cat.jpg")
    image_url = image_path

    if not image_path.startswith("http://") and not image_path.startswith("https://"):
        image_file_path = EXAMPLE_DIR / image_path
        if not image_file_path.exists():
            raise RuntimeError(f"Image file not found: {image_file_path}")
        image_bytes = image_file_path.read_bytes()
        mime_type = get_mime_type(image_file_path)
        image_path = str(image_file_path)
        image_url = (
            f"data:{mime_type};base64,{base64.b64encode(image_bytes).decode('utf-8')}"
        )

    return {
        "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        "api_key": api_key,
        "model": os.getenv("VISION_CHAT_MODEL", "gpt-4.1-mini"),
        "image_label": image_path,
        "image_url": image_url,
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
    prompt = "What animal is in this image? Answer with one short sentence."

    response = llm.invoke(
        [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": config["image_url"]}},
                ],
            }
        ]
    )
    model_name = response.response_metadata.get("model_name", config["model"])

    print("Vision chat example")
    print("-------------------")
    print(f"Base URL: {config['base_url']}")
    print(f"Model: {model_name}")
    print(f"Image input: {config['image_label']}")
    print(f"Prompt: {prompt}")
    print(f"Response: {response.text.strip() or '(empty)'}")


if __name__ == "__main__":
    main()
