> Auto-generated on 2026-04-21 14:20 by `scripts/update_docs.py`. Do not edit manually.

# API Reference

Welcome to the API Reference for the Med360 Patient AI application. This API provides endpoints for chat interactions, session retrieval, generating health recommendations based on patient data, uploading and retrieving report analyses, and more. The base URL pattern for accessing these endpoints is structured as `/api/v1/{endpoint}`.

## Endpoints

### POST /chat

#### Description
Initiate a chat session or continue an existing session with a message. This endpoint should be used when interacting with the chat service to inquire or provide information during the session.

#### Request Body

| Field      | Type   | Required | Description                         |
|------------|--------|----------|-------------------------------------|
| user_id    | string | Yes      | The unique identifier for the user. |
| session_id | string | No       | The session identifier, if continuing an existing session. |
| message    | string | Yes      | The message content to be sent in this chat interaction. |

#### Response Body

| Field   | Type    | Description                            |
|---------|---------|----------------------------------------|
| session_id | string | The session identifier used or created. |
| message | string  | Echo of the sent message or a response. |
| urgent  | boolean | Flag indicating if the response needs urgent attention. |

#### Example Request

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
-H "Content-Type: application/json" \
-d '{"user_id": "12345", "message": "Hello, I need some advice."}'
```

#### Example Response

```json
{
  "session_id": "abc123",
  "message": "Hello, I need some advice.",
  "urgent": false
}
```

### GET /session/{session_id}

#### Description
Retrieve details of a specific chat session by its session ID. Use this endpoint to track or obtain historical chat information.

#### Response Body

Varies based on stored session details. Typically includes state and history of the session.

#### Example Request

```bash
curl "http://localhost:8000/api/v1/session/abc123"
```

### POST /recommend

#### Description
Receive health recommendations based on patient details such as age, gender, and symptoms. Use this to get AI-generated guidance tailored to patient input.

#### Request Body

| Field        | Type   | Required | Description                             |
|--------------|--------|----------|-----------------------------------------|
| age          | int    | Yes      | Age of the patient.                     |
| gender       | string | Yes      | Gender of the patient.                  |
| severity     | string | Yes      | Severity of the presented symptoms.     |
| duration_days| int    | Yes      | Duration for which symptoms persisted.  |
| symptoms     | string | Yes      | Description of symptoms.                |

#### Response Body

| Field             | Type   | Description                                        |
|-------------------|--------|----------------------------------------------------|
| session_id        | string | Identifier for the recommendation session.         |
| urgency_level     | string | Urgency level: low, moderate, high, emergency.     |
| next_step         | string | Suggested next action: monitor, teleconsult, etc.  |
| suggested_specialty | string | Suggested specialty for consultation, if applicable. |
| patient_message   | string | Message intended for patient guidance.             |
| reasoning         | string | Explanation of the recommendation.                 |

#### Example Request

```bash
curl -X POST "http://localhost:8000/api/v1/recommend" \
-H "Content-Type: application/json" \
-d '{"age": 45, "gender": "female", "severity": "moderate", "duration_days": 3, "symptoms": "headache and dizziness"}'
```

#### Example Response

```json
{
  "session_id": "rec456",
  "urgency_level": "moderate",
  "next_step": "teleconsult",
  "suggested_specialty": "neurology",
  "patient_message": "We suggest a teleconsult with a neurologist.",
  "reasoning": "The symptoms suggest possible neurological issues."
}
```

### POST /reports/upload

#### Description
Upload a clinical report for analysis and receive detailed findings. Use when you need insights and explanations from document data.

#### Request Body

| Field      | Type       | Required | Description                                                   |
|------------|------------|----------|---------------------------------------------------------------|
| session_id | string     | Yes      | Identifier for the analysis session.                         |
| file       | UploadFile | Yes      | The report file to be uploaded and analyzed.                  |

#### Response Body

| Field       | Type  | Description                                     |
|-------------|-------|-------------------------------------------------|
| session_id  | string| The analysis session identifier.                |
| findings    | dict  | Key findings extracted from the report.         |
| explanation | string| Detailed explanation of the findings.           |

#### Example Request

```bash
curl -X POST "http://localhost:8000/api/v1/reports/upload" \
-F "session_id=ses789" \
-F "file=@/path/to/report.pdf"
```

#### Example Response

```json
{
  "session_id": "ses789",
  "findings": {
    "blood_pressure": "normal",
    "cholesterol": "elevated"
  },
  "explanation": "Cholesterol levels are above normal, suggesting a need for dietary consultation."
}
```

### GET /reports/{report_id}

#### Description
Retrieve a processed report by its ID. Use for accessing previously generated analyses.

#### Response Body

Contents depend on the specific report queried. Typically includes findings and analytical notes.

#### Example Request

```bash
curl "http://localhost:8000/api/v1/reports/123456"
```

## Error Responses

- 400 Bad Request: Invalid input data provided.
- 401 Unauthorized: Authentication failed.
- 403 Forbidden: Access to the resource is denied.
- 404 Not Found: The requested resource does not exist.
- 500 Internal Server Error: A server side error occurred.

This API is designed to facilitate interactions with patient data and provide insights through AI-driven analysis. Ensure all payloads are correctly formatted and valid to receive optimal responses.