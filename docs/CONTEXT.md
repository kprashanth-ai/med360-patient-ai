---
tags: [reference, orientation]
---

# Med360 Patient AI — Session Context

> Claude reads this file at the start of every session to get oriented fast.
> Also read [[PROGRESS]] before starting work.
> See [[DECISIONS]] for why key choices were made. See [[SESSION_LOG]] for history.

## What we're building
A **FastAPI + JSON-file AI backend** for the Med360 patient app — a patient-facing health guidance and report interpretation system. NOT a diagnosis engine.

## Tech stack
- **FastAPI 0.115** — API layer (3 routers: recommender, reports, chat)
- **JSON files** in `data/` — storage (sessions, reports, chats). MongoDB deferred.
- **OpenAI GPT-4o** via `openai>=2.0.0` — `beta.chat.completions.parse()` for structured outputs
- **pdfplumber** — text-based PDF parsing
- **pymupdf (fitz)** — render scanned PDFs to images for vision fallback
- **Python 3.10**, `.venv` at project root
- **pytest + pytest-asyncio** (mode=auto)

## Running the app
```bash
uvicorn app.main:app --reload       # API at http://localhost:8000
python cli.py recommend             # one-shot specialist recommendation
python cli.py interpret             # interpret a PDF/TXT medical report
python cli.py chat                  # conversational chat with Medi
```

## Project structure (key paths)
```
app/
  main.py                    — FastAPI entry, mounts 3 routers
  config.py                  — Settings (reads .env)
  api/v1/
    recommendations.py       — POST /recommend, GET /sessions
    reports.py               — POST /reports/upload, GET /reports
    chat.py                  — POST /chat/sessions, /message, /report, GET history
  modules/
    recommender/engine.py    — RecommendationResult, SpecialistPathwayItem schemas
    report_interpreter/
      engine.py              — ReportFindings, LabValue schemas
      parser.py              — extract_text(), extract_images_from_pdf(), ImageBasedPDFError
    chatbot/engine.py        — ChatTurn, CollectedPatientData schemas
  prompts/
    recommender_prompts.py   — RECOMMENDER_SYSTEM_PROMPT
    report_prompts.py        — REPORT_EXTRACTION_PROMPT
    chatbot_prompts.py       — CHAT_SYSTEM_PROMPT
  services/
    openai_client.py         — structured_completion(), chat_completion()
    llm.py                   — get_recommendation(), build_patient_info()
    report_service.py        — save_upload(), interpret_report() (vision fallback)
    chat_service.py          — start_chat(), send_message(), attach_report()
    storage.py               — save/load/list for sessions, reports, chats
  tracker.py                 — in-memory usage totals per process run
cli.py                       — CLI with recommend / interpret / chat subcommands
scripts/
  update_docs.py             — auto-generates API_REFERENCE, MODULES, DATA_MODELS via GPT-4o
  battle_test.py             — 21-scenario prompt battle test for recommender
tests/
  test_recommender.py        — 5 tests (schema, session, usage, emergency, low urgency)
  test_validation.py         — 10 input validation tests for /recommend
  test_report_interpreter.py — 14 tests (schema, parser, storage, API)
  test_chat.py               — 13 tests (schema, storage, API)
```

## Three core features (all working)
1. **Recommender** — one-shot: patient info → urgency + specialist pathway + red flags
2. **Report Interpreter** — PDF/TXT upload → structured findings + plain-language explanation. Falls back to GPT-4o vision for scanned PDFs.
3. **Chat (Medi)** — multi-turn conversation. Collects age/gender/severity/duration/symptoms through natural dialogue, then fires the full recommender pipeline and renders the same rich structured output inline.

## Key service contracts
- `structured_completion(system, message, model, images=None)` → `(result, model_used, usage)`
- `chat_completion(system, history, model)` → `(result, model_used, usage)`
- `get_recommendation(patient_info_str)` → `(RecommendationResult, model, usage, session_id)`
- `send_message(chat_id, text)` → `(ChatTurn, model, usage, RecommendationResult | None)`

## Storage layout
```
data/
  sessions/{uuid}.json   — recommender calls
  reports/{uuid}.json    — interpreted reports
  chats/{uuid}.json      — chat conversations (full message history + report_context)
```

## Obsidian vault
Vault root = project root (`.obsidian/` exists). `docs/` holds CONTEXT, PROGRESS, DECISIONS plus auto-generated API_REFERENCE, MODULES, DATA_MODELS.
