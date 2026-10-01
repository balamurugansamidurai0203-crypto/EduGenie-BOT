"""
EduGenie - FastAPI Application
"""

from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from explanation_module import explain_topic
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie",
    description=(
        "Google Gemini powered AI learning assistant "
        "for Q&A, explanations, quizzes, summaries, "
        "and personalized learning paths."
    ),
    version="1.0.0",
)


app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)


templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# ============================================================
# Request Models
# ============================================================

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=30000,
    )


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=10000,
    )


class TopicRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=10000,
    )


class LearningRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=5000,
    )

    level: str = Field(
        default="Beginner",
        min_length=1,
        max_length=50,
    )


# ============================================================
# Frontend
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )


# ============================================================
# Health Check
# ============================================================

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "application": "EduGenie",
        "version": "1.0.0",
    }


# ============================================================
# Q&A
# ============================================================

@app.post("/qa")
async def qa(request: QuestionRequest):
    try:
        result = answer_question(request.question)

        return {
            "success": True,
            "result": result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Q&A generation failed: {exc}",
        ) from exc


# ============================================================
# Explanation
# ============================================================

@app.post("/explain")
async def explain(request: TopicRequest):
    try:
        result = explain_topic(request.topic)

        return {
            "success": True,
            "result": result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Explanation generation failed: {exc}",
        ) from exc


# ============================================================
# Quiz
# ============================================================

@app.post("/quiz")
async def quiz(request: TextRequest):
    try:
        questions = generate_quiz(request.text)

        return {
            "success": True,
            "questions": questions,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Quiz generation failed: {exc}",
        ) from exc


# ============================================================
# Summary
# ============================================================

@app.post("/summarize")
async def summarize(request: TextRequest):
    try:
        result = summarize_text(request.text)

        return {
            "success": True,
            "result": result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Summarization failed: {exc}",
        ) from exc


# ============================================================
# Learning Recommendations
# ============================================================

@app.post("/learn/recommendations")
async def learning_recommendations(
    request: LearningRequest,
):
    try:
        result = get_learning_recommendations(
            topic=request.topic,
            level=request.level,
        )

        return {
            "success": True,
            "result": result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Learning path generation failed: {exc}",
        ) from exc