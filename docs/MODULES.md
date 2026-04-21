---
tags: [modules, reference, auto-generated]
updated: "2026-04-21 17:19"
---

> Auto-generated on 2026-04-21 17:19 by `scripts/update_docs.py`. Do not edit manually.

# Module Reference

## Architecture Overview

The system is structured into several interconnected modules and services. The **chatbot module** handles user interactions and patient data collection, while the **recommender module** makes healthcare recommendations. The **report interpreter handles** document parsing and interpretation. Data flows seamlessly between these components via services such as **chat_service** and **report_service**, while the **openai_client** interacts with the OpenAI API for processing. The **storage service** persists data.

## Modules

### Chatbot Engine

- **Purpose:** Manage chat interactions and data collection from patients.
- **Key Classes:** 
  - `CollectedPatientData`: Stores patient demographics and symptom data.
  - `ChatTurn`: Represents one interaction in a chat session.
- **Inputs and Outputs:** Manages input data from patient interactions and provides output ready for recommendations.
- **Dependencies:** None.
- **Usage:**
  ```python
  from app.modules.chatbot.engine import ChatTurn
  turn = ChatTurn(message="Hello", urgency_level="low")
  ```

### Chatbot Followup

- **Purpose:** Generate follow-up dialogues based on clinical state.
- **Key Functions:**
  - `generate_followup(clinical_state: dict) -> str`: Produces follow-up prompts based on missing information.
- **Inputs and Outputs:** Takes clinical state input and returns a follow-up string.
- **Dependencies:** Imports `chat_completion` from `openai_client`.
- **Usage:**
  ```python
  await generate_followup({"missing_info": ["age", "gender"]})
  ```

### Chatbot Handler

- **Purpose:** Construct chat responses based on patient interactions.
- **Key Functions:**
  - `build_response(clinical_state: dict, recommendation: dict) -> str`: Creates a response using a clinical state and recommended course of action.
- **Inputs and Outputs:** Accepts clinical state and recommendation, outputs a chat response string.
- **Dependencies:** Imports `chat_completion` from `openai_client`.
- **Usage:**
  ```python
  await build_response({"age": 35}, {"next_step": "teleconsult"})
  ```

### Recommender Engine

- **Purpose:** Model and process patient recommendations.
- **Key Classes:**
  - `SpecialistPathwayItem`: Represents a recommended specialist path.
  - `RecommendationResult`: Stores a comprehensive set of recommendations.
- **Inputs and Outputs:** Takes patient data and produces a structured recommendation.
- **Dependencies:** None.
- **Usage:**
  ```python
  from app.modules.recommender.engine import RecommendationResult
  result = RecommendationResult(recommended_specialist="Cardiologist")
  ```

### Recommender Red Flags

- **Purpose:** Detect critical symptom keywords in patient data.
- **Key Functions:**
  - `detect_red_flags(clinical_state: dict) -> bool`: Returns true if red flag symptoms are detected.
- **Inputs and Outputs:** Accepts clinical state and outputs a Boolean for red flag presence.
- **Dependencies:** None.
- **Usage:**
  ```python
  await detect_red_flags({"chief_complaint": "chest pain"})
  ```

### Report Interpreter Engine

- **Purpose:** Define data models for interpreting lab reports.
- **Key Classes:**
  - `LabValue`: Represents individual lab test specifics.
  - `ReportFindings`: Encapsulates the comprehensive report interpretation.
- **Inputs and Outputs:** Processes report data and delivers structured findings.
- **Dependencies:** None.
- **Usage:**
  ```python
  from app.modules.report_interpreter.engine import LabValue
  lab = LabValue(name="Glucose", value="5.6", status="normal")
  ```

### Report Interpreter Explainer

- **Purpose:** Explain medical report findings.
- **Key Functions:**
  - `explain_findings(findings: dict) -> str`: Provides explanations for parsed report findings.
- **Inputs and Outputs:** Accepts report findings and returns explanatory text.
- **Dependencies:** Imports `chat_completion` from `openai_client`.
- **Usage:**
  ```python
  await explain_findings({"report_type": "Lipid Panel"})
  ```

### Report Interpreter Parser

- **Purpose:** Extract data from text and PDF reports.
- **Key Functions:**
  - `extract_text(file_path: str, content_type: str) -> str`: Extracts text from a report file.
  - `extract_images_from_pdf(file_path: str) -> list[str]`: Converts PDF pages to images.
