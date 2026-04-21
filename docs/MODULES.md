> Auto-generated on 2026-04-21 14:20 by `scripts/update_docs.py`. Do not edit manually.

# Module Reference

This document provides an architectural overview of the Med360 application, detailing how its different modules and services interact to fulfill patient requests. Each module description includes its purpose, key functions, classes, inputs, outputs, dependencies, and usage examples. A section on data flow explains how patient requests are processed through the system.

## Architecture Overview

The Med360 application consists of several modules and services that interact to process patient requests:
- **Chatbot**: Engages with patients, gathers information, and provides responses or follow-up questions.
- **Recommender**: Analyzes clinical state data to generate medical recommendations.
- **Report Interpreter**: Parses and explains diagnostic reports.
- **Core**: Orchestrates the session management and data flow.
- **Services**: Provides utilities for file operations and interactions with the OpenAI API.
- **Prompts**: Contains system prompts and configurations used by modules.
- **Tracker**: Monitors and records usage analytics.

Data flow typically starts with a patient message entry, followed by information extraction, red flag detection, and then either follow-up or recommendation delivery. Each module contributes a specific function to this chain, ensuring a comprehensive and guided interaction for the patient.

## Modules and Services

### 1. Chatbot - Follow-up

- **Purpose**: Generate follow-up questions based on missing clinical information.
- **Key Functions**:
  - `generate_followup(clinical_state: dict) -> str`: Asynchronously generates a follow-up question.
- **Inputs**: Clinical state dictionary with missing information.
- **Outputs**: String containing the follow-up question.
- **Dependencies**: Imports `chat_completion` from `app.services.openai_client` and `FOLLOWUP_SYSTEM_PROMPT` from `app.prompts.chatbot_prompts`.
- **Usage Example**:
  ```python
  missing_info = {"missing_info": ["duration", "severity"]}
  followup_question = await generate_followup(missing_info)
  ```

### 2. Chatbot - Handler

- **Purpose**: Construct responses to patient queries based on clinical state and recommendations.
- **Key Functions**:
  - `build_response(clinical_state: dict, recommendation: dict) -> str`: Asynchronously builds a patient response.
- **Inputs**: Clinical state and recommendation dictionaries.
- **Outputs**: Response string.
- **Dependencies**: Uses `chat_completion` from `app.services.openai_client` and `RESPONSE_SYSTEM_PROMPT` from `app.prompts.chatbot_prompts`.
- **Usage Example**:
  ```python
  response = await build_response(clinical_state, recommendation)
  ```

### 3. Recommender - Engine

- **Purpose**: Define data models for medical recommendations.
- **Key Classes**:
  - `SpecialistPathwayItem`: Contains specialist type and reason for recommendation.
  - `RecommendationResult`: Models the structure of a recommendation outcome.
- **Inputs**: None (model definitions).
- **Outputs**: Defined data structures.
- **Dependencies**: None.
- **Usage Example**:
  ```python
  recommendation = RecommendationResult(
      recommended_specialist="cardiologist",
      primary_recommendation_summary="Consult a cardiologist.",
      symptom_explanation="Symptoms suggest heart-related issues.",
      specialist_pathway=[SpecialistPathwayItem(specialist="cardiologist", reason="heart symptoms")],
      red_flags=["chest pain"],
      urgency_level="high",
      next_step="teleconsult",
      disclaimer="This is not a diagnosis."
  )
  ```

### 4. Recommender - Red Flags

- **Purpose**: Detect red-flag symptoms from the clinical state.
- **Key Functions**:
  - `detect_red_flags(clinical_state: dict) -> bool`: Checks for urgent or severe symptoms.
- **Inputs**: Clinical state dictionary.
- **Outputs**: Boolean indicating presence of red flags.
- **Dependencies**: None.
- **Usage Example**:
  ```python
  has_red_flags = await detect_red_flags(clinical_state)
  ```

### 5. Report Interpreter - Explainer

- **Purpose**: Explain medical report findings to patients in simple terms.
- **Key Functions**:
  - `explain_findings(findings: dict) -> str`: Asynchronously explains diagnostic findings.
- **Inputs**: Dictionary of findings.
- **Outputs**: Explanation string.
- **Dependencies**: Uses `chat_completion` from `app.services.openai_client` and `REPORT_EXPLANATION_PROMPT`.
- **Usage Example**:
  ```python
  explanation = await explain_findings(report_findings)
  ```

### 6. Report Interpreter - Parser

