"""
EduGenie - Text Summarization Module
"""

from ai_client import generate_text


def summarize_text(text: str) -> str:
    """
    Summarize educational content.
    """

    text = text.strip()

    if not text:
        raise ValueError("Text cannot be empty.")

    if len(text) < 80:
        prompt = f"""
Rewrite the following short educational text into a concise
and easy-to-understand summary.

Text:
{text}
"""
    else:
        prompt = f"""
Summarize the following educational passage.

Requirements:
- Preserve the important facts.
- Remove repetition.
- Use simple language.
- Keep the main ideas.
- Use bullet points when helpful.
- Do not add information that is not present in the passage.

Educational passage:
{text}
"""

    return generate_text(prompt, temperature=0.25)