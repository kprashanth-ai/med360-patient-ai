---
tags: [decisions, architecture]
---

# Architecture Decisions

> Short entries only. WHY we chose something, not what it is.
> See [[CONTEXT]] for how the project is structured. See [[ROADMAP]] for pending decisions.

---

## JSON files instead of MongoDB (for now)
Storage is flat JSON files under `data/` (sessions/, reports/, chats/). Motor and pymongo removed.
Migration path: replace `app/services/storage.py` reads/writes with motor calls — service layer and API stay the same.

## openai>=2.0.0 — `beta.chat.completions.parse()`
Upgraded from 1.x to 2.x to fix httpx proxies conflict. `beta.chat.completions.parse()` gives native Pydantic structured output with no JSON parsing fragility.

## Two OpenAI client functions — `structured_completion` vs `chat_completion`
Single-turn (recommender, report) uses `structured_completion(system, message, model)`.
Multi-turn (chat) uses `chat_completion(system, history, model)` — different signatures, cleaner than a combined function with optional overrides.

## `ready_to_recommend` flag in `ChatTurn`
The chat LLM signals when it has collected enough patient data by setting `ready_to_recommend=true` and populating `patient_data`. The service layer then calls `get_recommendation()` in the same turn and returns the result. This keeps orchestration logic in the service, not in the LLM.

## Vision fallback for scanned PDFs
`pdfplumber` raises `ImageBasedPDFError` when no text is found. `report_service.py` catches it, renders pages to images via `pymupdf`, and passes them as base64 to GPT-4o vision. One API call, same structured output pipeline.

## Plain text enforced in chat system prompt
GPT-4o defaults to markdown. Explicitly instructing "plain text only, no asterisks, no # headers" in `CHAT_SYSTEM_PROMPT` prevents raw markdown from rendering in the CLI and in patient-facing UIs.

## Prompts in their own module (`app/prompts/`)
Prompts change often and independently of orchestration logic. Isolated here they can be versioned, A/B tested, or swapped without touching services.

## No auth in V1
Auth is the frontend/backend team's responsibility. This repo delivers the AI service layer only.

## pdfplumber over PyPDF2
Better text extraction for table-heavy lab reports. PyPDF2 struggles with multi-column layouts.

## CLI as primary test harness
Interactive CLI (`cli.py`) lets us test the full pipeline end-to-end — prompt, spinner, colour output, session saving — without needing a frontend. Added before API testing.