- **Purpose**: Parse and store diagnostic reports.
- **Key Functions**:
  - `parse_report(file: UploadFile, session_id: str) -> dict`: Processes and extracts content from uploaded files.
- **Inputs**: File to parse and session ID.
- **Outputs**: Parsed findings dictionary.
- **Dependencies**: Imports several services for file reading and database storage.
- **Usage Example**:
  ```python
  parsed_data = await parse_report(uploaded_file, user_session_id)
  ```

### 7. Services - File Service

- **Purpose**: Handle file storage and removal operations.
- **Key Functions**:
  - `save_upload(filename: str, contents: bytes) -> str`: Saves file data.
  - `delete_upload(filename: str)`: Deletes a specified file.
- **Inputs**: File names and data.
- **Outputs**: File path or deletion side-effects.
- **Dependencies**: None.
- **Usage Example**:
  ```python
  path = save_upload("report.pdf", file_contents)
  delete_upload("report.pdf")
  ```

### 8. Services - LLM

- **Purpose**: Initiate and process recommendations using language model interactions.
- **Key Functions**:
  - `build_patient_info(...) -> str`: Creates a textual patient info summary.
  - `get_recommendation(...) -> tuple`: Calls LLM for recommendations.
- **Inputs**: Patient data in structured form.
- **Outputs**: Recommendation and usage metrics.
- **Dependencies**: Relies on `app.services.openai_client` and the `RecommendationResult` model.
- **Usage Example**:
  ```python
  patient_info_str = build_patient_info(30, "female", "moderate", 7, "fever, fatigue")
  result, used_model, usage = await get_recommendation(patient_info_str)
  ```

### 9. Services - OpenAI Client

- **Purpose**: Interact with OpenAI's API for chat and structured completions.
- **Key Functions**:
  - `structured_completion(...) -> tuple`: Handles LLM result parsing and usage accounting.
- **Inputs**: Prompts, messages, and response models.
- **Outputs**: Structured response and analytics data.
- **Dependencies**: Depends on `openai` and project-specific configs.
- **Usage Example**:
  ```python
  response, model, usage = await structured_completion(prompt, message, ResponseModel)
  ```

### 10. Core - Orchestrator

- **Purpose**: Coordinate the workflow from patient message to chatbot response.
- **Key Functions**:
  - `handle_chat(request: ChatRequest) -> ChatResponse`: Full chat processing pipeline.
- **Inputs**: `ChatRequest` structured object.
- **Outputs**: `ChatResponse` structured object.
- **Dependencies**: Multiple core functions and modules from chatbot, recommender, and state extractor.
- **Usage Example**:
  ```python
  response = await handle_chat(chat_request)
  ```

### 11. Core - Session Manager

- **Purpose**: Manage and persist session data.
- **Key Functions**:
  - `load_or_create_session(...)`: Initiates or retrieves a session.
  - `save_message(...)`: Logs conversation messages.
- **Inputs**: Session identifiers and message contents.
- **Outputs**: Session dictionary structures.
- **Dependencies**: Uses database interaction helpers.
- **Usage Example**:
  ```python
  session = await load_or_create_session(None, "user_id_123")
  ```

### 12. Core - State Extractor

- **Purpose**: Develop clinical state understanding from conversation data.
- **Key Functions**:
  - `extract_clinical_state(...)`: Asynchronously converts messages into a structured clinical state.
- **Inputs**: User message and session context.
- **Outputs**: Clinical state as a dictionary.
- **Dependencies**: Operates with the OpenAI client and database collations.
- **Usage Example**:
  ```python
  clinical_state = await extract_clinical_state("I feel dizzy and have a headache", session_data)
  ```

## Data Flow

1. **Patient Message Received**: A new message from the patient is received (`handle_chat`).
2. **Session Management**: Session is loaded or created to track conversation (`load_or_create_session`).
3. **State Extraction**: The message and session history are processed to extract clinical data (`extract_clinical_state`).
4. **Red Flag Detection**: Checks clinical state for urgent symptoms (`detect_red_flags`).
5. **Follow-up Generation**: If missing information is found, generates a follow-up question (`generate_followup`).
6. **Recommendation Generation**: For complete state data, recommendations are formulated (`get_recommendation`).
7. **Response Construction**: Based on the clinical state and recommendations, a patient response is generated (`build_response`).
8. **Saving Messages**: Each interaction is logged to the session history (`save_message`).
9. **Response Delivery**: A `ChatResponse` is crafted and sent back to the patient.

The detailed collaboration of components enables Med360 to offer real-time, structured guidance and recommendations effectively.