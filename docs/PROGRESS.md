# Build Progress

## How to use this file
- Update status after each working session
- Claude reads this to know where to pick up
- Keep entries short — just what changed and what's next

---

## Status key
- `[ ]` Not started
- `[~]` In progress
- `[x]` Done and tested

---

## Step 1 — Foundation
- [x] Project structure scaffolded
- [x] `.venv` created
- [x] `requirements.txt` installed (motor/pymongo removed — using JSON files for now)
- [x] Storage decision: JSON files in `data/`, migrate to MongoDB later
- [ ] `.env` file created with real keys
- [ ] FastAPI app boots (`uvicorn app.main:app --reload`)

## Step 2 — Recommender (current)
- [x] `openai_client.py` — `structured_completion()` using OpenAI native `parse()`
- [x] `recommender/engine.py` — `recommend(symptoms)` → `RecommendationResult`
- [x] `POST /api/v1/recommend` endpoint wired
- [x] 3 tests written (schema, emergency, low urgency)
- [x] `.env` set up with real key
- [x] Tests passing (3/3) — schema, emergency escalation, low urgency
- [ ] Manual test via `/docs`

## Step 2 — Session Management
- [ ] `session_manager.py` — create session
- [ ] `session_manager.py` — load session by ID
- [ ] `session_manager.py` — save message to session
- [ ] Test: create session, add messages, reload and verify

## Step 3 — Clinical State Extraction
- [ ] `state_extractor.py` — send patient message to OpenAI, get structured JSON back
- [ ] `state_extractor.py` — persist state to MongoDB
- [ ] Test: send "I have a headache for 2 days" → verify structured state returned

## Step 4 — Chatbot (follow-up questions)
- [ ] `followup.py` — given missing_info, generate one follow-up question
- [ ] `handler.py` — build patient-friendly response
- [ ] Test: incomplete state → follow-up question generated

## Step 5 — Red Flag Detection
- [ ] `red_flags.py` — keyword + state-based detection
- [ ] Test: "chest pain and difficulty breathing" → urgent=True

## Step 6 — Care Recommender
- [ ] `engine.py` — send clinical state to OpenAI, get structured recommendation
- [ ] Test: complete state → recommendation with urgency + next_step

## Step 7 — Report Interpreter
- [ ] `parser.py` — extract text from PDF
- [ ] `explainer.py` — explain findings in plain language
- [ ] Test: upload a sample blood report → structured findings + explanation

## Step 8 — Orchestrator + API wiring
- [ ] `orchestrator.py` — tie all modules together
- [ ] `/chat` endpoint end-to-end test
- [ ] `/reports/upload` endpoint end-to-end test
- [ ] `/recommendations/{session_id}` endpoint end-to-end test

---

## Decisions log
See [[DECISIONS]]
