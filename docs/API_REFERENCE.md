> Auto-generated on 2026-04-21 14:18 by `scripts/update_docs.py`. Do not edit manually.

# API Reference

This API serves as the AI intelligence layer for the Med360 patient app, enabling features like chat interaction, medical recommendations, and report processing. The base URL pattern for the API is `/api/v1`.

## Endpoints

### POST /chat

**Description:**  
This endpoint begins a chat session or continues an existing chat session. It is used for communication between users and the AI system.

**Request Body:**

| Field     | Type   | Required | Description                                |
|-----------|--------|----------|--------------------------------------------|
| user_id   | string | Yes      | Unique identifier for the user.            |
| session_id| string | No       | Identifier for an existing chat session.   |
| message   | string | Yes      | The user's message to the AI chatbot.      |

**Response Body:**

| Field     | Type    | Description                              |
|-----------|---------|------------------------------------------|
| session_id| string  | The session identifier.                  |
| message   | string  | AI's response message.                   |
| urgent    | boolean | Indicates if there's an urgent response. |

**Example Request:**

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
-H "Content-Type: application/json" \
-d '{"user_id": "user123", "message": "Hello AI"}'
```

**Example Response:**

```json
{
  "session_id": "sess567",
  "message": "Hello, how can I assist you today?",
  "urgent": false
}
```

### GET /session/{session_id}

**Description:**  
Fetches detailed information about a specific chat session.

**Example Request:**

```bash
curl -X GET "http://localhost:8000/api/v1/session/sess567"
```

**Example Response:**

```json
{
  "session_id": "sess567",
  "messages": [
    {"from": "user", "content": "Hello AI"},
    {"from": "ai", "content": "Hello, how can I assist you today?"}
  ]
}
```

### POST /recommend

**Description:**  
Provides medical recommendations based on patient symptoms and conditions.

**Request Body:**

| Field         | Type   | Required | Description                              |
|---------------|--------|----------|------------------------------------------|
| age           | int    | Yes      | Age of the patient.                      |
| gender        | string | Yes      | Gender of the patient.                   |
| severity      | string | Yes      | Severity of the condition.               |
| duration_days | int    | Yes      | Duration of symptoms in days.            |
| symptoms      | string | Yes      | Summary of the symptoms.                 |

**Response Body:**

| Field               | Type   | Description                                     |
|---------------------|--------|-------------------------------------------------|
| urgency_level       | string | Urgency level of the condition.                 |
| next_step           | string | Recommended next step for the patient.          |
| suggested_specialty | string | Recommended specialty if applicable.            |
| patient_message     | string | Message for the patient regarding the next steps.|
| reasoning           | string | Explanation of the recommendation.              |

**Example Request:**

```bash
curl -X POST "http://localhost:8000/api/v1/recommend" \
-H "Content-Type: application/json" \
-d '{"age": 30, "gender": "male", "severity": "high", "duration_days": 5, "symptoms": "fever, cough"}'
```

**Example Response:**

```json
{
  "urgency_level": "high",
  "next_step": "teleconsult",
  "suggested_specialty": "Pulmonologist",
  "patient_message": "We recommend a teleconsult with a specialist.",
  "reasoning": "Given the high severity and presented symptoms, a pulmonologist is advisable."
}
```

### POST /reports/upload

**Description:**  
Uploads a medical report for analysis and explanation of findings.

**Request Body:**

Field: 

- `session_id` (form-data, required): Session identifier for the current operation.
- `file` (form-data, required): Report file to be uploaded.

**Response Body:**

| Field      | Type  | Description                             |
|------------|-------|-----------------------------------------|
| session_id | string| The session identifier.                 |
| findings   | dict  | Interpreted findings from the report.   |
| explanation| string| Explanation of the findings.            |

**Example Request:**

```bash
curl -X POST "http://localhost:8000/api/v1/reports/upload" \
-F "session_id=sess789" \
-F "file=@report.pdf"
```

**Example Response:**

```json
{
  "session_id": "sess789",
  "findings": {"blood_pressure": "140/90", "unusual_markers": "true"},
  "explanation": "Elevated blood pressure noted, markers suggest further investigation necessary."
}
```

### GET /reports/{report_id}

**Description:**  
Retrieves a specific report by its ID.

**Example Request:**

```bash
curl -X GET "http://localhost:8000/api/v1/reports/report123"
```

**Example Response:**

```json
{
  "report_id": "report123",
  "session_id": "sess789",
  "findings": {"blood_pressure": "140/90", "unusual_markers": "true"},
  "explanation": "Elevated blood pressure noted, markers suggest further investigation necessary."
}
```

## Error Responses

- `400 Bad Request` - The request was malformed or missing required fields.
- `404 Not Found` - The requested resource does not exist.
- `500 Internal Server Error` - An unexpected error occurred on the server.