- **Inputs and Outputs:** Processes files and returns extracted text or images.
- **Dependencies:** Uses third-party libraries `pdfplumber` and `fitz`.
- **Usage:**
  ```python
  text = extract_text("report.pdf", "application/pdf")
  ```

## Services

### Chat Service

- **Purpose:** Manage chat sessions and exchange messages.
- **Key Functions:**
  - `start_chat(report_id: str | None) -> str`: Initiates a chat session.
  - `send_message(chat_id: str, user_text: str) -> tuple`: Sends a message within a session.
- **Inputs and Outputs:** Manages chat session data and facilitates message exchange.
- **Dependencies:** Interfaces with modules such as `chatbot` and `recommender`.
- **Usage:**
  ```python
  chat_id = start_chat()
  turn, model, usage, recommendation = await send_message(chat_id, "I have a fever.")
  ```

### File Service

- **Purpose:** Handle file storage operations.
- **Key Functions:**
  - `save_upload(filename: str, contents: bytes) -> str`: Saves uploaded files.
- **Inputs and Outputs:** Manages file storage paths.
- **Dependencies:** Uses `os` for file operations.
- **Usage:**
  ```python
  file_path = save_upload("file.pdf", file_content)
  ```

### LLM Service

- **Purpose:** Facilitate structured completion interactions with the LLM.
- **Key Functions:**
  - `get_recommendation(patient_info: str) -> tuple`: Requests a structured recommendation from LLM.
- **Inputs and Outputs:** Handles requests to and responses from OpenAI LLM.
- **Dependencies:** Relies on `openai_client` for API interactions.
- **Usage:**
  ```python
  recommendation, model, usage, session_id = await get_recommendation(patient_info)
  ```

### OpenAI Client

- **Purpose:** Manage interactions with OpenAI API.
- **Key Functions:**
  - `structured_completion(system_prompt: str, user_message: str, response_model: Type[T]) -> tuple`: Handles LLM requests.
- **Inputs and Outputs:** Performs structured completions and maneuvers usage metrics.
- **Dependencies:** Uses `openai` for LLM interactions.
- **Usage:**
  ```python
  response, model_used, usage = await structured_completion(prompt, message, Model)
  ```

### Report Service

- **Purpose:** Process and interpret uploaded reports.
- **Key Functions:**
  - `interpret_report(file_path: str, content_type: str) -> tuple`: Converts report content to structured findings.
- **Inputs and Outputs:** Manages report file processing and interpretation.
- **Dependencies:** Depends on `parser` from `report_interpreter` for data extraction.
- **Usage:**
  ```python
  findings, model_used, usage, report_id = await interpret_report(file_path, content_type)
  ```

### Storage Service

- **Purpose:** Persist application data related to sessions, reports, and chats.
- **Key Functions:**
  - `save_session(patient_info: dict, recommendation: dict) -> str`: Saves session data.
- **Inputs and Outputs:** Handles file-based data storage.
- **Dependencies:** Uses `json` for data serialization.
- **Usage:**
  ```python
  session_id = save_session(patient_info, recommendation)
  ```

### Tracker

- **Purpose:** Track usage metrics for the system.
- **Key Functions:**
  - `record_usage(usage_entry: dict)`: Records API usage details.
- **Inputs and Outputs:** Manages usage statistics.
- **Dependencies:** None.
- **Usage:**
  ```python
  record_usage({"total_tokens": 100})
  ```

## Data Flow

1. **Patient Request Initiation:** A patient starts a chat session via the `chat_service`. This session uniquely identifies each interaction.

2. **Information Gathering:** The chatbot engages the patient, collects essential details (using `Chatbot Engine`), and stores messages.

3. **Red Flags Detection:** The `Recommender Red Flags` module checks symptom descriptions for urgent conditions before recommending further steps.

4. **Analysis and Recommendations:** Patient details are used by the `Recommender Engine` to produce a recommendation based on symptoms and medical history.

5. **Report Handling:** If a medical report is provided, the `report_service` extracts and interprets the findings using the `report_interpreter`.

6. **Response Composition:** Using all collected data, a structured response is composed and sent back to the patient.

7. **Data Storage and Metrics:** All interactions and sessions are logged to the `Storage Service`, while usage metrics are captured by the `Tracker`.