---
tags: [reference, problem-statement]
---

# Med360 Patient AI — Problem Statement and V1 Reference

## 1. Project Title
**Med360 Patient AI**

---

## 2. Background
Med360 is being envisioned as a patient-first digital intelligence layer for home-based primary care. The broader Med360 ecosystem may later include MCO workflows, doctor workflows, and admin operations, but the current focus is only on the **patient app intelligence layer**.

The purpose of this project is to design and build a safe, modular, API-first AI system that can help patients:
- describe symptoms conversationally,
- upload and understand medical reports,
- answer guided follow-up questions,
- receive a safe recommendation for the next step in care.

This project is **not** intended to behave like a fully autonomous doctor, a final diagnosis engine, or a medical prescription system. Instead, it is intended to operate as a **conversational clinical intake and report-understanding layer** that supports patient guidance and care navigation.

---

## 3. Core Problem Statement
Patients often struggle with three major problems before they reach proper care:

### 3.1 They do not know how to explain their condition clearly
Most patients describe symptoms in incomplete, unstructured, or emotionally driven ways. Important details such as duration, severity, comorbidities, medication use, and warning signs are often missing. This makes it difficult to guide them correctly.

### 3.2 They do not understand their own medical reports
Patients frequently receive blood test reports, diagnostic summaries, prescriptions, or discharge documents, but they do not know how to interpret them. Even when abnormal values are visible, the meaning is often unclear. This creates anxiety, confusion, and delayed action.

### 3.3 They do not know the right next step in care
Patients may not know whether they should:
- monitor symptoms at home,
- book a teleconsult,
- request a home visit,
- see a specialist,
- or seek urgent hospital care.

As a result, the patient journey becomes reactive, fragmented, and inefficient.

---

## 4. Product Vision for This Repo
This repository is intended to power the **AI intelligence layer** of the Med360 patient app.

The system should act as a **patient-facing conversational intake assistant** that combines:
1. structured symptom intake,
2. medical report interpretation,
3. conversational follow-up questioning,
4. care recommendation logic.

The goal is to make patient communication more structured, report understanding more accessible, and next-step recommendations more useful.

---

## 5. Primary Goal of V1
Build a modular AI service that can be wrapped in **FastAPI**, backed by **MongoDB**, and handed off to frontend and backend engineers for integration into the Med360 patient application.

The AI engineer’s responsibility is to deliver a clean service layer with:
- API endpoints,
- prompt/orchestration logic,
- structured data extraction,
- recommendation logic,
- report interpretation logic,
- database design,
- and reusable integration contracts.

---

## 6. V1 Scope
V1 will include three core capabilities.

### 6.1 Recommender
This module should not be treated as a simple specialist recommender alone. It should function as a **care recommendation engine**.

Its purpose is to:
- analyze patient symptoms and context,
- identify likely care pathways,
- detect urgency and red flags,
- suggest the likely specialty or type of care,
- determine what information is still missing,
- propose the best next follow-up question.

### 6.2 Report Interpreter
This module should help patients understand uploaded reports.

Its purpose is to:
- accept PDF or image-based reports,
- extract structured findings,
- identify abnormal values or notable markers,
- explain the findings in simple language,
- provide a summary that can be used by the chatbot and recommendation engine.

### 6.3 Conversational Chatbot
This is the patient-facing orchestration layer.

Its purpose is to:
- accept natural language symptom descriptions,
- maintain session context,
- ask follow-up questions,
- call the recommender and report interpreter when needed,
- generate patient-friendly responses,
- keep the interaction natural, helpful, and calm.

---

## 7. Hidden but Essential V1 Component
Although not exposed as a standalone feature, the system must include a **structured clinical state layer**.

This layer should convert free-form chat into structured data such as:
- chief complaint,
- symptoms,
- duration,
- severity,
- chronic conditions,
- medications,
- red flags,
- missing information,
- report findings,
- recommendation status,
- urgency level.

This structured state is critical because it makes the chatbot more reliable, makes debugging easier, improves recommendation quality, and creates a better foundation for future analytics and model improvement.

---

## 8. What the System Should Do
At a high level, the system should be able to:

1. Receive a patient message.
2. Extract relevant clinical context.
3. Decide whether to ask a follow-up question, interpret a report, or provide a recommendation.
4. Detect red flags and escalate when needed.
5. Persist session and message data in MongoDB.
6. Return a clean structured and natural-language response via FastAPI.

---

## 9. What the System Should Not Do in V1
To keep the product safe, realistic, and buildable, the following are intentionally excluded from V1:

- tongue image analysis,
- selfie-based age estimation,
- mood detection from face,
- hydration estimation from selfie,
- medication prescription,
- dosage recommendation,
- autonomous diagnosis,
- high-claim medical decisioning,
- overly broad multimodal disease prediction.

These may be explored later, but they should not distract from a strong and credible first release.

---

## 10. Why This Scope Is Strong
This V1 scope is strong because it is:

- directly useful to patients,
- aligned with real patient pain points,
- safer than image-heavy diagnosis features,
- technically feasible within a focused build cycle,
- easy to wrap as services,
- easier to test and improve over time.

Instead of building a flashy but unreliable health app, this project focuses on building a **practical, structured, patient-facing AI service**.

---

