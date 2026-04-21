> Auto-generated on 2026-04-21 14:18 by `scripts/update_docs.py`. Do not edit manually.

# Data Models

This documentation outlines the various data models used in our application, which facilitate the storage and manipulation of medical session data within a JSON file-based database system. Each model captures specific aspects of the clinical, user, and recommendation data relevant to enhancing patient care. Below, you will find a description of each model, including their fields, data types, and how these models interconnect.

## ClinicalState

**Purpose**: Represents the medical state of a patient during a session.

| Field Name           | Type                                        | Required | Default        | Description                                               |
|----------------------|---------------------------------------------|----------|----------------|-----------------------------------------------------------|
| id                   | ObjectId                                    | Yes      | Generated      | Unique identifier for the record.                         |
| session_id           | ObjectId                                    | Yes      | None           | ID of the associated session.                             |
| chief_complaint      | str                                          | No       | None           | Chief complaint of the patient.                           |
| symptoms             | list[str]                                   | No       | []             | List of symptoms reported.                                |
| duration             | str                                          | No       | None           | Duration of illness.                                      |
| severity             | str                                          | No       | None           | Severity level of symptoms.                               |
| chronic_conditions   | list[str]                                   | No       | []             | List of existing chronic conditions.                      |
| medications          | list[str]                                   | No       | []             | Medications currently being taken.                        |
| red_flags            | list[str]                                   | No       | []             | Indicators of potential serious conditions.               |
| missing_info         | list[str]                                   | No       | []             | Important information missing in the current assessment.  |
| report_findings_summary | str                                      | No       | None           | Summary of report findings.                               |
| urgency_level        | Literal["low", "moderate", "high", "emergency"] | No   | None           | Estimated urgency of the condition.                       |
| recommendation_status| Literal["pending", "ready"]                 | No       | "pending"      | Status of the clinical recommendation.                    |
| updated_at           | datetime                                    | No       | Current time   | Timestamp for the last update.                            |

**Example JSON Instance**:
```json
{
    "_id": "645a1e123456789012345678",
    "session_id": "645a1e223456789012345679",
    "chief_complaint": "Headache",
    "symptoms": ["Nausea", "Dizziness"],
    "duration": "3 days",
    "severity": "Moderate",
    "chronic_conditions": ["Hypertension"],
    "medications": ["Lisinopril"],
    "red_flags": [],
    "missing_info": ["Blood Pressure Level"],
    "report_findings_summary": "MRI shows no acute findings.",
    "urgency_level": "moderate",
    "recommendation_status": "pending",
    "updated_at": "2023-10-01T12:34:56"
}
```

## Message

**Purpose**: Captures conversation messages between the patient and assistant.

| Field Name | Type                        | Required | Default      | Description                           |
|------------|-----------------------------|----------|--------------|---------------------------------------|
| id         | ObjectId                    | Yes      | Generated    | Unique identifier for the message.    |
| session_id | ObjectId                    | Yes      | None         | ID of the associated session.        |
| role       | Literal["user", "assistant"]| Yes      | None         | The role of the message sender.       |
| content    | str                         | Yes      | None         | The message text content.            |
| created_at | datetime                    | No       | Current time | Timestamp when message was created.  |

**Example JSON Instance**:
```json
{
    "_id": "645a1f123456789012345688",
    "session_id": "645a1f223456789012345689",
    "role": "user",
    "content": "I have a severe headache.",
    "created_at": "2023-10-01T12:35:01"
}
```

## Recommendation

**Purpose**: Suggests clinical pathways and urgency levels for the patient's condition.

| Field Name            | Type                                                                          | Required | Default      | Description                                           |
|-----------------------|-------------------------------------------------------------------------------|----------|--------------|-------------------------------------------------------|
| id                    | ObjectId                                                                      | Yes      | Generated    | Unique identifier for the recommendation.              |
| session_id            | ObjectId                                                                      | Yes      | None         | ID of the associated session.                          |
| urgency_level         | Literal["low", "moderate", "high", "emergency"]                               | Yes      | None         | Urgency of the recommended action.                     |
| suggested_care_pathway| str                                                                            | Yes      | None         | Recommended care pathway description.                  |
| suggested_specialty   | str | None                                                                    | No       | None         | Suggested medical specialty for further action.        |
| next_step             | Literal["monitor", "teleconsult", "home_visit", "specialist", "emergency"]    | Yes      | None         | Immediate recommended next step.                       |
| reasoning             | str                                                                            | Yes      | None         | Reasoning behind the recommendation.                   |
| patient_message       | str                                                                            | Yes      | None         | Message to convey to the patient.                      |
| created_at            | datetime                                                                       | No       | Current time | Timestamp when recommendation was created.             |

**Example JSON Instance**:
```json
{
    "_id": "645a1g123456789012345699",
    "session_id": "645a1g223456789012345700",
    "urgency_level": "high",
    "suggested_care_pathway": "Immediate evaluation recommended in ER.",
    "suggested_specialty": "Neurology",
    "next_step": "emergency",
    "reasoning": "Severe headache with potential neurological signs.",
    "patient_message": "Please visit the nearest emergency room immediately.",
    "created_at": "2023-10-01T12:35:30"
}
```

