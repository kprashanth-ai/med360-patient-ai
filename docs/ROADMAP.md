---
tags: [roadmap, planning]
---

# Roadmap

> Future phases in rough priority order. See [[PROGRESS]] for what's already done.
> Move items to [[PROGRESS]] when a phase starts.

---

## Phase 5 — Deployment & Frontend Integration

**Goal:** Frontend team can hit the API from their app.

- [ ] Run locally as a persistent server (PM2 or simple Windows service)
- [ ] Add `X-API-Key` header check — simple env-var secret for V1
- [ ] CORS configured for frontend's dev origin
- [ ] README updated with integration guide and base URL
- [ ] Swagger UI (`/docs`) tested end-to-end by frontend team
- [ ] Sample frontend calls documented (JS fetch / axios snippets)

---

## Phase 6 — Streaming Responses

**Goal:** Medi's reply streams token-by-token for better UX.

- [ ] Switch chat turns to `stream=True` via OpenAI async streaming
- [ ] Server-sent events (SSE) on `POST /chat/sessions/{id}/message`
- [ ] CLI streams characters to terminal in real-time (no waiting for full response)
- [ ] Structured metadata (urgency, next_step, recommendation) sent as final JSON chunk after stream ends

---

## Phase 7 — Robustness

**Goal:** Production-grade reliability without major rewrites.

- [ ] Chat history token cap — drop oldest messages when approaching model context limit (keep system prompt + last N turns)
- [ ] Retry logic on OpenAI timeouts — exponential backoff, max 3 attempts
- [ ] Request timeout middleware — 30s max per API call, clean 504 response
- [ ] Structured logging (structlog or loguru) — replace all print() calls
- [ ] Standardised error responses (RFC 7807 Problem JSON format)

---

## Phase 8 — MongoDB Migration

**Goal:** Move off flat JSON files to a real database.

- [ ] Add motor back to requirements
- [ ] Swap `app/services/storage.py` reads/writes for motor async calls — nothing else changes
- [ ] Collections: `sessions`, `reports`, `chats`
- [ ] Index on `created_at` for list queries
- [ ] Data migration script: import existing JSON files into MongoDB

> Architecture note: because all storage is isolated in `storage.py`, the API, services, and schemas don't change at all. See [[DECISIONS]].

---

## Phase 9 — Enhanced Chat

**Goal:** Richer patient experience.

- [ ] Multi-report comparison — load two reports and ask Medi to compare trends
- [ ] Medication awareness — patient lists current medications, Medi flags context (non-prescriptive)
- [ ] Session memory — patient can say "last time you suggested X, how is that going?"
- [ ] Report at chat start — `POST /chat/sessions` accepts a file upload directly, not just a `report_id`
- [ ] Follow-up reminder — Medi suggests a follow-up date based on urgency

---

## Phase 10 — Patient Identity

**Goal:** Know who the patient is across sessions.

- [ ] Simple patient profile: name, DOB, known conditions (JSON file → MongoDB collection)
- [ ] Chat and reports linked to `patient_id`
- [ ] `GET /patients/{id}/reports` — full report history for a patient
- [ ] Chat can reference prior sessions: "your HbA1c from 3 months ago was…"
