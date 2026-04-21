> Auto-generated on 2026-04-21 14:50 by `scripts/update_docs.py`. Do not edit manually.

# Module Reference

## Architecture Overview
The architecture is composed of various modules and services designed for clinical patient interaction, document processing, and response generation. The system leverages OpenAI models for generating clinical pathways and interpreting medical reports. It integrates several modules like `chatbot`, `recommender`, `report_interpreter`, core logic (`orchestrator`, `session_manager`, `state_extractor`), and client utility services (`openai_client`, `file_service`, `storage`) to achieve its functionalities.

## Modules and Services

### Chatbot Follow-Up Module (`app/modules/chatbot/followup.py`)
- **Purpose:** 
  To generate follow-up questions based on missing clinical information from the patient.
- **Key Function:**
  - `async def generate_followup(clinical_state: dict) -> str`: Uses the structured `clinical_state` to generate follow-up questions.
- **Inputs:** A dictionary representing the clinical state of the patient.
- **Outputs:** A follow-up question as a string.
- **Dependencies:** Imports `chat_completion` from `openai_client` and prompt `FOLLOWUP_SYSTEM_PROMPT` from `chatbot_prompts`.
- **Example:**
  ```python
  followup_question = await generate_followup(clinical_state)
  ```

### Chatbot Handler Module (`app/modules/chatbot/handler.py`)
- **Purpose:** 
  To build a response from the chatbot using the patient's clinical state and recommendations.
- **Key Function:**
  - `async def build_response(clinical_state: dict, recommendation: dict) -> str`: Forms a response incorporating the patient's state and provided recommendations.
- **Inputs:** Clinical state and recommendation dictionaries.
- **Outputs:** A response string.
- **Dependencies:** Uses `chat_completion` from `openai_client` and `RESPONSE_SYSTEM_PROMPT` from `chatbot_prompts`.
- **Example:**
  ```python
  response = await build_response(clinical_state, recommendation)
  ```

### Recommender Engine Module (`app/modules/recommender/engine.py`)
- **Purpose:** 
  Manages the structure of recommendation results including pathways and red flags.
- **Key Classes:**
  - `SpecialistPathwayItem(BaseModel)`: Describes a specialist pathway item.
  - `RecommendationResult(BaseModel)`: Contains information about recommendations.
- **Inputs:** N/A (data model definitions).
- **Outputs:** Structured data for recommendations.
- **Dependencies:** N/A.
- **Example:**
  ```python
  recommendation = RecommendationResult(...)
  ```

### Red Flags Detection Module (`app/modules/recommender/red_flags.py`)
- **Purpose:** 
  Detects potential red flags in a patient's clinical information.
- **Key Function:**
  - `async def detect_red_flags(clinical_state: dict) -> bool`: Checks if any red flags are present in the clinical state.
- **Inputs:** A dictionary representing the clinical state.
- **Outputs:** Boolean indicating presence of red flags.
- **Dependencies:** N/A
- **Example:**
  ```python
  has_red_flags = await detect_red_flags(clinical_state)
  ```

### Report Explainer Module (`app/modules/report_interpreter/explainer.py`)
- **Purpose:** 
  To provide an explanation of medical findings in layman's terms.
- **Key Function:**
  - `async def explain_findings(findings: dict) -> str`: Explains medical report findings.
- **Inputs:** Dictionary of findings.
- **Outputs:** Explanation string.
- **Dependencies:** Uses `chat_completion` and `REPORT_EXPLANATION_PROMPT`.
- **Example:**
  ```python
  explanation = await explain_findings(findings)
  ```

### Report Parser Module (`app/modules/report_interpreter/parser.py`)
- **Purpose:** 
  Parses uploaded medical reports to extract structured findings.
- **Key Functions:**
  - `async def parse_report(file: UploadFile, session_id: str) -> dict`: Parses the report and extracts findings.
  - `def _extract_text(file_path: str, content_type: str) -> str`: Extracts text from a file based on the type.
- **Inputs:** File to be parsed and session ID.
- **Outputs:** Extracted findings as a dictionary.
- **Dependencies:** `structured_completion`, `REPORT_EXTRACTION_PROMPT`, and `get_collection`.
- **Example:**
  ```python
  findings = await parse_report(file, session_id)
  ```

### File Service Module (`app/services/file_service.py`)
- **Purpose:** 
  Handles file operations such as saving and deleting uploaded files.
- **Key Functions:**
  - `def save_upload(filename: str, contents: bytes) -> str`: Saves a file.
  - `def delete_upload(filename: str)`: Deletes a file.
