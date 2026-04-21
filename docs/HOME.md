---
tags: [home, index]
---

# Med360 Patient AI

> A patient-facing AI backend for the Med360 home-based primary care platform.
> Not a diagnosis engine — a guidance and navigation layer.

---

## Start Here

| Note | What it's for |
|------|--------------|
| [[CONTEXT]] | Full project orientation — read this first every session |
| [[PROGRESS]] | Live checklist of what's built, tested, and next |
| [[DECISIONS]] | Why we made each architectural choice |
| [[SESSION_LOG]] | Running history of what changed each session |
| [[ROADMAP]] | Future phases and feature ideas |
| [[PROBLEM_STATEMENT]] | Original V1 scope, goals, and success criteria |

---

## Reference (auto-generated)

| Note | What it's for |
|------|--------------|
| [[API_REFERENCE]] | All endpoints — request/response schemas, curl examples |
| [[MODULES]] | Module architecture, function signatures, data flow |
| [[DATA_MODELS]] | All Pydantic models with field tables and JSON examples |

---

## Current Status — 2026-04-21

3 features fully built and tested. **42 tests passing.**

- [x] **Recommender** — one-shot: patient info → urgency + specialist pathway + red flags
- [x] **Report Interpreter** — PDF/TXT upload → structured findings + plain-language explanation. Vision fallback for scanned PDFs via GPT-4o.
- [x] **Chat (Medi)** — multi-turn conversation. Asks follow-up questions, then fires the full recommender and renders the structured panel inline.

---

## Running the App

```bash
# API
uvicorn app.main:app --reload
# open http://localhost:8000/docs for Swagger UI

# CLI
python cli.py recommend     # one-shot specialist recommendation
python cli.py interpret     # interpret a PDF or TXT report
python cli.py chat          # conversational chat with Medi
```

---

## Tech Stack

| Layer | Choice |
|-------|--------|
| API | FastAPI 0.115 |
| AI | OpenAI GPT-4o via `beta.chat.completions.parse()` |
| Storage | JSON files in `data/` (MongoDB later) |
| PDF parsing | pdfplumber (text) + pymupdf (vision fallback) |
| Tests | pytest + pytest-asyncio (42 passing) |
| Python | 3.10, `.venv` at project root |
