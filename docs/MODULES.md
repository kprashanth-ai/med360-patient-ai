> Auto-generated on 2026-04-21 14:18 by `scripts/update_docs.py`. Do not edit manually.

# Module Reference

## Overview

The provided system is a modular Python application focused on facilitating patient interaction, recommendations, and report interpretation for a home-based primary care platform. The system is structured into several distinct modules, each responsible for specific aspects of handling patient interactions, generating recommendations, processing and interpreting medical reports, and managing sessions. The system heavily relies on OpenAI's APIs for language processing tasks to create conversational interfaces and extract clinical data.

---

## Chatbot Follow-up Module

### Purpose
Generates follow-up questions for missing clinical information in a patient interaction context.

### Key Functions
- `async generate_followup(clinical_state: dict) -> str`: Produces a follow-up question based on missing clinical information.

### Inputs and Outputs
- **Inputs:** `clinical_state` (a dictionary containing patient information including any missing fields)
- **Outputs:** A string containing a follow-up question.

### Dependencies
- `chat_completion` from `app.services.openai_client`
- `FOLLOWUP_SYSTEM_PROMPT` from `app.prompts.chatbot_prompts`

### Usage Example
```python
followup_question = await generate_followup(clinical_state={"missing_info": ["duration"]})
```

---

## Chatbot Handler Module

### Purpose
Builds response messages based on clinical state and recommendations.

### Key Functions
- `async build_response(clinical_state: dict, recommendation: dict) -> str`: Constructs a chat response message integrating clinical state and recommendations.

### Inputs and Outputs
- **Inputs:** `clinical_state` and `recommendation` dictionaries.
- **Outputs:** A string that is the constructed response.

### Dependencies
- `chat_completion` from `app.services.openai_client`
- `RESPONSE_SYSTEM_PROMPT` from `app.prompts.chatbot_prompts`

### Usage Example
```python
response = await build_response(clinical_state, recommendation)
```

---

## Recommender Engine Module

### Purpose
Defines models and structures for generating patient care recommendations.

### Key Classes
- `SpecialistPathwayItem(BaseModel)`: Represents a specialist and reason for referral.
- `RecommendationResult(BaseModel)`: Houses recommendation details including red flags and next steps.

### Inputs and Outputs
- **Outputs:** Instances of recommendation models used to guide patient care decisions.

### Dependencies
- `Literal` from `typing`
- `BaseModel` from `pydantic`

### Usage Example
```python
recommendation = RecommendationResult()
```

---

## Red Flags Module

### Purpose
Detects critical symptoms in the clinical state that require urgent care.

### Key Functions
- `async detect_red_flags(clinical_state: dict) -> bool`: Determines if any red flag symptoms are present in the clinical state.

### Inputs and Outputs
- **Inputs:** `clinical_state` dictionary.
- **Outputs:** Boolean indicating presence of red flags.

### Dependencies
None beyond standard Python libraries.

### Usage Example
```python
is_urgent = await detect_red_flags(clinical_state)
```

---

## Report Interpreter Module

### Purpose
Interprets and explains findings from medical reports.

### Key Functions
- `async explain_findings(findings: dict) -> str`: Provides a simplified explanation of medical report findings.

### Inputs and Outputs
- **Inputs:** `findings` dictionary.
- **Outputs:** A string explaining the findings.

### Dependencies
- `chat_completion` from `app.services.openai_client`
- `REPORT_EXPLANATION_PROMPT` from `app.prompts.report_prompts`

### Usage Example
```python
explanation = await explain_findings(report_findings)
```

---

## Report Parser Module

### Purpose
Parses and processes medical reports to extract structured data.

### Key Functions
- `async parse_report(file: UploadFile, session_id: str) -> dict`: Parses uploaded medical reports and extracts findings.

### Inputs and Outputs
- **Inputs:** `file` (uploaded file object), `session_id`.
- **Outputs:** Extracted findings in a dictionary format.

### Dependencies
- Imports from `os`, `fastapi`, `datetime`
- `structured_completion` from `app.services.openai_client`
- `REPORT_EXTRACTION_PROMPT` from `app.prompts.report_prompts`
- MongoDB operations via methods like `get_collection`

