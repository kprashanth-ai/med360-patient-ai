> Auto-generated on 2026-04-21 14:40 by `scripts/update_docs.py`. Do not edit manually.

# Data Models

This document provides an overview of the data models used in our application. These models represent various entities such as clinical states, messages, recommendations, reports, sessions, and users, and are stored as JSON records within our data storage system. Each model is described in terms of its purpose, fields, and an example JSON instance. Additionally, we explore the relationships between these models.

## Clinical State

### Purpose
The `ClinicalState` model represents the health status and related information of a session involving a patient.

### Fields
| Field Name            | Type                                                      | Required | Default | Description                                              |
|-----------------------|-----------------------------------------------------------|----------|---------|----------------------------------------------------------|
| `id`                  | `ObjectId`                                                | No       | Auto    | Unique identifier for the clinical state.                |
| `session_id`          | `ObjectId`                                                | Yes      |         | Identifier linking to the associated session.            |
| `chief_complaint`     | `str` or `None`                                           | No       | None    | Main complaint of the patient.                           |
| `symptoms`            | `list[str]`                                               | No       | `[]`    | List of symptoms reported by the patient.                |
| `duration`            | `str` or `None`                                           | No       | None    | Duration of the symptoms.                                |
| `severity`            | `str` or `None`                                           | No       | None    | Severity of the symptoms.                                |
| `chronic_conditions`  | `list[str]`                                               | No       | `[]`    | List of existing chronic conditions.                     |
| `medications`         | `list[str]`                                               | No       | `[]`    | Medications the patient is taking.                       |
| `red_flags`           | `list[str]`                                               | No       | `[]`    | Red flag indicators for urgent conditions.               |
| `missing_info`        | `list[str]`                                               | No       | `[]`    | Information missing from the patient's record.           |
| `report_findings_summary` | `str` or `None`                                         | No       | None    | Summary of findings from reports.                        |
| `urgency_level`       | `Literal["low", "moderate", "high", "emergency"]` or `None` | No       | None    | Indicates the level of urgency.                          |
| `recommendation_status` | `Literal["pending", "ready"]`                             | No       | `'pending'` | Status of recommendations relative to the session.      |
| `updated_at`          | `datetime`                                                | No       | Auto    | Timestamp for the last update of the record.             |

### Example JSON Instance
```json
{
    "_id": "60fa3ca0678e30e1d8b7b574",
    "session_id": "60fa3ca0678e30e1d8b7b571",
    "chief_complaint": "Headache",
    "symptoms": ["nausea", "blurred vision"],
    "duration": "3 days",
    "severity": "moderate",
    "chronic_conditions": ["hypertension"],
    "medications": ["aspirin"],
    "red_flags": ["sudden onset"],
    "missing_info": ["family history"],
    "report_findings_summary": null,
    "urgency_level": "high",
    "recommendation_status": "pending",
    "updated_at": "2023-09-10T12:34:56.789Z"
}
```

## Message

### Purpose
The `Message` model logs the interaction through messages between a user and an assistant during a session.

### Fields
| Field Name | Type                                | Required | Default | Description                                       |
|------------|-------------------------------------|----------|---------|---------------------------------------------------|
| `id`       | `ObjectId`                          | No       | Auto    | Unique identifier for the message.                |
| `session_id` | `ObjectId`                        | Yes      |         | Identifier linking to the associated session.     |
| `role`     | `Literal["user", "assistant"]`      | Yes      |         | The role of the sender: user or assistant.        |
| `content`  | `str`                               | Yes      |         | The text content of the message.                  |
| `created_at` | `datetime`                        | No       | Auto    | Timestamp for when the message was created.       |

### Example JSON Instance
```json
{
    "_id": "60fa3ca0678e30e1d8b7b575",
    "session_id": "60fa3ca0678e30e1d8b7b571",
    "role": "user",
    "content": "I have a headache and feel nauseous.",
    "created_at": "2023-09-10T12:30:00Z"
}
```

## Recommendation

### Purpose
The `Recommendation` model provides medical advice and suggests how a user's medical condition should be managed.

### Fields
| Field Name             | Type                                                      | Required | Default | Description                                           |
|------------------------|-----------------------------------------------------------|----------|---------|-------------------------------------------------------|
| `id`                   | `ObjectId`                                                | No       | Auto    | Unique identifier for the recommendation.             |
| `session_id`           | `ObjectId`                                                | Yes      |         | Identifier linking to the associated session.         |
| `urgency_level`        | `Literal["low", "moderate", "high", "emergency"]`         | Yes      |         | Specifies the urgency level of the condition.         |
| `suggested_care_pathway` | `str`                                                   | Yes      |         | Description of the proposed care pathway.             |
| `suggested_specialty`  | `str` or `None`                                           | No       | None    | Recommended medical specialty for consultation.       |
| `next_step`            | `Literal["monitor", "teleconsult", "home_visit", "specialist", "emergency"]` | Yes | | Next recommended action for the user.                |
| `reasoning`            | `str`                                                     | Yes      |         | Explanation behind the recommendation.                |
| `patient_message`      | `str`                                                     | Yes      |         | Information intended for the patient.                 |
| `created_at`           | `datetime`                                                | No       | Auto    | Timestamp for when the recommendation was created.    |

### Example JSON Instance
```json
{
    "_id": "60fa3ca0678e30e1d8b7b576",
    "session_id": "60fa3ca0678e30e1d8b7b571",
    "urgency_level": "high",
    "suggested_care_pathway": "Immediate consultation with a neurologist.",
    "suggested_specialty": "Neurology",
    "next_step": "specialist",
    "reasoning": "Symptoms suggest a neurological evaluation is necessary.",
    "patient_message": "We recommend that you seek a consultation with a neurologist as soon as possible.",
    "created_at": "2023-09-10T12:35:00Z"
}
```

