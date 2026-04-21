# Build Progress

> Update after each session. Claude reads this to know where to pick up.

---

## Status key
- `[ ]` Not started
- `[~]` In progress
- `[x]` Done and tested

---

## Phase 1 — Foundation
- [x] Project structure scaffolded
- [x] `.venv` created, requirements installed
- [x] `.env` configured with real OpenAI key
- [x] Storage decision: JSON files in `data/`, MongoDB deferred
- [x] FastAPI app boots — `uvicorn app.main:app --reload`

## Phase 2 — Recommender
- [x] `openai_client.py` — `structured_completion()` using `beta.chat.completions.parse()`
- [x] `recommender/engine.py` — `RecommendationResult` + `SpecialistPathwayItem` Pydantic schemas
- [x] `llm.py` — `get_recommendation()`, `build_patient_info()`, cost tracking
- [x] `storage.py` — `save_session()`, `load_session()`, `list_sessions()`
- [x] `tracker.py` — in-memory usage totals
- [x] `POST /api/v1/recommend` + `GET /api/v1/sessions` + `GET /api/v1/sessions/{id}`
- [x] Input validation: age 1-120, gender Literal, severity Literal, duration 1-3650, symptoms 10-1000 chars
- [x] CLI `recommend` subcommand with animated spinner + colour-coded urgency output
- [x] 15 tests passing (schema, session saving, usage tracking, emergency escalation, low urgency, all validation)
- [x] Battle test: 21 scenarios across 7 categories — all passing

## Phase 3 — Report Interpreter
- [x] `report_interpreter/engine.py` — `ReportFindings` + `LabValue` schemas
- [x] `report_interpreter/parser.py` — `extract_text()`, `extract_images_from_pdf()`, `ImageBasedPDFError`
- [x] `report_prompts.py` — `REPORT_EXTRACTION_PROMPT`
- [x] `report_service.py` — `save_upload()`, `interpret_report()` with vision fallback for scanned PDFs
- [x] `storage.py` — `save_report()`, `load_report()`, `list_reports()`
- [x] `POST /api/v1/reports/upload` (PDF + TXT, 415 for other types)
- [x] `GET /api/v1/reports` + `GET /api/v1/reports/{id}`
- [x] CLI `interpret` subcommand — prompts for file path, colour-coded findings
- [x] Vision fallback: scanned PDFs rendered to images via pymupdf, sent to GPT-4o vision
- [x] 14 tests passing

## Phase 4 — Conversational Chat (Medi)
- [x] `chatbot/engine.py` — `ChatTurn` + `CollectedPatientData` schemas
- [x] `chatbot_prompts.py` — `CHAT_SYSTEM_PROMPT` with plain-text style + follow-up question instructions + recommendation trigger logic
- [x] `openai_client.py` — `chat_completion()` for multi-turn history
- [x] `storage.py` — `save_chat()`, `load_chat()`, `list_chats()`
- [x] `chat_service.py` — `start_chat()`, `send_message()`, `attach_report()`
- [x] `POST /api/v1/chat/sessions` — create chat
- [x] `POST /api/v1/chat/sessions/{id}/message` — send message, returns `ChatTurn` + optional `RecommendationResult`
- [x] `POST /api/v1/chat/sessions/{id}/report` — attach interpreted report to chat context
- [x] `GET /api/v1/chat/sessions/{id}` + `GET /api/v1/chat/sessions`
- [x] CLI `chat` subcommand — interactive REPL, `report <path>` mid-chat, emergency banner, urgency badges
- [x] Smart follow-up: Medi collects 5 fields (age, gender, severity, duration, symptoms) then fires full recommender, renders rich panel inline
- [x] Report Q&A: once a report is loaded, all report questions answered from findings context
- [x] 13 tests passing

## Total tests
- 42 passing, 0 failing

---

## What's next (candidate for next session)
- [ ] **Deployment** — run as a local server so frontend team can integrate
- [ ] **Auth header** — simple API key check for frontend integration
- [ ] **Chat history truncation** — cap message history at N tokens to avoid context overflow on long chats
- [ ] **Report in chat at start** — allow `POST /chat/sessions` to accept a report file directly, not just a report_id
- [ ] **Streaming responses** — stream Medi's reply token-by-token for better CLI/frontend feel
- [ ] **MongoDB migration** — swap `storage.py` when ready
