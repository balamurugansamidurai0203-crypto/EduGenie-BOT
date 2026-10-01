"""
EduGenie - Question Answering Module
"""

from ai_client import generate_text


def answer_question(question: str) -> str:
    """
    Answer an academic/general educational question.
    """

    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    prompt = f"""
You are EduGenie, an educational AI assistant.

Answer the following question clearly and accurately.

Rules:
- Give a direct answer first.
- Explain the reasoning or concept briefly.
- Use simple language.
- Avoid unnecessary jargon.
- If useful, provide a small example.
- Do not invent facts.
- If the question is ambiguous, clearly state the assumption.

Student question:
{question}
"""

    return generate_text(prompt, temperature=0.3)