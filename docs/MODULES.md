> Auto-generated on 2026-04-21 17:10 by `scripts/update_docs.py`. Do not edit manually.

# Module Reference

This document provides an overview and reference guide for various components of the healthcare platform system. It includes service modules, core logic, and processing capabilities. The architecture is designed to handle patient interactions, report parsing, and recommendation generation.

## Architecture Overview

The architecture consists of:
- **Chatbot modules**: Handle patient interactions, collect clinical data, and generate follow-ups.
- **Recommender modules**: Provide health recommendations based on collected data.
- **Report interpreter modules**: Analyze and summarize medical reports.
- **Services**: Provide core functionalities such as chat management and file handling.
- **Prompts**: Text templates used by the OpenAI API for processing requests.
  
The data flow typically starts with a patient interaction in the chatbot, utilizes the recommender system to generate advice, and potentially evaluates uploaded medical reports.

## Chatbot Module: `engine.py`

### Purpose
Defines the structure for patient data and chatbot interaction within a chat turn.

### Key Classes
- **CollectedPatientData**: Contains fields such as age, gender, severity, duration, and symptoms.
- **ChatTurn**: Represents a single interaction, including the message, urgency level, suggested next step, and patient data.

### Dependencies
Imports `Literal` from `typing` and `BaseModel` from `pydantic`.

### Example Usage
```python
turn = ChatTurn(
    message="I have a headache.",
    urgency_level="none",
    suggested_next_step="none"
)
```

## Chatbot Module: `followup.py`

### Purpose
Generates follow-up questions based on missing clinical data using an OpenAI client.

### Key Function
- **`generate_followup(clinical_state: dict) -> str`**: Asynchronously creates follow-up queries based on clinical data provided.

### Dependencies
Imports `chat_completion` from `app.services.openai_client` and `FOLLOWUP_SYSTEM_PROMPT` from `app.prompts.chatbot_prompts`.

### Example Usage
```python
followup_response = await generate_followup({"missing_info": ["age", "severity"]})
```

## Chatbot Module: `handler.py`

### Purpose
Formulates a response to user input with recommendation and clinical state data.

### Key Function
- **`build_response(clinical_state: dict, recommendation: dict) -> str`**: Asynchronously constructs a response message.

### Dependencies
Imports `chat_completion` from `app.services.openai_client` and `RESPONSE_SYSTEM_PROMPT` from `app.prompts.chatbot_prompts`.

### Example Usage
```python
response = await build_response({"symptoms": "headache"}, {"next_step": "teleconsult"})
```

## Recommender Module: `engine.py`

### Purpose
Houses the data model for health recommendations.

### Key Classes
- **SpecialistPathwayItem**: Details about necessary specialists and reasons.
- **RecommendationResult**: Encapsulates recommendation results including the next step and urgency level.

### Dependencies
Imports `Literal` and `BaseModel` from `pydantic`.

### Example Usage
```python
recommendation = RecommendationResult(
    recommended_specialist="Neurologist",
    primary_recommendation_summary="Consult a neurologist."
)
```

## Recommender Module: `red_flags.py`

### Purpose
Detects critical symptoms indicative of emergencies within clinical data.

### Key Function
- **`detect_red_flags(clinical_state: dict) -> bool`**: Checks for the presence of emergency symptoms.

### Example Usage
```python
has_red_flags = await detect_red_flags({"symptoms": "chest pain"})
```

## Report Interpreter Module: `engine.py`

### Purpose
Defines structures for lab values and report findings for medical interpretation.

### Key Classes
- **LabValue**: Describes a laboratory test result.
- **ReportFindings**: Provides a detailed summary of a medical report analysis.

### Dependencies
Imports `Literal` and `BaseModel` from `pydantic`.

### Example Usage
```python
report = ReportFindings(
    report_type="Complete Blood Count",
    overall_summary="All values within normal range."
)
```

## Report Interpreter Module: `explainer.py`

### Purpose
Explains findings from a report using an OpenAI completion call.

### Key Function
- **`explain_findings(findings: dict) -> str`**: Provides a plain-language explanation of report findings.

### Dependencies
Imports `chat_completion` from `app.services.openai_client` and `REPORT_EXPLANATION_PROMPT`.

### Example Usage
```python
explanation = await explain_findings({"overall_summary": "Normal results."})
```

## Report Interpreter Module: `parser.py`

### Purpose
Parses text and images from medical reports, primarily PDFs.

### Key Functions
- **`extract_text(file_path: str, content_type: str) -> str`**: Extracts text based on file type.
- **`extract_images_from_pdf(file_path: str) -> list[str]`**: Converts PDF pages to images.

### Dependencies
Conditional imports of `fitz`, `pdfplumber`.

### Example Usage
```python
text = extract_text("/path/to/report.pdf", "application/pdf")
```

## Chat Service: `chat_service.py`

### Purpose
Handles sessions and user interactions within the chatting system.

### Key Functions
- **`start_chat(report_id: str | None = None) -> str`**: Initializes a chat session.
- **`send_message(chat_id: str, user_text: str) -> tuple`**: Processes a message and updates the session.

### Dependencies
Imports from `uuid`, `datetime`, `json` and several `app` modules.

### Example Usage
```python
chat_id = start_chat()
response = await send_message(chat_id, "I have a fever.")
```

## File Service: `file_service.py`

### Purpose
Manages file uploads and deletions for the system.

### Key Functions
- **`save_upload(filename: str, contents: bytes) -> str`**: Saves a file to the server.
- **`delete_upload(filename: str)`**: Deletes a specified file.

### Dependencies
Imports from `os` and `app.config`.

### Example Usage
```python
file_path = save_upload("test_report.pdf", b"PDF binary content")
```

## LLM Service: `llm.py`

### Purpose
Interacts with an AI model to generate structured health recommendations.

### Key Functions
- **`build_patient_info(...) -> str`**: Formats a patient profile string.
- **`get_recommendation(patient_info: str) -> tuple`**: Obtains a health recommendation.

### Dependencies
Imports from `app.services.openai_client` and `app.modules.recommender.engine`.

### Example Usage
```python
patient_info = build_patient_info(30, "female", "moderate", 5, "cough")
recommendation = await get_recommendation(patient_info)
```

## Report Service: `report_service.py`

### Purpose
Processes and interprets medical reports, saving the analysis.

### Key Functions
- **`save_upload(...) -> tuple[str, str]`**: Saves uploaded file data.
- **`interpret_report(...) -> tuple`**: Analyzes the contents of a medical report.

### Dependencies
Imports from `os`, `fastapi`, and several `app.modules`.

### Example Usage
```python
(file_path, _) = await save_upload(upload_file)
findings, _, _, _ = await interpret_report(file_path, "application/pdf", "report.pdf")
```

## Storage Service: `storage.py`

### Purpose
Provides persistent storage capabilities for sessions and reports.

### Key Functions
- **`save_session(...) -> str`**: Stores a session record.
- **`load_session(session_id: str) -> dict | None`**: Retrieves a session record by ID.

### Dependencies
Imports from `json`, `uuid`, and `pathlib`.

### Example Usage
```python
session_id = save_session(patient_info, recommendation, "model_v1", usage_data)
session = load_session(session_id)
```

## Data Flow

The data flow begins with a user interacting via the chatbot service, which collects symptom information and triggers follow-up actions. The chatbot's collected data is used in the recommender engine to provide health-related advice. If a user uploads a medical report, it is parsed and interpreted by the report interpreter module. These processes interact with external AI models through the `openai_client`. All sessions and report data are persistently stored using the storage service.