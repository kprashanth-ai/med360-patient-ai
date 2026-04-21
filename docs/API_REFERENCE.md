> Auto-generated on 2026-04-21 14:40 by `scripts/update_docs.py`. Do not edit manually.

# API Reference

Welcome to the API Reference for the Med360 Patient AI. This API provides an AI-based intelligence layer for patient management, enabling chat interactions, medical recommendations, and report processing functionalities.

The base URL pattern for accessing the API is `/api/v1`.

## POST /chat

### Description
Initiates a chat interaction within the system. Use this endpoint to send a message to the chat service and receive a response, possibly updating or creating a session.

### Request Body

| Field       | Type   | Required | Description                       |
|-------------|--------|----------|-----------------------------------|
| user_id     | string | Yes      | Unique identifier for the user.   |
| session_id  | string | No       | Existing session identifier.      |
| message     | string | Yes      | The message content to send.      |

### Response Body

| Field       | Type    | Description                             |
|-------------|---------|-----------------------------------------|
| session_id  | string  | The session identifier for the chat.    |
| message     | string  | The response message from the system.   |
| urgent      | boolean | Indicates if the message is urgent.     |

### Example Request

```bash
curl -X POST "http://localhost/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{ "user_id": "12345", "message": "Hello, I need help" }'
```

### Example Response

```json
{
  "session_id": "abcde-12345",
  "message": "Hello, how can I assist you today?",
  "urgent": false
}
```

## GET /session/{session_id}

### Description
Fetches details of a particular session using its unique session ID. Use this to retrieve session-specific information.

### Example Request

```bash
curl -X GET "http://localhost/api/v1/session/abcde-12345"
```

### Example Response

```json
{
  "session_id": "abcde-12345",
  "user_data": {...}
}
```

## POST /recommend

### Description
Provides healthcare recommendations based on the patient's health status. Submit the health details to get a tailored recommendation.

### Request Body

| Field         | Type   | Required | Description                                  |
|---------------|--------|----------|----------------------------------------------|
| age           | int    | Yes      | The patient's age (1 to 120 years).          |
| gender        | string | Yes      | The patient's gender ("male", "female", "other"). |
| severity      | string | Yes      | Severity of symptoms ("low", "medium", "high"). |
| duration_days | int    | Yes      | Duration of symptoms in days (1 to 3650).    |
| symptoms      | string | Yes      | Description of symptoms (10 to 1000 chars).  |

### Response Body

| Field           | Type                     | Description                                   |
|-----------------|--------------------------|-----------------------------------------------|
| session_id      | string                   | Unique session identifier.                    |
| recommendation  | `RecommendationResult`   | Contains recommendation details.              |

### Example Request

```bash
curl -X POST "http://localhost/api/v1/recommend" \
  -H "Content-Type: application/json" \
  -d '{ "age": 35, "gender": "male", "severity": "medium", "duration_days": 5, "symptoms": "fever and headache" }'
```

### Example Response

```json
{
  "session_id": "def456-67890",
  "recommendation": {
    "urgency_level": "moderate",
    "next_step": "teleconsult",
    "suggested_specialty": "general_medicine",
    "patient_message": "We recommend a teleconsultation.",
    "reasoning": "Based on your symptoms and severity."
  }
}
```

## GET /sessions

### Description
Lists recent sessions based on a provided limit. Retrieve information on how many sessions have been recently processed.

### Parameters

| Parameter | Type  | Description                     |
|-----------|-------|---------------------------------|
| limit     | int   | Optional, max number of sessions to return, default is 20. |

### Example Request

```bash
curl -X GET "http://localhost/api/v1/sessions?limit=5"
```

### Example Response

```json
[
  { "session_id": "abcde-12345", "summary": {...} },
  { "session_id": "def456-67890", "summary": {...} }
]
```

## GET /sessions/{session_id}

### Description
Fetches details for a specific session using `session_id`. Use this to examine a single session's details further.

### Example Request

```bash
curl -X GET "http://localhost/api/v1/sessions/abcde-12345"
```

### Example Response

```json
{
  "session_id": "abcde-12345",
  "details": {...}
}
```

## POST /reports/upload

### Description
Uploads a medical report file associated with a session. This endpoint is used to analyze the report and return findings.

### Request Body

| Field      | Type                   | Required | Description               |
|------------|------------------------|----------|---------------------------|
| session_id | string                 | Yes      | The session identifier.   |
| file       | `UploadFile` (Binary)  | Yes      | The file to be uploaded.  |

### Response Body

| Field       | Type   | Description                                     |
|-------------|--------|-------------------------------------------------|
| session_id  | string | Session associated with the report.             |
| findings    | dict   | Parsed findings from the uploaded report.       |
| explanation | string | Explanation of the report findings.             |

### Example Request

```bash
curl -X POST "http://localhost/api/v1/reports/upload" \
  -F "session_id=abcde-12345" \
  -F "file=@report.pdf"
```

### Example Response

```json
{
  "session_id": "abcde-12345",
  "findings": { "test": "value" },
  "explanation": "Findings explained."
}
```

## GET /reports/{report_id}

### Description
Retrieves report details identified by its report ID.

### Example Request

```bash
curl -X GET "http://localhost/api/v1/reports/abcd1234"
```

### Example Response

```json
{
  "_id": "abcd1234",
  "session_id": "abcde-12345",
  "report_content": {...}
}
```

## Error Responses

| Status Code | Description                          |
|-------------|--------------------------------------|
| 400         | Bad request (e.g., validation error) |
| 404         | Resource not found                   |
| 500         | Internal server error                |

This concludes the current API documentation. For further information, please contact the support team.