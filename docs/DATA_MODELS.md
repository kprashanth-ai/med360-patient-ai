> Auto-generated on 2026-04-21 14:20 by `scripts/update_docs.py`. Do not edit manually.

# Data Models

This document provides a detailed overview of the data models utilized in our application, which are primarily used for managing clinical and patient-related data. The models are defined using Pydantic, facilitating data validation and settings management, and are stored as JSON files for persistence.

## ClinicalState

**Purpose:** Represents the clinical state of a patient session, capturing complaints, symptoms, and other medical conditions.

| Field Name           | Type                                                     | Required | Default                  | Description                                             |
|----------------------|----------------------------------------------------------|----------|--------------------------|---------------------------------------------------------|
| id                   | ObjectId                                                 | No       | Generated automatically  | Unique identifier for the clinical state record.        |
| session_id           | ObjectId                                                 | Yes      | None                     | Identifier linking to the session associated with the clinical state. |
| chief_complaint      | str                                                      | No       | None                     | The chief complaint of the patient.                     |
| symptoms             | list[str]                                                | No       | []                       | List of symptoms observed in the patient.               |
| duration             | str                                                      | No       | None                     | Duration for which symptoms have persisted.             |
| severity             | str                                                      | No       | None                     | Severity of the condition based on symptoms reported.   |
| chronic_conditions   | list[str]                                                | No       | []                       | List of chronic conditions the patient has.             |
| medications          | list[str]                                                | No       | []                       | List of medications the patient is on.                  |
| red_flags            | list[str]                                                | No       | []                       | List of red flags indicating serious conditions.        |
| missing_info         | list[str]                                                | No       | []                       | List of missing information needed for assessment.      |
| report_findings_summary | str                                                   | No       | None                     | Summary of findings from reports.                       |
| urgency_level        | Literal["low", "moderate", "high", "emergency"]          | No       | None                     | Assessed level of urgency for the case.                 |
| recommendation_status| Literal["pending", "ready"]                              | No       | "pending"                | Status of the recommendation advice.                    |
| updated_at           | datetime                                                 | No       | Current timestamp        | Last updated time of the record.                        |

**Example JSON:**
```json
{
  "_id": "60c72b2f9b1e4f1e5f4e4f29",
  "session_id": "60c72b3d9b1e4f1e5f4e4f30",
  "chief_complaint": "Headache",
  "symptoms": ["Headache", "Nausea"],
  "duration": "3 days",
  "severity": "Moderate",
  "chronic_conditions": ["Hypertension"],
  "medications": ["Ibuprofen"],
  "red_flags": ["Blurred vision"],
  "missing_info": [],
  "report_findings_summary": "Inflammation in sinus area",
  "urgency_level": "moderate",
  "recommendation_status": "pending",
  "updated_at": "2023-10-01T12:00:00Z"
}
```

## Message

**Purpose:** Represents a message exchanged between a user and an assistant during a session.

| Field Name | Type                                | Required | Default                  | Description                                 |
|------------|-------------------------------------|----------|--------------------------|---------------------------------------------|
| id         | ObjectId                            | No       | Generated automatically  | Unique identifier for the message.          |
| session_id | ObjectId                            | Yes      | None                     | Identifier linking to the associated session. |
| role       | Literal["user", "assistant"]        | Yes      | None                     | The role of the message sender.             |
| content    | str                                 | Yes      | None                     | The content of the message.                 |
| created_at | datetime                            | No       | Current timestamp        | Timestamp of when the message was created.  |

**Example JSON:**
```json
{
  "_id": "60c72b4f9b1e4f1e5f4e4f31",
  "session_id": "60c72b3d9b1e4f1e5f4e4f30",
  "role": "user",
  "content": "What should I do for my headache?",
  "created_at": "2023-10-01T12:05:00Z"
}
```

## Recommendation

**Purpose:** Provides a recommended course of action based on clinical assessment of a patient session.

