"""
EduGenie API tests.

These tests mock the AI modules so that the API structure
can be tested without consuming a Gemini API request.
"""

from fastapi.testclient import TestClient

import main


client = TestClient(main.app)


def test_home_page():
    response = client.get("/")

    assert response.status_code == 200

    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"

    assert data["application"] == "EduGenie"


def test_qa(monkeypatch):

    monkeypatch.setattr(
        main,
        "answer_question",
        lambda question:
            "The Pacific Ocean is the largest ocean."
    )

    response = client.post(
        "/qa",
        json={
            "question":
                "Which is the largest ocean?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True

    assert "Pacific" in data["result"]


def test_explain(monkeypatch):

    monkeypatch.setattr(
        main,
        "explain_topic",
        lambda topic:
            "Pythagoras theorem relates the sides of a right triangle."
    )

    response = client.post(
        "/explain",
        json={
            "topic":
                "Pythagoras theorem"
        },
    )

    assert response.status_code == 200

    assert response.json()["success"] is True


def test_summary(monkeypatch):

    monkeypatch.setattr(
        main,
        "summarize_text",
        lambda text:
            "This is a concise summary."
    )

    response = client.post(
        "/summarize",
        json={
            "text":
                "A long educational passage about science."
        },
    )

    assert response.status_code == 200

    assert response.json()["success"] is True


def test_quiz(monkeypatch):

    fake_questions = [
        {
            "question": "What is Python?",
            "options": [
                "Programming language",
                "Database",
                "Operating system",
                "Browser",
            ],
            "answer": "Programming language",
            "explanation":
                "Python is a programming language.",
        },
        {
            "question": "What is HTML?",
            "options": [
                "Markup language",
                "Database",
                "Compiler",
                "Operating system",
            ],
            "answer": "Markup language",
            "explanation":
                "HTML structures web pages.",
        },
        {
            "question": "What is CSS?",
            "options": [
                "Styling language",
                "Database",
                "Programming language",
                "Server",
            ],
            "answer": "Styling language",
            "explanation":
                "CSS styles web pages.",
        },
    ]

    monkeypatch.setattr(
        main,
        "generate_quiz",
        lambda text:
            fake_questions,
    )

    response = client.post(
        "/quiz",
        json={
            "text":
                "Python, HTML and CSS are used in web development."
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True

    assert len(data["questions"]) == 3

    for question in data["questions"]:

        assert len(question["options"]) == 4

        assert (
            question["answer"]
            in question["options"]
        )


def test_learning_path(monkeypatch):

    monkeypatch.setattr(
        main,
        "get_learning_recommendations",
        lambda topic, level:
            "Begin with fundamentals, then move to advanced topics."
    )

    response = client.post(
        "/learn/recommendations",
        json={
            "topic": "SQL",
            "level": "Beginner",
        },
    )

    assert response.status_code == 200

    assert response.json()["success"] is True


def test_empty_question_rejected():

    response = client.post(
        "/qa",
        json={
            "question": ""
        },
    )

    assert response.status_code == 422