## Report

**Purpose**: Holds the details and findings of a clinical report for a session.

| Field Name | Type       | Required | Default      | Description                                 |
|------------|------------|----------|--------------|---------------------------------------------|
| id         | ObjectId   | Yes      | Generated    | Unique identifier for the report.           |
| session_id | ObjectId   | Yes      | None         | ID of the associated session.               |
| filename   | str        | Yes      | None         | Name of the report file.                    |
| findings   | dict       | No       | {}           | Detailed findings from the report.          |
| created_at | datetime   | No       | Current time | Timestamp when the report was created.      |

**Example JSON Instance**:
```json
{
    "_id": "645a1h123456789012345079",
    "session_id": "645a1h223456789012345080",
    "filename": "session_report_001.pdf",
    "findings": {
        "blood_test_results": {
            "WBC": "7.4",
            "RBC": "4.9"
        }
    },
    "created_at": "2023-10-01T12:40:25"
}
```

## ReportFinding

**Purpose**: Details specific findings and markers in a clinical report.

| Field Name     | Type     | Required | Default      | Description                                         |
|----------------|----------|----------|--------------|-----------------------------------------------------|
| id             | ObjectId | Yes      | Generated    | Unique identifier for the report finding.            |
| session_id     | ObjectId | Yes      | None         | ID of the associated session.                       |
| abnormal_values| list[dict]| No      | []           | List of abnormal laboratory values and markers.     |
| normal_values  | list[dict]| No      | []           | List of normal laboratory values.                   |
| notable_markers| list[str]| No      | []           | Noteworthy markers indicating critical conditions.  |
| summary        | str | None| No     | None         | Summary of all the findings.                        |
| created_at     | datetime| No       | Current time | Timestamp when the report finding was created.      |

**Example JSON Instance**:
```json
{
    "_id": "645a1i123456789012345089",
    "session_id": "645a1i223456789012345090",
    "abnormal_values": [{"Glucose": "105 mg/dL"}],
    "normal_values": [{"Cholesterol": "180 mg/dL"}],
    "notable_markers": ["Elevated Glucose Level"],
    "summary": "Moderate glucose elevation, monitor dietary intake.",
    "created_at": "2023-10-01T12:45:00"
}
```

## Session

**Purpose**: Represents a user session encompassing various interactions and data exchanges.

| Field Name | Type       | Required | Default      | Description                               |
|------------|------------|----------|--------------|-------------------------------------------|
| id         | ObjectId   | Yes      | Generated    | Unique identifier for the session.        |
| user_id    | str        | Yes      | None         | Identifier for the user of the session.   |
| messages   | list[dict] | No       | []           | Collection of messages exchanged.         |
| created_at | datetime   | No       | Current time | Timestamp for session initiation.         |
| updated_at | datetime   | No       | Current time | Timestamp for the last session update.    |

**Example JSON Instance**:
```json
{
    "_id": "645a1j123456789012345100",
    "user_id": "abc123",
    "messages": [
        {"role": "user", "content": "I have a cough."},
        {"role": "assistant", "content": "Please check your temperature."}
    ],
    "created_at": "2023-10-01T12:50:00",
    "updated_at": "2023-10-01T12:51:00"
}
```

## User

**Purpose**: Stores user-specific details such as contact information and demographics.

| Field Name    | Type     | Required | Default      | Description                                     |
|---------------|----------|----------|--------------|-------------------------------------------------|
| id            | ObjectId | Yes      | Generated    | Unique user identifier.                         |
| name          | str      | Yes      | None         | Full name of the user.                          |
| phone         | str | None| No      | None         | User's phone number.                            |
| email         | str | None| No      | None         | Email address for user contact.                 |
| date_of_birth | str | None| No      | None         | Birthdate of the user.                          |
| gender        | str | None| No      | None         | Gender designation of the user.                 |
| created_at    | datetime | No       | Current time | Account creation timestamp.                     |

**Example JSON Instance**:
```json
{
    "_id": "645a1k123456789012345110",
    "name": "John Doe",
    "phone": "+1234567890",
    "email": "johndoe@example.com",
    "date_of_birth": "1980-01-01",
    "gender": "male",
    "created_at": "2023-10-01T12:55:00"
}
```

## Model Relationships

The data models relate to one another to form a complete system of patient interaction and recommendation:

- **Users** initiate and participate in **Sessions**.
- A **Session** contains multiple **Messages** exchanged between users and assistants.
- **ClinicalState** is linked to a **Session**, capturing the patient's health state.
- **Recommendation** provides advice based on the **ClinicalState** and is tied to a session.
- **Reports** and **ReportFindings** provide detailed analyses and findings, aligned with a session's investigation and results.
- All models are interconnected through the `session_id`, allowing traceability of actions and data throughout various processes.

These models collectively support the clinical data documentation, providing a structured approach to medical assessments, session handling, and patient follow-up.