| Field Name             | Type                                            | Required | Default                  | Description                                     |
|------------------------|-------------------------------------------------|----------|--------------------------|-------------------------------------------------|
| id                     | ObjectId                                        | No       | Generated automatically  | Unique identifier for the recommendation.       |
| session_id             | ObjectId                                        | Yes      | None                     | Identifier linking to the associated session.   |
| urgency_level          | Literal["low", "moderate", "high", "emergency"] | Yes      | None                     | Assessed urgency level for the recommendation.  |
| suggested_care_pathway | str                                             | Yes      | None                     | Recommended care pathway for the patient.       |
| suggested_specialty    | str                                             | No       | None                     | Suggested medical specialty if applicable.      |
| next_step              | Literal["monitor", "teleconsult", "home_visit", "specialist", "emergency"] | Yes  | None   | Suggested next step to take for the patient.   |
| reasoning              | str                                             | Yes      | None                     | Reasoning for the recommendation provided.      |
| patient_message        | str                                             | Yes      | None                     | Message to be conveyed to the patient.          |
| created_at             | datetime                                        | No       | Current timestamp        | Timestamp when the recommendation was created.  |

**Example JSON:**
```json
{
  "_id": "60c72b5f9b1e4f1e5f4e4f32",
  "session_id": "60c72b3d9b1e4f1e5f4e4f30",
  "urgency_level": "high",
  "suggested_care_pathway": "Immediate consultation with a specialist.",
  "suggested_specialty": "Neurology",
  "next_step": "specialist",
  "reasoning": "The symptoms and red flags indicate a possible neurological issue.",
  "patient_message": "We recommend an immediate consultation with a neurologist.",
  "created_at": "2023-10-01T12:10:00Z"
}
```

## Report

**Purpose:** Holds information about diagnostic reports generated during a session.

| Field Name | Type        | Required | Default                  | Description                                      |
|------------|-------------|----------|--------------------------|--------------------------------------------------|
| id         | ObjectId    | No       | Generated automatically  | Unique identifier for the report.                |
| session_id | ObjectId    | Yes      | None                     | Identifier linking to the associated session.    |
| filename   | str         | Yes      | None                     | The filename of the report document.             |
| findings   | dict        | No       | {}                       | Compiled findings from the report.               |
| created_at | datetime    | No       | Current timestamp        | Timestamp of when the report was created.        |

**Example JSON:**
```json
{
  "_id": "60c72b6f9b1e4f1e5f4e4f33",
  "session_id": "60c72b3d9b1e4f1e5f4e4f30",
  "filename": "headache_report.pdf",
  "findings": {"observations": "No major abnormalities detected apart from sinus inflammation."},
  "created_at": "2023-10-01T12:15:00Z"
}
```

## ReportFinding

**Purpose:** Summarizes key findings from diagnostic reports, highlighting normal and abnormal values.

| Field Name      | Type        | Required | Default                  | Description                                  |
|-----------------|-------------|----------|--------------------------|----------------------------------------------|
| id              | ObjectId    | No       | Generated automatically  | Unique identifier for the report finding.    |
| session_id      | ObjectId    | Yes      | None                     | Identifier linking to the associated session.|
| abnormal_values | list[dict]  | No       | []                       | List of abnormal values noted in tests.      |
| normal_values   | list[dict]  | No       | []                       | List of normal values noted in tests.        |
| notable_markers | list[str]   | No       | []                       | Any notable markers identified in findings.  |
| summary         | str         | No       | None                     | Summary report of the findings.              |
| created_at      | datetime    | No       | Current timestamp        | Timestamp of when findings were recorded.    |

**Example JSON:**
```json
{
  "_id": "60c72b7f9b1e4f1e5f4e4f34",
  "session_id": "60c72b3d9b1e4f1e5f4e4f30",
  "abnormal_values": [{"marker": "WBC", "level": "elevated"}],
  "normal_values": [{"marker": "RBC", "level": "normal"}],
  "notable_markers": ["CRP"],
  "summary": "Elevated WBC counts could indicate a bacterial infection.",
  "created_at": "2023-10-01T12:20:00Z"
}
```

## Session

**Purpose:** Encapsulates a user's interaction session, potentially involving multiple messages and steps.

