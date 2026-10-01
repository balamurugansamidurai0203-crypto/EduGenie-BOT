"""
EduGenie - Gemini AI Client

Centralized Google Gemini API integration.
"""

import json
import os
import re
from typing import Any

from dotenv import load_dotenv
from google import genai

load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6LuJqNztvycpcooyGyuW8JPhyMDjtBecBIDDXudQGRZpg").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

_client = None


def get_client():
    """
    Create and cache the Gemini client.
    """

    global _client

    if _client is not None:
        return _client

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Create a .env file and add your Gemini API key."
        )

    _client = genai.Client(api_key=GEMINI_API_KEY)

    return _client


def generate_text(
    prompt: str,
    temperature: float = 0.4,
) -> str:
    """
    Generate normal text using Gemini.
    """

    client = get_client()

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config={
            "temperature": temperature,
        },
    )

    text = getattr(response, "text", None)

    if not text:
        raise RuntimeError("Gemini returned an empty response.")

    return text.strip()


def clean_json_block(text: str) -> str:
    """
    Remove Markdown code fences from a JSON response.

    Example:

    ```json
    {...}
    ```

    becomes:

    {...}
    """

    cleaned = text.strip()

    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    cleaned = re.sub(
        r"\s*```$",
        "",
        cleaned,
    )

    return cleaned.strip()


def generate_json(
    prompt: str,
    temperature: float = 0.2,
) -> Any:
    """
    Generate and parse JSON from Gemini.
    """

    client = get_client()

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config={
            "temperature": temperature,
            "response_mime_type": "application/json",
        },
    )

    text = getattr(response, "text", None)

    if not text:
        raise RuntimeError("Gemini returned an empty JSON response.")

    cleaned = clean_json_block(text)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Gemini returned invalid JSON: {exc}"
        ) from exc