- **Inputs:** Filename and file content bytes.
- **Outputs:** File path.
- **Dependencies:** N/A.
- **Example:**
  ```python
  path = save_upload("report.pdf", file_contents)
  ```

### LLM Service Module (`app/services/llm.py`)
- **Purpose:** 
  Provides functions to create patient information and manage recommendations using language models.
- **Key Functions:**
  - `def build_patient_info(...) -> str`: Builds a formatted string of patient information.
  - `async def get_recommendation(...) -> tuple`: Fetches recommendations based on patient information.
- **Inputs:** Patient information details.
- **Outputs:** Recommendation result, model used, usage statistics, and session ID.
- **Dependencies:** Uses `structured_completion` and `save_session`.
- **Example:**
  ```python
  recommendation = await get_recommendation(patient_info)
  ```

### OpenAI Client Module (`app/services/openai_client.py`)
- **Purpose:** 
  Facilitates communication with OpenAI's API for structured completions.
- **Key Function:**
  - `async def structured_completion(...) -> tuple`: Communicates with OpenAI's API to get structured completion responses.
- **Inputs:** System prompts, user messages, response model type.
- **Outputs:** Parsed result, model used, and usage statistics.
- **Dependencies:** Uses OpenAI's `AsyncOpenAI`.
- **Example:**
  ```python
  result, model, usage = await structured_completion(prompt, user_message, ResponseModel)
  ```

### Storage Service Module (`app/services/storage.py`)
- **Purpose:** 
  Manages the storage of session data.
- **Key Functions:**
  - `def save_session(...) -> str`: Saves session data into a JSON file.
  - `def load_session(session_id: str) -> dict | None`: Loads session data from storage.
- **Inputs:** Session data, session ID.
- **Outputs:** Session ID or session data.
- **Dependencies:** Uses `Path`, `json`, and `uuid`.
- **Example:**
  ```python
  session_id = save_session(patient_info, recommendation, model_used, usage)
  ```

### Orchestrator Core Module (`app/core/orchestrator.py`)
- **Purpose:** 
  Orchestrates the chatbot interactions and manages session-based dialogues and recommendations.
- **Key Function:**
  - `async def handle_chat(request: ChatRequest) -> ChatResponse`: Handles chat logic, integrates modules for responses.
- **Inputs:** Chat request object.
- **Outputs:** Chat response object.
- **Dependencies:** Uses multiple modules including `chatbot`, `recommender`, and session manager.
- **Example:**
  ```python
  response = await handle_chat(chat_request)
  ```

### Session Manager Core Module (`app/core/session_manager.py`)
- **Purpose:** 
  Manages user sessions and message history.
- **Key Functions:**
  - `async def load_or_create_session(...) -> dict`: Loads or initiates a new session for a user.
  - `async def save_message(session_id, role: str, content: str)`: Saves user or assistant messages.
- **Inputs:** Session ID, user ID, message details.
- **Outputs:** Session data or confirmation.
- **Dependencies:** Directly interacts with the database.
- **Example:**
  ```python
  session_data = await load_or_create_session(session_id, user_id)
  ```

### State Extractor Core Module (`app/core/state_extractor.py`)
- **Purpose:** 
  Extracts the clinical state from patient messages.
- **Key Function:**
  - `async def extract_clinical_state(message: str, session: dict) -> dict`: Extracts structured state from messages.
- **Inputs:** Patient message and session data.
- **Outputs:** Extracted clinical state as a dictionary.
- **Dependencies:** Uses `structured_completion`.
- **Example:**
  ```python
  clinical_state = await extract_clinical_state(patient_message, session)
  ```

## Data Flow
1. **Patient Interaction**: A user sends a message, which is processed by `handle_chat` in the `orchestrator` core module.
2. **Session Management**: Load or create a session using `session_manager`.
3. **State Extraction**: Extract clinical state via the `state_extractor`.
4. **Red Flag Detection**: Check for any red flags with `recommender/red_flags`.
5. **Follow-Up or Recommendation**:
   - If there are red flags, respond urgently.
   - If information is missing, generate a follow-up using `chatbot/followup`.
   - Otherwise, get recommendation via `llm`.
6. **Response Building**: Construct a response through the `chatbot/handler`.
7. **Session Update**: Store responses in the session using `session_manager`.
8. **Output**: Return the response to the user as defined in `ChatResponse`.

This modular approach ensures scalability, maintainability, and clear separation of concerns across the various responsibilities of each component.