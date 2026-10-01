"""
EduGenie - Concept Explanation Module

By default this uses Gemini because it is the simplest setup.

Optional local mode:
USE_LOCAL_EXPLAINER=true

The local mode uses LaMini-Flan-T5 when the required packages
are installed.
"""

import os

from ai_client import generate_text


_LOCAL_MODEL = None


def _get_local_model():
    """
    Load the local LaMini-Flan-T5 model only when requested.
    """

    global _LOCAL_MODEL

    if _LOCAL_MODEL is not None:
        return _LOCAL_MODEL

    try:
        from transformers import pipeline

        _LOCAL_MODEL = pipeline(
            "text2text-generation",
            model="MBZUAI/LaMini-Flan-T5-783M",
            device=-1,
        )

        return _LOCAL_MODEL

    except ImportError as exc:
        raise RuntimeError(
            "Local explanation mode requires transformers and torch. "
            "Run: pip install -r requirements-local.txt"
        ) from exc


def explain_topic(topic: str) -> str:
    """
    Explain a difficult topic in beginner-friendly language.
    """

    topic = topic.strip()

    if not topic:
        raise ValueError("Topic cannot be empty.")

    use_local = (
        os.getenv("USE_LOCAL_EXPLAINER", "false").lower()
        == "true"
    )

    if use_local:
        model = _get_local_model()

        prompt = (
            "Explain the following educational topic in very simple "
            "language for a beginner. Include a short example.\n\n"
            f"Topic: {topic}"
        )

        result = model(
            prompt,
            max_new_tokens=250,
            do_sample=False,
        )

        return result[0]["generated_text"].strip()

    prompt = f"""
You are EduGenie, a patient educational teacher.

Explain this topic to a beginner:

{topic}

Structure your answer as:

1. Simple definition
2. How it works
3. Easy example
4. Important points
5. One-line summary

Use simple language suitable for a student.
"""

    return generate_text(prompt, temperature=0.35)