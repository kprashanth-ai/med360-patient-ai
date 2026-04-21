> Auto-generated on 2026-04-21 14:50 by `scripts/update_docs.py`. Do not edit manually.

# API Reference

Welcome to the API reference for Med360 Patient AI. This API provides AI-driven recommendations, chat services, and report analysis for the Med360 patient application. The base URL pattern for this API is `/api/v1`.

## Endpoints

### POST /chat

#### Description
Initiate a chat session or continue an existing conversation with the AI. Use this endpoint to get quick responses to user inquiries during a session.

#### Request Body
| Field     | Type   | Required | Description                            |
|-----------|--------|----------|----------------------------------------|
| user_id   | string | Yes      | Unique identifier for the user.        |
| session_id| string | No       | Optional session ID to continue a chat.|
| message   | string | Yes      | User's message to the chat.            |

#### Response Body
| Field     | Type    | Description                                  |
|-----------|---------|----------------------------------------------|
| session_id| string  | ID of the session.                           |
| message   | string  | AI response to the user's message.           |
| urgent    | boolean | Indicates if the response is marked urgent.  |

#### Example Request
```bash
curl -X POST "http://localhost/api/v1/chat" \
-H "Content-Type: application/json" \
-d '{
  "user_id": "12345",
  "session_id": "abcde",
  "message": "What should I do if I feel dizzy?"
}'
```

#### Example Response
```json
{
  "session_id": "abcde",
  "message": "Please make sure to sit or lie down and take rest.",
  "urgent": false
}
```

---

### POST /recommend

#### Description
Get a personalized recommendation based on user demographic and symptom information. This service uses AI to assess the situation and provide tailored advice.

#### Request Body
| Field        | Type    | Required | Description                              |
|--------------|---------|----------|------------------------------------------|
| age          | integer | Yes      | Age of the user (1-120).                 |
| gender       | string  | Yes      | User's gender ("male", "female", "other").|
| severity     | string  | Yes      | Severity level of the symptoms. ("low", "medium", "high").|
| duration_days| integer | Yes      | Duration of symptoms in days (1-3650).   |
| symptoms     | string  | Yes      | Detailed description of symptoms (10-1000 characters).|

#### Response Body
| Field           | Type                     | Description                      |
|-----------------|--------------------------|----------------------------------|
| session_id      | string                   | Session identifier.              |
| recommendation  | RecommendationResponse   | AI-generated healthcare recommendation.|

#### Example Request
```bash
curl -X POST "http://localhost/api/v1/recommend" \
-H "Content-Type: application/json" \
-d '{
  "age": 30,
  "gender": "female",
  "severity": "medium",
  "duration_days": 5,
  "symptoms": "Persistent headache and nausea"
}'
```

#### Example Response
```json
{
  "session_id": "xyz123",
  "recommendation": {
    "session_id": "xyz123",
    "urgency_level": "moderate",
    "next_step": "teleconsult",
    "suggested_specialty": "neurology",
    "patient_message": "It is recommended to have a teleconsultation with a neurology specialist.",
    "reasoning": "Symptoms consistent with moderate urgency requiring professional consultation."
  }
}
```

---

### POST /reports/upload

#### Description
Upload a medical report file for AI analysis. The service parses the report and provides explanations of findings linked to a specific session.

#### Request Body
| Field     | Type       | Required | Description                      |
|-----------|------------|----------|----------------------------------|
| session_id| string     | Yes      | Session ID associated with the report.|
| file      | UploadFile | Yes      | File upload of the medical report.|

#### Response Body
| Field     | Type   | Description                                         |
|-----------|--------|-----------------------------------------------------|
| session_id| string | Session ID to which the report is associated.       |
| findings  | dict   | Parsed findings from the report.                    |
| explanation| string | Explanation of the findings by the AI.             |

#### Example Request
```bash
curl -X POST "http://localhost/api/v1/reports/upload" \
-F "session_id=abc123" \
-F "file=@path_to_report_file.pdf"
```

#### Example Response
```json
{
  "session_id": "abc123",
  "findings": {
    "blood_pressure": "normal",
    "cholesterol": "high"
  },
  "explanation": "The cholesterol level is high, suggesting dietary adjustments."
}
```

---

### Error Responses

| Status Code | Description              |
|-------------|--------------------------|
| 400         | Bad Request, invalid input data. |
| 404         | Not Found, resource does not exist.|
| 500         | Internal Server Error, something went wrong on the server.|

This documentation provides concise and precise information about how to interact with the Med360 Patient AI API, allowing developers to efficiently implement and use these capabilities within their applications.