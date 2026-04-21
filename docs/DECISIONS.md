# Architecture Decisions

> Short entries only. WHY we chose something, not what it is.

---

## JSON files instead of MongoDB (for now)
Storage is flat JSON files under `data/`. Motor and pymongo removed from requirements.
Migration path: replace `app/services/storage.py` reads/writes with motor calls — models stay the same.

## pymongo / motor — removed for now
Was causing version conflicts. Not needed until MongoDB migration.

## response_format: json_object for structured completions
OpenAI's `json_object` mode guarantees valid JSON output. Used in state extraction and recommender to avoid parsing failures.

## clinical_state is a separate MongoDB collection (not embedded in session)
Embedding would make it hard to query or update independently. Keeping it separate allows the recommender to read it directly without loading the full session.

## prompts are in their own module (`app/prompts/`)
Prompts change often. Keeping them isolated means we can version, A/B test, or swap them without touching orchestration logic.

## No auth in V1
Auth is the frontend/backend team's responsibility. This repo delivers the AI service layer only.

## pdfplumber for PDF parsing (not PyPDF2)
pdfplumber gives better text extraction for table-heavy lab reports. PyPDF2 struggles with multi-column layouts.
