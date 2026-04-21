---
tags: [log, sessions]
---

# Session Log

> Reverse-chronological. One entry per build session.
> Add a new entry at the top when starting a session. Mark it done at the end.

---

## 2026-04-21 — Report Interpreter + Chat (Medi)

**What was built:**
- Report Interpreter: pdfplumber for text PDFs, GPT-4o vision fallback for scanned/image PDFs via pymupdf
- Chat (Medi): multi-turn conversational assistant with smart follow-up question collection
- Chat triggers full recommender pipeline inline when all 5 patient fields collected (age, gender, severity, duration, symptoms)
- Mid-session report loading: `report <path>` in CLI attaches interpreted report to chat context
- CLI: `interpret` and `chat` subcommands with spinner, colour-coded urgency, emergency banner
- API: `/reports/upload`, `/chat/sessions` and sub-routes

**Key decisions made:**
- `ready_to_recommend` flag in `ChatTurn` — LLM signals the service layer to fire the recommender, keeps orchestration out of the prompt
- `chat_completion()` separate from `structured_completion()` — different call shapes for multi-turn vs single-turn
- Plain text enforced in chat system prompt — prevents raw markdown leaking into patient-facing output
- `ImageBasedPDFError` custom exception — clean fallback from pdfplumber to vision pipeline

**Files created:**
- `app/modules/chatbot/engine.py` — `ChatTurn`, `CollectedPatientData`
- `app/modules/report_interpreter/engine.py` — `ReportFindings`, `LabValue`
- `app/modules/report_interpreter/parser.py` — text + image extraction
- `app/services/chat_service.py` — `start_chat`, `send_message`, `attach_report`
- `app/services/report_service.py` — `save_upload`, `interpret_report`
- `tests/test_chat.py` (13 tests), `tests/test_report_interpreter.py` (14 tests), `tests/test_validation.py` (10 tests)

**Test count at end:** 42 passing, 0 failing

---

## 2026-04-XX — Foundation + Recommender

**What was built:**
- Project scaffolded: FastAPI, `.venv`, `requirements.txt`
- Storage decision: dropped MongoDB, using JSON files in `data/` (sessions, reports, chats)
- `openai_client.py` — `structured_completion()` using `beta.chat.completions.parse()`
- `recommender/engine.py` — `RecommendationResult`, `SpecialistPathwayItem` schemas
- `llm.py` — `get_recommendation()`, `build_patient_info()`, cost tracking
- `storage.py` — save/load/list for sessions
- `tracker.py` — in-memory usage totals per run
- `POST /api/v1/recommend`, `GET /api/v1/sessions`, `GET /api/v1/sessions/{id}`
- Input validation: age 1-120, gender, severity, duration, symptoms length
- CLI `recommend` subcommand with animated spinner + colour-coded urgency output
- Battle test: 21 scenarios across 7 categories (emergencies, high urgency, moderate, low, vague, mental health, safety) — all passing
- `scripts/update_docs.py` — auto-generates API_REFERENCE, MODULES, DATA_MODELS via GPT-4o on git pre-push

**Key decisions made:**
- `openai>=2.0.0` for `beta.chat.completions.parse()` structured output — avoids JSON parsing fragility
- pdfplumber over PyPDF2 — better extraction for table-heavy lab reports
- CLI as primary test harness before API testing
- Prompts isolated in `app/prompts/` — can version, A/B test, or swap without touching services

**Test count at end:** 15 passing (5 recommender + 10 validation)
