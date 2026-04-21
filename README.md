# Med360 Patient AI

AI intelligence layer for the Med360 patient app. A FastAPI + MongoDB backend that helps patients describe symptoms, understand medical reports, and navigate to the right care.

## What it does
- Conversational symptom intake with guided follow-up questions
- Medical report interpretation (PDF/image → plain language)
- Care pathway recommendation with urgency and red flag detection

## Tech stack
- Python 3.10, FastAPI, MongoDB (motor), OpenAI GPT-4o, pdfplumber

## Getting started
```bash
cp .env.example .env        # add your keys
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Docs
See the `docs/` folder — CONTEXT, PROGRESS, and DECISIONS notes.

## Scope
This repo is the AI service layer only. Auth, frontend, and deployment are handled separately.