### Usage Example
```python
findings = await parse_report(uploaded_file, session_id)
```

---

## File Service Module

### Purpose
Manages file storage for uploads used throughout the application.

### Key Functions
- `save_upload(filename: str, contents: bytes) -> str`: Saves files to disk.
- `delete_upload(filename: str)`: Deletes files from disk.

### Inputs and Outputs
- **Outputs:** File paths or actions performed on the file system.

### Dependencies
- `os`
- `settings` from `app.config`

### Usage Example
```python
file_path = save_upload("report.pdf", file_data)
```

---

## LLM Service Module

### Purpose
Facilitates interactions with a language model to generate patient recommendations.

### Key Functions
- `async get_recommendation(patient_info: str) -> tuple`: Retrieves a structured recommendation for patient care.

### Inputs and Outputs
- **Inputs:** `patient_info` formatted string.
- **Outputs:** Tuple containing `RecommendationResult`, model used, and usage statistics.

### Dependencies
- `structured_completion` from `app.services.openai_client`
- `record_usage` from `app.tracker`
- `RECOMMENDER_SYSTEM_PROMPT` from `app.prompts.recommender_prompts`

### Usage Example
```python
result, model, usage = await get_recommendation(patient_information)
```

---

## OpenAI Client Module

### Purpose
Provides interaction interfaces with OpenAI's APIs for structured completions.

### Key Functions
- `async structured_completion(...) -> tuple`: Interacts with OpenAI API to get structured completions.

### Dependencies
- `AsyncOpenAI` from `openai`
- Pydantic models for enforcing response structure.

### Usage Example
```python
result, model, usage = await structured_completion(prompt, message, RecommendationResult)
```

---

## Orchestrator Core Module

### Purpose
Coordinates the entire data flow of patient sessions, managing states and responses.

### Key Functions
- `async handle_chat(request: ChatRequest) -> ChatResponse`: Primary function to handle a chat session, update state, and return response.

### Inputs and Outputs
- **Inputs:** `ChatRequest` object.
- **Outputs:** `ChatResponse` object.

### Dependencies
- `load_or_create_session`, `save_message` from `app.core.session_manager`
- `extract_clinical_state` from `app.core.state_extractor`
- `build_response` and `generate_followup` from chatbot modules
- `get_recommendation` from recommender engine

### Usage Example
```python
response = await handle_chat(chat_request)
```

---

## Session Manager Core Module

### Purpose
Manages session creation, retrieval, and message saving for user interactions.

### Key Functions
- `async load_or_create_session(...) -> dict`: Loads or initializes a user session.
- `async save_message(session_id, role: str, content: str)`: Saves a message under a session.

### Dependencies
- `datetime`, `bson` ObjectId
- MongoDB operations via methods like `get_collection`

### Usage Example
```python
session = await load_or_create_session(None, user_id)
```

---

## State Extractor Core Module

### Purpose
Extracts and processes clinical state information from patient interaction messages.

### Key Functions
- `async extract_clinical_state(message: str, session: dict) -> dict`: Extracts structured clinical state information.

### Dependencies
- `structured_completion` from `app.services.openai_client`
- `STATE_EXTRACTION_PROMPT` from `app.prompts.state_extraction_prompts`

### Usage Example
```python
clinical_state = await extract_clinical_state(patient_message, session)
```

---

## Data Flow

### Patient Request Flow

1. **Session Management**: The incoming request is processed by `session_manager` to load or create a new session.

2. **Message Handling**: The `orchestrator` takes the request, extracts the clinical state using `state_extractor`.

3. **Red Flag Detection**: Checks for emergency symptoms using the `red_flags` module.

4. **Follow-Up & Recommendations**: If any info is missing, the `chatbot followup` module is engaged to ask for additional data. Otherwise, a recommendation is generated via `recommender`.

5. **Response Construction**: The final response is crafted using `chatbot handler` and sent back to the patient.

6. **Database Updates**: Throughout the interaction, all states, sessions, and messages are continuously updated in the MongoDB database.

This flow ensures that each patient interaction is handled carefully, with emphasis on safety, clarity, and guidance through the primary care process.