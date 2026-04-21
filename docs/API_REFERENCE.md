---
tags: [api, reference, auto-generated]
updated: "2026-04-21 17:19"
---

> Auto-generated on 2026-04-21 17:19 by `scripts/update_docs.py`. Do not edit manually.

# API Reference

Welcome to the Med360 Patient AI API Reference. This API serves as an AI intelligence layer for the Med360 patient app, enabling chat interactions, report uploads, and medical recommendations. The base URL pattern for all API calls is: `/api/v1`.

## Endpoints

### POST /chat/sessions

#### Description
This endpoint starts a new chat session, optionally linked to a specific report. Use this to initiate a conversation session for a patient.

#### Request Body

| Field     | Type   | Required | Description                            |
|-----------|--------|----------|----------------------------------------|
| report_id | string | No       | Optional report ID to attach to the chat session. |

#### Response Body

| Field   | Type   | Description      |
|---------|--------|------------------|
| chat_id | string | The ID of the newly created chat session. |

#### Example Request

```bash
curl -X POST "https://api.med360.com/api/v1/chat/sessions" -H "Content-Type: application/json" -d '{"report_id": "xyz123"}'
```

#### Example Response

```json
{
  "chat_id": "abc456"
}
```

### POST /chat/sessions/{chat_id}/message

#### Description
Send a message in an existing chat session. This endpoint facilitates ongoing conversation in the chat session.

#### Request Body

| Field   | Type   | Required | Description               |
|---------|--------|----------|---------------------------|
| message | string | Yes      | Message to send to the AI. |

#### Response Body

| Field           | Type     | Description                       |
|-----------------|----------|-----------------------------------|
| chat_id         | string   | ID of the chat.                   |
| model_used      | string   | Name of the AI model used.        |
| usage           | dict     | Usage statistics.                 |
| turn            | ChatTurn | Data from the conversation turn.  |
| recommendation  | object   | Recommendation if applicable.     |

#### Example Request

```bash
curl -X POST "https://api.med360.com/api/v1/chat/sessions/abc456/message" -H "Content-Type: application/json" -d '{"message": "What should I do about my headache?"}'
```

#### Example Response

```json
{
  "chat_id": "abc456",
  "model_used": "gpt-3",
  "usage": {"prompt_tokens": 20, "completion_tokens": 30},
  "turn": {
    "user": "What should I do about my headache?",
    "assistant": "Based on your symptoms, it is recommended to rest and stay hydrated."
  },
  "recommendation": null
}
```

### POST /chat/sessions/{chat_id}/report

#### Description
Attach a report to an existing chat session. Useful for correlating patient reports with chat transcripts.

#### Request Body

| Field     | Type   | Required | Description           |
|-----------|--------|----------|-----------------------|
| report_id | string | Yes      | ID of the report to attach. |

#### Response Body

| Field      | Type   | Description                |
|------------|--------|----------------------------|
| chat_id    | string | ID of the chat session.    |
| report_type | string | Type of the attached report. |
| urgency    | string | Urgency level of the report. |

#### Example Request

```bash
curl -X POST "https://api.med360.com/api/v1/chat/sessions/abc456/report" -H "Content-Type: application/json" -d '{"report_id": "xyz123"}'
```

#### Example Response

```json
{
  "chat_id": "abc456",
  "report_type": "blood test",
  "urgency": "high"
}
```

### GET /chat/sessions/{chat_id}

#### Description
Retrieve the details of a specific chat session using its unique ID.

#### Example Request

```bash
curl -X GET "https://api.med360.com/api/v1/chat/sessions/abc456"
```

#### Example Response

```json
{
  "chat_id": "abc456",
  "messages": [
    {
      "sender": "user",
      "text": "What should I do about my headache?"
    },
    {
      "sender": "assistant",
      "text": "Based on your symptoms, it is recommended to rest and stay hydrated."
    }
  ]
}
```

### POST /recommend

#### Description
Generate a medical recommendation based on patient information provided.

#### Request Body

| Field          | Type   | Required | Description                        |
|----------------|--------|----------|------------------------------------|
| age            | int    | Yes      | Age of the patient (1-120).        |
| gender         | string | Yes      | Gender of the patient.             |
| severity       | string | Yes      | Severity of the condition.         |
| duration_days  | int    | Yes      | Duration of symptoms in days.      |
| symptoms       | string | Yes      | Symptoms description (10-1000 chars). |

#### Response Body

| Field           | Type   | Description                |
|-----------------|--------|----------------------------|
| session_id      | string | ID of the recommendation session. |
| recommendation  | object | The recommendation data.   |

#### Example Request

```bash
curl -X POST "https://api.med360.com/api/v1/recommend" -H "Content-Type: application/json" -d '{"age": 30, "gender": "female", "severity": "medium", "duration_days": 5, "symptoms": "Persistent headache and dizziness."}'
```

#### Example Response

```json
{
  "session_id": "session789",
  "recommendation": {
    "treatment": "Take ibuprofen as needed and consult a doctor if symptoms persist.",
    "urgency": "medium"
  }
}
```

### POST /reports/upload

#### Description
Upload a report file to be interpreted by the AI. Supports PDF and plain-text formats.

#### Response Body

| Field       | Type               | Description                    |
|-------------|--------------------|--------------------------------|
| report_id   | string             | ID of the uploaded report.     |
| model_used  | string             | Name of the AI model used.     |
| usage       | dict               | Usage statistics.              |
| findings    | ReportFindings     | Report interpretation findings.|

#### Example Request

```bash
curl -X POST "https://api.med360.com/api/v1/reports/upload" -F "file=@/path/to/report.pdf"
```

#### Example Response

```json
{
  "report_id": "report567",
  "model_used": "report-analyzer-1.0",
  "usage": {"tokens_used": 150},
  "findings": {
    "analysis": "The report indicates elevated blood sugar levels.",
    "recommendation": "Consider a diet plan consultation."
  }
}
```

## Error Responses

The API can return several error responses. Here are the most common ones:

- **404 Not Found:** The requested resource was not found, such as an invalid `chat_id`, `session_id`, or `report_id`.
- **415 Unsupported Media Type:** Occurs when the uploaded report file is not in a supported format (neither PDF nor plain-text).
- **400 Bad Request:** Typically due to invalid input, such as required fields missing or invalid field formats.

Use this reference to integrate with the Med360 Patient AI API effectively, ensuring appropriate handling of responses and errors.