> Auto-generated on 2026-04-21 17:10 by `scripts/update_docs.py`. Do not edit manually.

# API Reference

Welcome to the API reference documentation for the Med360 Patient AI. This API provides an AI-powered backend for handling chat sessions, making recommendations, and processing reports for the Med360 patient application. All endpoints are prefixed with `/api/v1`.

## Endpoints

### POST /api/v1/chat/sessions

**Description**: Initiate a new chat session. Optionally associates a report with the session if a `report_id` is provided. Use this endpoint to begin a user interaction session with the AI.

**Request Body**:

| Field     | Type   | Required | Description                |
|-----------|--------|----------|----------------------------|
| report_id | string | No       | ID of the report to attach |

**Response Body**:

| Field   | Type   | Description          |
|---------|--------|----------------------|
| chat_id | string | Unique ID for chat   |

**Example Request**:
```bash
curl -X POST "http://example.com/api/v1/chat/sessions" -H "Content-Type: application/json" -d '{"report_id": "12345"}'
```

**Example Response**:
```json
{
  "chat_id": "abc123"
}
```

### POST /api/v1/chat/sessions/{chat_id}/message

**Description**: Send a message to an existing chat session. Use this to interact with the AI within a session.

**Request Body**:

| Field   | Type   | Required | Description          |
|---------|--------|----------|----------------------|
| message | string | Yes      | User's message       |

**Response Body**:

| Field           | Type   | Description                                  |
|-----------------|--------|----------------------------------------------|
| chat_id         | string | ID of the chat session                       |
| model_used      | string | Model identifier used to process the message |
| usage           | dict   | Information about model usage                |
| turn            | dict   | Details of the chat turn                     |
| recommendation  | dict   | AI recommendation, if any                    |

**Example Request**:
```bash
curl -X POST "http://example.com/api/v1/chat/sessions/abc123/message" -H "Content-Type: application/json" -d '{"message": "Hello!"}'
```

**Example Response**:
```json
{
  "chat_id": "abc123",
  "model_used": "gpt-4",
  "usage": {"tokens": 50},
  "turn": {...},
  "recommendation": {...}
}
```

### POST /api/v1/chat/sessions/{chat_id}/report

**Description**: Attach a report to an ongoing chat session. Useful for incorporating additional contextual data into the chat.

**Request Body**:

| Field     | Type   | Required | Description       |
|-----------|--------|----------|-------------------|
| report_id | string | Yes      | ID of the report  |

**Response Body**:

| Field       | Type   | Description             |
|-------------|--------|-------------------------|
| chat_id     | string | ID of the chat session  |
| report_type | string | Type of attached report |
| urgency     | string | Urgency level           |

**Example Request**:
```bash
curl -X POST "http://example.com/api/v1/chat/sessions/abc123/report" -H "Content-Type: application/json" -d '{"report_id": "67890"}'
```

**Example Response**:
```json
{
  "chat_id": "abc123",
  "report_type": "Blood test",
  "urgency": "High"
}
```

### GET /api/v1/chat/sessions/{chat_id}

**Description**: Retrieve details about a particular chat session. This is useful for reviewing past interactions.

**Example Request**:
```bash
curl -X GET "http://example.com/api/v1/chat/sessions/abc123"
```

### GET /api/v1/chat/sessions

**Description**: List recent chat sessions. Use this to browse through active or recent chats.

**Example Request**:
```bash
curl -X GET "http://example.com/api/v1/chat/sessions?limit=20"
```

### POST /api/v1/recommend

**Description**: Get a health-related recommendation based on provided patient symptoms and details.

**Request Body**:

| Field         | Type    | Required | Description                  |
|---------------|---------|----------|------------------------------|
| age           | integer | Yes      | Age of the patient (1-120)   |
| gender        | string  | Yes      | Gender of the patient        |
| severity      | string  | Yes      | Severity level of symptoms   |
| duration_days | integer | Yes      | Duration of symptoms (days)  |
| symptoms      | string  | Yes      | Detailed patient symptoms    |

**Response Body**:

| Field          | Type   | Description                      |
|----------------|--------|----------------------------------|
| session_id     | string | Unique session ID                |
| recommendation | dict   | Health recommendation            |

**Example Request**:
```bash
curl -X POST "http://example.com/api/v1/recommend" -H "Content-Type: application/json" -d '{"age": 30, "gender": "female", "severity": "medium", "duration_days": 5, "symptoms": "Persistent cough and fever"}'
```

**Example Response**:
```json
{
  "session_id": "rec123",
  "recommendation": {...}
}
```

### POST /api/v1/reports/upload

**Description**: Upload a report file (PDF or plain-text) to the server for processing.

**Response Body**:

| Field       | Type   | Description                        |
|-------------|--------|------------------------------------|
| report_id   | string | ID of the uploaded report          |
| model_used  | string | Model used for interpretation      |
| usage       | dict   | Information about model usage      |
| findings    | dict   | Interpreted findings from the report|

**Example Request**:
```bash
curl -X POST "http://example.com/api/v1/reports/upload" -F 'file=@path/to/report.pdf'
```

**Example Response**:
```json
{
  "report_id": "rep123",
  "model_used": "clarity-ai",
  "usage": {"tokens": 100},
  "findings": {...}
}
```

### GET /api/v1/reports

**Description**: Retrieve a list of available reports.

**Example Request**:
```bash
curl -X GET "http://example.com/api/v1/reports?limit=20"
```

### GET /api/v1/reports/{report_id}

**Description**: Retrieve details of a specific report by ID.

**Example Request**:
```bash
curl -X GET "http://example.com/api/v1/reports/rep123"
```

## Error Responses

- **404 Not Found**: Returned when a specified session or chat is not found.
- **415 Unsupported Media Type**: Returned when attempting to upload files that are not supported formats.
- **Validation Error**: Occurs when request data does not meet required validation rules.