| Field Name | Type     | Required | Default                  | Description                                   |
|------------|----------|----------|--------------------------|-----------------------------------------------|
| id         | ObjectId | No       | Generated automatically  | Unique identifier for the session.            |
| user_id    | str      | Yes      | None                     | Identifier for the user initiating the session.|
| messages   | list[dict]| No      | []                       | List of messages exchanged during the session.|
| created_at | datetime | No       | Current timestamp        | Timestamp when the session was created.       |
| updated_at | datetime | No       | Current timestamp        | Timestamp of the last session update.         |

**Example JSON:**
```json
{
  "_id": "60c72b3d9b1e4f1e5f4e4f30",
  "user_id": "user123",
  "messages": [{"role": "user", "content": "I have a headache."}],
  "created_at": "2023-10-01T11:50:00Z",
  "updated_at": "2023-10-01T12:25:00Z"
}
```

## User

**Purpose:** Stores user profile information for identification and communication.

| Field Name   | Type     | Required | Default                  | Description                      |
|--------------|----------|----------|--------------------------|----------------------------------|
| id           | ObjectId | No       | Generated automatically  | Unique identifier for the user.  |
| name         | str      | Yes      | None                     | Full name of the user.           |
| phone        | str      | No       | None                     | Phone number of the user.        |
| email        | str      | No       | None                     | Email address of the user.       |
| date_of_birth| str      | No       | None                     | Date of birth of the user.       |
| gender       | str      | No       | None                     | Gender of the user.              |
| created_at   | datetime | No       | Current timestamp        | Timestamp when the user profile was created. |

**Example JSON:**
```json
{
  "_id": "60c72b1f9b1e4f1e5f4e4f28",
  "name": "John Doe",
  "phone": "+1234567890",
  "email": "johndoe@example.com",
  "date_of_birth": "1990-01-01",
  "gender": "male",
  "created_at": "2023-10-01T11:45:00Z"
}
```

## Chat Schemas

**ChatRequest**

**Purpose:** Handles input data for initiating or continuing a chat session.

| Field Name | Type | Required | Default | Description                  |
|------------|------|----------|---------|------------------------------|
| user_id    | str  | Yes      | None    | ID of the user engaging in chat.         |
| session_id | str  | No       | None    | Session ID if resuming, else none for a new session. |
| message    | str  | Yes      | None    | Message content from user.  |

**Example JSON:**
```json
{
  "user_id": "user123",
  "session_id": "60c72b3d9b1e4f1e5f4e4f30",
  "message": "What should I do next?"
}
```

**ChatResponse**

**Purpose:** Provides output data in response to a chat interaction.

| Field Name | Type | Required | Default | Description                 |
|------------|------|----------|---------|-----------------------------|
| session_id | str  | Yes      | None    | ID of the session ongoing or initiated. |
| message    | str  | Yes      | None    | Response message to user.   |
| urgent     | bool | No       | False   | Indicates if immediate action needed. |

**Example JSON:**
```json
{
  "session_id": "60c72b3d9b1e4f1e5f4e4f30",
  "message": "Please consult a neurologist.",
  "urgent": true
}
```

## Recommendation Schemas

**RecommendationResponse**

**Purpose:** Provides structured recommendation feedback from the system to the user.

| Field Name          | Type                                            | Required | Default | Description                           |
|---------------------|-------------------------------------------------|----------|---------|---------------------------------------|
| session_id          | str                                             | Yes      | None    | ID of the user session.               |
| urgency_level       | Literal["low", "moderate", "high", "emergency"] | Yes      | None    | Urgency level of the recommendation.  |
| next_step           | Literal["monitor", "teleconsult", "home_visit", "specialist", "emergency"] | Yes | None | Next suggested action for the user. |
| suggested_specialty | str                                             | No       | None    | Suggested medical specialty, if any. |
| patient_message     | str                                             | Yes      | None    | Message to be conveyed to the patient.|
| reasoning           | str                                             | Yes      | None    | Explanation of the recommendation.    |