## Report

### Purpose
The `Report` model stores uploaded medical reports related to a session.

### Fields
| Field Name | Type        | Required | Default | Description                                  |
|------------|-------------|----------|---------|----------------------------------------------|
| `id`       | `ObjectId`  | No       | Auto    | Unique identifier for the report.            |
| `session_id` | `ObjectId`| Yes      |         | Identifier linking to the associated session.|
| `filename` | `str`       | Yes      |         | Name of the file for identification.         |
| `findings` | `dict`      | No       | `{}`    | Contains the findings from the report.       |
| `created_at` | `datetime`| No       | Auto    | Timestamp for when the report was created.   |

### Example JSON Instance
```json
{
    "_id": "60fa3ca0678e30e1d8b7b577",
    "session_id": "60fa3ca0678e30e1d8b7b571",
    "filename": "brain_mri_report.pdf",
    "findings": {"tumor_presence": false, "vascular_issues": true},
    "created_at": "2023-09-10T12:40:00Z"
}
```

## Report Finding

### Purpose
The `ReportFinding` model captures detailed findings from medical reports, emphasizing notable markers and results.

### Fields
| Field Name       | Type        | Required | Default | Description                                           |
|------------------|-------------|----------|---------|-------------------------------------------------------|
| `id`             | `ObjectId`  | No       | Auto    | Unique identifier for the report finding.             |
| `session_id`     | `ObjectId`  | Yes      |         | Identifier linking to the associated session.         |
| `abnormal_values` | `list[dict]`| No      | `[]`    | Lists abnormal values detected in the findings.       |
| `normal_values`  | `list[dict]`| No       | `[]`    | Lists normal values identified in the findings.       |
| `notable_markers` | `list[str]`| No       | `[]`    | Contains markers of significant interest in the report findings. |
| `summary`        | `str` or `None` | No   | None    | Summary of the report's critical findings.            |
| `created_at`     | `datetime`  | No       | Auto    | Timestamp for when the report finding was created.    |

### Example JSON Instance
```json
{
    "_id": "60fa3ca0678e30e1d8b7b578",
    "session_id": "60fa3ca0678e30e1d8b7b571",
    "abnormal_values": [{"glucose": "high"}],
    "normal_values": [{"cholesterol": "normal"}],
    "notable_markers": ["C-reactive protein"],
    "summary": "The report indicates inflammation markers are elevated.",
    "created_at": "2023-09-10T12:45:00Z"
}
```

## Session

### Purpose
The `Session` model logs user interactions and events throughout a single session.

### Fields
| Field Name | Type        | Required | Default | Description                                  |
|------------|-------------|----------|---------|----------------------------------------------|
| `id`       | `ObjectId`  | No       | Auto    | Unique identifier for the session.           |
| `user_id`  | `str`       | Yes      |         | Identifier of the user participating in the session.|
| `messages` | `list[dict]`| No       | `[]`    | Collection of messages exchanged during the session.|
| `created_at` | `datetime`| No       | Auto    | Timestamp for when the session was created.  |
| `updated_at` | `datetime`| No       | Auto    | Timestamp for the last update of the session.|

### Example JSON Instance
```json
{
    "_id": "60fa3ca0678e30e1d8b7b571",
    "user_id": "user123",
    "messages": [{"role": "user", "content": "Hello"}],
    "created_at": "2023-09-10T12:00:00Z",
    "updated_at": "2023-09-10T12:50:00Z"
}
```

## User

### Purpose
The `User` model contains essential information about the users.

### Fields
| Field Name     | Type        | Required | Default | Description                                      |
|----------------|-------------|----------|---------|--------------------------------------------------|
| `id`           | `ObjectId`  | No       | Auto    | Unique identifier for the user.                  |
| `name`         | `str`       | Yes      |         | Full name of the user.                           |
| `phone`        | `str` or `None` | No   | None    | Contact phone number of the user.                |
| `email`        | `str` or `None` | No   | None    | Email address of the user.                       |
| `date_of_birth` | `str` or `None` | No  | None    | User's date of birth.                            |
| `gender`       | `str` or `None` | No   | None    | Gender of the user.                              |
| `created_at`   | `datetime`  | No       | Auto    | Timestamp for when the user record was created.  |

### Example JSON Instance
```json
{
    "_id": "60fa3ca0678e30e1d8b7b573",
    "name": "John Doe",
    "phone": "123-456-7890",
    "email": "johndoe@example.com",
    "date_of_birth": "1985-05-15",
    "gender": "male",
    "created_at": "2023-09-10T12:10:00Z"
}
```

## Relationships Between Models

The models are interrelated to facilitate comprehensive data management and interaction workflows:

- **User** → **Session**: A user can initiate multiple sessions, linking each session to a unique user ID.
- **Session** → **Message**: Each session can contain multiple messages exchanged between the user and an assistant.
- **Session** → **Clinical State**/**Recommendation**/**Report**/**Report Finding**: A session can have associated clinical states, recommendations, reports, and report findings, all linked by session IDs.
- **Clinical State** ↔ **Recommendation**: Recommendations are often influenced by the clinical state details, highlighting a reciprocal relation where the clinical state data guides the recommendation outcomes.

These structured relationships ensure data consistency and integrity across systems, optimizing healthcare interaction workflows.