## 11. User Problems Being Solved
The Med360 Patient AI system aims to solve the following user problems:

### 11.1 Symptom expression problem
Patients do not know what details matter when explaining symptoms.

### 11.2 Report interpretation problem
Patients struggle to understand laboratory values, abnormal findings, and what those findings may indicate in plain language.

### 11.3 Care navigation problem
Patients are often unsure about the next best action and whether the issue is urgent.

### 11.4 Communication quality problem
Without guided follow-up questions, conversations remain vague and unhelpful.

### 11.5 Continuity problem
Patients may want their sessions, report summaries, and prior interactions preserved for future reference and future system improvement.

---

## 12. Intended Value to the Business
For Med360, this system can become the intelligence layer that improves:

- patient intake quality,
- report understanding,
- digital triage quality,
- consistency of recommendations,
- handoff readiness for future operational layers,
- structured data collection for future system refinement.

This can reduce confusion, improve patient guidance, and create a stronger digital front door to home-based primary care.

---

## 13. AI Engineer Ownership
The AI engineer’s focus in this project is not full product development. The AI engineer is responsible for building the **intelligence backend**.

### Ownership includes:
- system design for patient AI workflows,
- MongoDB data model,
- FastAPI service layer,
- OpenAI integration,
- conversational orchestration,
- recommender logic,
- report interpretation logic,
- structured clinical state extraction,
- prompt design,
- API contracts,
- testable service outputs.

### Ownership does not primarily include:
- frontend styling,
- app UI implementation,
- complete product deployment workflows,
- non-AI application infrastructure,
- general product polish unrelated to the AI layer.

The output of this repo is therefore a **production-oriented AI service layer** that frontend and backend engineers can consume.

---

## 14. Delivery Model
The repository should be built as a modular backend project that can be handed over for integration.

### The AI layer should deliver:
- stable endpoints,
- structured request/response contracts,
- clean database flows,
- tested business logic,
- documentation for integration.

### Frontend and backend engineers should be able to use it for:
- patient app integration,
- report upload flows,
- chat UI integration,
- deployment and infra,
- authentication and app-level orchestration.

---

## 15. Database Philosophy
MongoDB is being chosen because the system naturally handles flexible document-shaped data such as:
- conversations,
- evolving clinical state,
- report findings,
- AI outputs,
- recommendation records,
- future training candidates.

The database should support three long-term goals:
1. product continuity,
2. structured analytics,
3. future sanitized model-improvement pipelines.

The system should not simply store raw chat blindly. It should also preserve structured state and support future de-identification workflows.

---

## 16. V1 Collections at a High Level
The database design should eventually support collections such as:
- users,
- sessions,
- messages,
- clinical_states,
- reports,
- report_findings,
- recommendations,
- feedback,
- training_candidates.

These should be designed so that the system remains queryable, maintainable, and extensible.

---

## 17. Functional Expectations of V1
A typical V1 session should look like this:

### Flow A — Symptom-first
1. Patient sends a symptom message.
2. Chatbot extracts structured state.
3. Recommender decides whether a follow-up question is needed.
4. Chatbot asks the next question or produces a recommendation.
5. Session data is saved in MongoDB.

### Flow B — Report-first
1. Patient uploads a report.
2. Report interpreter processes the document.
3. Structured findings are stored.
4. Chatbot explains the report.
5. Recommender may use report findings to guide next-step recommendations.

### Flow C — Mixed session
1. Patient describes symptoms.
2. Patient uploads a report.
3. The chatbot combines both symptom context and report findings.
4. The system returns a more informed next-step recommendation.

---

## 18. Safety Positioning
This system must be framed carefully.

It should behave as:
- a patient guidance assistant,
- a report understanding assistant,
- a structured intake assistant,
- a next-step recommendation assistant.

It should not behave as:
- a final diagnostician,
- a prescription engine,
- a replacement for clinical care,
- a high-certainty health predictor.

All outputs should use careful language and allow room for uncertainty, escalation, and follow-up questioning.

---

## 19. Success Criteria for V1
V1 should be considered successful if it can reliably do the following:

- hold a useful patient conversation,
- ask relevant follow-up questions,
- interpret common reports in patient-friendly language,
- maintain structured session state,
- generate reasonable care recommendations,
- expose usable FastAPI endpoints,
- persist conversations and outputs in MongoDB,
- provide a clean handoff layer to frontend/backend engineers.

---

## 20. Strategic Long-Term Benefit
Even though V1 is intentionally narrow, it creates the foundation for future extensions such as:
- image analysis,
- voice-based intake,
- multilingual flows,
- doctor handoff layers,
- MCO integration,
- better training datasets from de-identified interactions,
- longitudinal patient memory.

By keeping V1 focused, the system can mature on a reliable foundation instead of becoming a loose collection of disconnected features.

---

## 21. Final Statement
**Med360 Patient AI** is a focused AI service project intended to power the patient-facing intelligence layer of a home-based care platform.

Its V1 goal is to combine:
- conversational symptom intake,
- report understanding,
- and recommendation logic

into a modular, MongoDB-backed, FastAPI-delivered backend service.

This repository is meant to serve as the foundational AI layer that improves patient communication, report understanding, and next-step care guidance, while remaining structured, extensible, and safe for future growth.

