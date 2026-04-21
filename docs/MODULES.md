> Auto-generated on 2026-04-21 14:40 by `scripts/update_docs.py`. Do not edit manually.

# Module Reference

## Architecture Overview

The system is designed as a modular healthcare AI platform to assist with patient guidance by using NLP and ML technologies powered by the OpenAI API. It consists of several interconnected modules, each serving a specific purpose in handling patient data, generating recommendations, parsing reports, and managing sessions.

- **Chatbot Modules**: Handles patient interaction, generates responses, and follows up on missing information.
- **Recommender Modules**: Provides healthcare recommendations, considering red flags to assess urgency.
- **Report Interpreter Modules**: Parses and explains medical reports using AI prompts.
- **Core Logic**: Orchestrates the overall flow of the patient interaction and manages sessions.
- **Services**: Provides utility services such as file management, API client interactions, storage functions, and session tracking.

## Modules and Services

### Chatbot Followup Module

- **Purpose**: Generates follow-up questions for patients based on their provided clinical state.
- **Key Functions**:
  - `generate_followup(clinical_state: dict) -> str`: Asynchronously generates a follow-up question based on missing patient information using the OpenAI chat API.
- **Inputs**: A dictionary `clinical_state` with patient information including a list of missing data points.
- **Outputs**: A string containing a follow-up question.
- **Dependencies**: Imports `chat_completion` from `app.services.openai_client` and `FOLLOWUP_SYSTEM_PROMPT` from `app.prompts.chatbot_prompts`.

### Chatbot Handler Module

- **Purpose**: Constructs appropriate responses for patient inquiries.
- **Key Functions**:
  - `build_response(clinical_state: dict, recommendation: dict) -> str`: Asynchronously builds a chatbot response considering the clinical state and recommendation.
- **Inputs**: Two dictionaries, `clinical_state` and `recommendation`.
- **Outputs**: A string formatted as a complete response.
- **Dependencies**: Uses `chat_completion` from `app.services.openai_client` and `RESPONSE_SYSTEM_PROMPT` from `app.prompts.chatbot_prompts`.

### Recommender Engine Module

- **Purpose**: Structures the healthcare recommendations based on patient symptoms.
- **Key Classes**:
  - `SpecialistPathwayItem(BaseModel)`, `RecommendationResult(BaseModel)`: Pydantic models defining the expected structure of the recommendation results.
- **Outputs**: A structured response aligning with the recommendation model.
- **Dependencies**: Utilizes Pydantic for data modeling.

### Recommender Red Flags Module

- **Purpose**: Identifies urgent health-related symptoms indicating a possible emergency.
- **Key Functions**:
  - `detect_red_flags(clinical_state: dict) -> bool`: Checks clinical states for emergency red flag keywords.
- **Inputs**: Dictionary `clinical_state` with patient symptoms.
- **Outputs**: Boolean indicating the presence of red flag symptoms.

### Report Interpreter Explainer Module

- **Purpose**: Transforms structured report findings into patient-friendly language explanations.
- **Key Functions**:
  - `explain_findings(findings: dict) -> str`: Explains report findings using simple language.
- **Inputs**: Dictionary of findings from the parsed medical report.
- **Outputs**: String explanation of the findings.

### Report Interpreter Parser Module

- **Purpose**: Parses uploaded medical reports to extract structured information.
- **Key Functions**:
  - `parse_report(file: UploadFile, session_id: str) -> dict`: Extracts text data from uploaded documents and converts it into a structured format.
  - `_extract_text`: Internal utility to deal with different file formats.
- **Inputs**: `UploadFile` object and a `session_id`.
- **Outputs**: Dictionary of parsed findings.
- **Dependencies**: Interfaces with `structured_completion` from `openai_client` and file I/O utilities.

### File Service Module

- **Purpose**: Manages file storage and deletion tasks.
- **Key Functions**:
  - `save_upload(filename: str, contents: bytes) -> str`: Saves uploaded files to the disk.
  - `delete_upload(filename: str)`: Deletes file from storage.
- **Inputs**: Filename and file contents for saving; filename for deletion.
- **Outputs**: File path of saved files.

### LLM Service Module

- **Purpose**: Constructs patient data into structured information for use with the language model.
- **Key Functions**:
  - `build_patient_info(age: int, gender: str, severity: str, duration: int, symptoms: str) -> str`: Creates a structured string.
  - `get_recommendation(patient_info: str) -> tuple`: Generates health recommendations and tracks API usage.
- **Inputs**: Patient information string.
- **Outputs**: Recommendation result and analytics.

### OpenAI Client Service Module

- **Purpose**: Interfaces with OpenAI's API for structured completions.
- **Key Functions**:
  - `structured_completion(system_prompt: str, user_message: str, response_model: Type[T]) -> tuple`: Sends and receives parsed results from the OpenAI API.
- **Inputs**: Prompts and message content.
- **Outputs**: Parsed results conforming to given model class.

### Storage Service Module

- **Purpose**: Manages session data through file storage operations.
- **Key Functions**:
  - `save_session`: Saves session data to storage.
  - `load_session`: Loads session data from storage.
  - `list_sessions`: Lists recent sessions.
- **Dependencies**: Relies on JSON and filesystem libraries for data management.

### Tracker Module

- **Purpose**: Tracks API usage and calculates related costs.
- **Key Functions**:
  - `record_usage(usage_entry: dict)`: Increments the session state with usage entries.
  - `get_session_totals() -> dict`: Retrieves aggregate usage statistics.

## Data Flow Overview

1. **Patient Request Entry**: The user sends a message via a chatbot interface, initiating a session.
2. **Session Management**: The `session_manager` ensures the session is loaded or created.
3. **Clinical State Extraction**: `state_extractor` pulls structured data from the message.
4. **Red Flag Detection**: Interpreted message is analyzed for emergency signals in the `red_flags` module.
5. **Follow-up and Recommendation**: If necessary, a follow-up is generated; otherwise, a recommendation process begins, leveraging the `recommender` module.
6. **Response Generation**: Compiles all data and creates a response using `chatbot.handler`.
7. **Result Delivery**: The system responds to the patient with advice, escalating if red flags are detected.

This document lays out module responsibilities and connections, supporting developers in understanding and extending the platform effectively.