**Example JSON:**
```json
{
  "session_id": "60c72b3d9b1e4f1e5f4e4f30",
  "urgency_level": "high",
  "next_step": "specialist",
  "suggested_specialty": "Neurology",
  "patient_message": "We recommend seeing a neurologist at your earliest convenience.",
  "reasoning": "Symptoms are consistent with neurological concerns and need further evaluation."
}
```

## Report Schemas

**ReportResponse**

**Purpose:** Conveys diagnostic findings and explanations back to the healthcare provider or patient.

| Field Name | Type  | Required | Default | Description                      |
|------------|-------|----------|---------|----------------------------------|
| session_id | str   | Yes      | None    | ID of the user session tied to the report. |
| findings   | dict  | Yes      | None    | Details and observations from the report. |
| explanation| str   | Yes      | None    | Narrated explanation of findings. |

**Example JSON:**
```json
{
  "session_id": "60c72b3d9b1e4f1e5f4e4f30",
  "findings": {"details": "All test results are normal."},
  "explanation": "The tests suggest no acute issues, but follow-up if symptoms persist."
}
```

## Recommender Engine

**SpecialistPathwayItem**

**Purpose:** Details individual pathways involving a specialist advice or intervention.

| Field Name | Type   | Required | Default | Description                           |
|------------|--------|----------|---------|---------------------------------------|
| specialist | str    | Yes      | None    | Name of the specialist recommended.   |
| reason     | str    | Yes      | None    | Reason for recommending the specialist.|

**Example JSON:**
```json
{
  "specialist": "Cardiologist",
  "reason": "Presence of chest pain suggests potential cardiac issues."
}
```

**RecommendationResult**

**Purpose:** Summarizes the final recommendation and provides a comprehensive care pathway.

| Field Name                     | Type        | Required | Default | Description                                      |
|--------------------------------|-------------|----------|---------|--------------------------------------------------|
| recommended_specialist         | str         | Yes      | None    | Specialist recommended for further consultation. |
| primary_recommendation_summary | str         | Yes      | None    | Summary of the key recommendation conclusion.    |
| symptom_explanation            | str         | Yes      | None    | Detailed explanation related to symptoms.        |
| specialist_pathway             | list[SpecialistPathwayItem] | Yes    | None | Pathway detailing specialist interventions needed.|
| red_flags                      | list[str]   | Yes      | None    | List of significant warning signs noted.         |
| urgency_level                  | Literal["low", "moderate", "high", "emergency"] | Yes | None | Evaluated urgency level associated with the case.|
| next_step                      | Literal["monitor", "teleconsult", "home_visit", "specialist", "emergency"] | Yes | None | Advised next step actions following assessment. |
| disclaimer                     | str         | Yes      | None    | Legal disclaimer or additional guidance.         |

**Example JSON:**
```json
{
  "recommended_specialist": "Endocrinologist",
  "primary_recommendation_summary": "Consider controlling the sugar levels more strictly.",
  "symptom_explanation": "The symptoms could indicate an onset of diabetes.",
  "specialist_pathway": [{"specialist": "Endocrinologist", "reason": "Sugar levels are borderline high, specialist consultation advisable."}],
  "red_flags": ["High glucose levels"],
  "urgency_level": "moderate",
  "next_step": "teleconsult",
  "disclaimer": "Consultations should be personalized per patient's condition and history."
}
```

## Model Relationships

In this system, the **Session** model acts as a central entity, linking user interactions through the **Message** model and bridging them with clinical evaluations encapsulated in the **ClinicalState**, **Report**, **ReportFinding**, and **Recommendation** models. Each session belongs to a **User**, establishing a connection between a single user's identification data and their ongoing healthcare interactions. Recommendations generated or updated throughout the session feed into consultation pathways, all documented within user sessions, reports, and findings.

Additionally, schemas such as **ChatRequest** and **RecommendationResponse** serve to facilitate input/output operations in chat and recommendation functionalities, ensuring seamless communication and data flow within the application framework. These schemas help in structuring user inputs and system outputs in a consistent and validated manner.