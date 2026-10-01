"""
EduGenie - Quiz Generation Module
"""

from typing import Any

from ai_client import generate_json


def _validate_quiz(data: Any) -> list[dict]:
    """
    Validate Gemini's quiz JSON structure.
    """

    if isinstance(data, dict):
        questions = data.get("questions")

        if questions is None:
            raise ValueError(
                "Quiz JSON must contain a 'questions' field."
            )
    elif isinstance(data, list):
        questions = data
    else:
        raise ValueError("Invalid quiz response.")

    if not isinstance(questions, list):
        raise ValueError("'questions' must be a list.")

    if len(questions) != 3:
        raise ValueError(
            f"Expected exactly 3 questions, got {len(questions)}."
        )

    validated = []

    for index, question in enumerate(questions, start=1):
        if not isinstance(question, dict):
            raise ValueError(
                f"Question {index} must be an object."
            )

        question_text = str(
            question.get("question", "")
        ).strip()

        options = question.get("options")

        answer = str(
            question.get("answer", "")
        ).strip()

        explanation = str(
            question.get("explanation", "")
        ).strip()

        if not question_text:
            raise ValueError(
                f"Question {index} has no question text."
            )

        if not isinstance(options, list):
            raise ValueError(
                f"Question {index} options must be a list."
            )

        if len(options) != 4:
            raise ValueError(
                f"Question {index} must have exactly 4 options."
            )

        options = [
            str(option).strip()
            for option in options
        ]

        if not answer:
            raise ValueError(
                f"Question {index} has no correct answer."
            )

        if answer not in options:
            raise ValueError(
                f"Question {index} answer must match one "
                "of the four options."
            )

        validated.append(
            {
                "question": question_text,
                "options": options,
                "answer": answer,
                "explanation": explanation,
            }
        )

    return validated


def generate_quiz(content: str) -> list[dict]:
    """
    Generate exactly three MCQs with four options each.
    """

    content = content.strip()

    if not content:
        raise ValueError("Quiz content cannot be empty.")

    prompt = f"""
You are EduGenie, an educational quiz generator.

Create exactly 3 multiple-choice questions from the
following educational content.

Each question must have exactly 4 options.

Return ONLY valid JSON.

Required format:

{{
  "questions": [
    {{
      "question": "Question text",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "answer": "Correct option exactly as written",
      "explanation": "Short explanation"
    }}
  ]
}}

Rules:
- Exactly 3 questions.
- Exactly 4 options per question.
- Only one correct answer.
- The correct answer must exactly match one option.
- Questions must be based only on the supplied content.
- Make distractors plausible.
- Avoid ambiguous questions.

Content:
{content}
"""

    data = generate_json(prompt, temperature=0.25)

    return _validate_quiz(data)