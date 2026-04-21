# Med360 Patient AI — Session Context

> Claude reads this file at the start of every session to get oriented fast.

## What we're building
A **FastAPI + MongoDB AI backend** for the Med360 patient app. It is a patient-facing clinical intake and guidance system — NOT a diagnosis engine.

## Tech stack
- **FastAPI** — API layer
- **MongoDB** (motor async) — storage
- **OpenAI GPT-4o** — AI backbone
- **Python 3.10**, `.venv` already created and requirements installed
- **pdfplumber** — PDF report parsing

## Project structure (key paths)
```
app/
  main.py              — FastAPI entry point
  config.py            — Settings (reads from .env)
  database.py          — MongoDB connection
  api/v1/              — Route handlers (thin, no logic)
  core/                — Orchestrator, state extractor, session manager
  modules/
    chatbot/           — Response builder + follow-up generator
    recommender/       — Care engine + red flag detector
    report_interpreter/— PDF parser + plain-language explainer
  models/              — MongoDB document shapes
  schemas/             — Pydantic API request/response contracts
  prompts/             — All system prompts (isolated)
  services/            — OpenAI client, file service
tests/                 — Async pytest tests
docs/                  — This folder (Obsidian vault)
```

## Three core modules
1. **Chatbot** — conversational intake, follow-up questions
2. **Recommender** — urgency detection, care pathway, red flags
3. **Report Interpreter** — PDF/image parsing, plain-language explanation

## Hidden but critical layer
`clinical_state` — structured extraction from chat (chief complaint, symptoms, duration, severity, red flags, missing info, urgency). Lives in MongoDB and drives the recommender.

## MongoDB collections
`users`, `sessions`, `messages`, `clinical_states`, `reports`, `report_findings`, `recommendations`

## Obsidian vault
The vault root is the **project root** (`.obsidian/` already exists there). The `docs/` folder holds CONTEXT, PROGRESS, and DECISIONS notes.

## Current state
See [[PROGRESS]] for what's built and what's next.
