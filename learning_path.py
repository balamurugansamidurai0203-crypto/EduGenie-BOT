"""
EduGenie - Personalized Learning Path Module
"""

from ai_client import generate_text


def get_learning_recommendations(
    topic: str,
    level: str = "Beginner",
) -> str:
    """
    Generate a structured learning path.
    """

    topic = topic.strip()
    level = level.strip() or "Beginner"

    if not topic:
        raise ValueError("Learning topic cannot be empty.")

    prompt = f"""
You are EduGenie, a personalized educational mentor.

Create a structured learning path for:

Topic:
{topic}

Learner level:
{level}

The learning path should move from beginner to advanced.

Include:

1. Learning goal
2. Prerequisites
3. Beginner stage
4. Intermediate stage
5. Advanced stage
6. Suggested timeline
7. Practice activities
8. Project ideas
9. Recommended resources
10. Final revision strategy

For every stage:
- Explain what to learn.
- Give practical activities.
- Mention what the learner should be able to do afterward.

Keep the recommendations realistic and student-friendly.

Do not invent specific URLs unless you are certain they are valid.
"""

    return generate_text(prompt, temperature=0.45)