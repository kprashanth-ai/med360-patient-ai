---
tags: [models, reference, auto-generated]
updated: "2026-04-21 17:19"
---

> Auto-generated on 2026-04-21 17:19 by `scripts/update_docs.py`. Do not edit manually.

# Data Models

This document provides an overview of the data models used across different modules of the application. The models are designed for JSON file storage, ensuring that the data can be easily serialized and deserialized.

## SpecialistPathwayItem Model
**Purpose:** Represents a pathway item for directing to a specialist with an associated reason.

| Field Name | Type | Required | Default | Description |
|------------|------|----------|---------|-------------|
| specialist | str  | Yes      | N/A     | The specialist name or role. |
| reason     | str  | Yes      | N/A     | The reason for recommending this specialist. |

**Example JSON Instance:**
```json
{
    "specialist": "Cardiologist",
    "reason": "Heart palpitations"
}
```

## RecommendationResult Model
**Purpose:** Provides the result of a recommendation process, including specialists, pathway, and urgency.

| Field Name                       | Type                                                           | Required | Default | Description |
|----------------------------------|----------------------------------------------------------------|----------|---------|-------------|
| recommended_specialist           | str                                                            | Yes      | N/A     | Specialist recommended for consultation. |
| primary_recommendation_summary   | str                                                            | Yes      | N/A     | Summary of the primary recommendation. |
| symptom_explanation              | str                                                            | Yes      | N/A     | Explanation of symptoms leading to the recommendation. |
| specialist_pathway               | list[SpecialistPathwayItem]                                    | Yes      | N/A     | Pathway items detailing the recommended specialists. |
| red_flags                        | list[str]                                                      | Yes      | N/A     | List of red flags identified in the assessment. |
| urgency_level                    | Literal["low", "moderate", "high", "emergency"]               | Yes      | N/A     | Urgency of the situation. |
| next_step                        | Literal["monitor", "teleconsult", "home_visit", "specialist", "emergency"] | Yes      | N/A     | Suggested next action to take. |
| disclaimer                       | str                                                            | Yes      | N/A     | Disclaimer about the recommendation. |

**Example JSON Instance:**
```json
{
    "recommended_specialist": "Dermatologist",
    "primary_recommendation_summary": "Skin rash assessment",
    "symptom_explanation": "Redness and itching observed",
    "specialist_pathway": [
        {"specialist": "Dermatologist", "reason": "Persistent rash"}
    ],
    "red_flags": ["Unusual skin color change"],
    "urgency_level": "moderate",
    "next_step": "specialist",
    "disclaimer": "Consult a professional for detailed analysis."
}
```

## LabValue Model
**Purpose:** Represents a single lab value with its status and plain meaning.

| Field Name     | Type                                       | Required | Default | Description |
|----------------|--------------------------------------------|----------|---------|-------------|
| name           | str                                        | Yes      | N/A     | The lab test name. |
| value          | str                                        | Yes      | N/A     | The measured value. |
| unit           | str \| None                                | No       | None    | The unit of the measured value. |
| reference_range| str \| None                                | No       | None    | The standard reference range. |
| status         | Literal["normal", "abnormal", "borderline"]| Yes      | N/A     | Status of the lab value. |
| plain_meaning  | str                                        | Yes      | N/A     | Plain language explanation of the value. |

**Example JSON Instance:**
```json
{
    "name": "Hemoglobin",
    "value": "13.5",
    "unit": "g/dL",
    "reference_range": "13.0-17.0",
    "status": "normal",
    "plain_meaning": "Normal hemoglobin level."
}
```

## ReportFindings Model
**Purpose:** Contains comprehensive report findings, including lab result interpretations and recommended actions.

| Field Name         | Type                                       | Required | Default | Description |
|--------------------|--------------------------------------------|----------|---------|-------------|
| report_type        | str                                        | Yes      | N/A     | The type of medical report. |
| test_date          | str \| None                                | No       | None    | The date the test was conducted. |
| abnormal_values    | list[LabValue]                             | Yes      | N/A     | List of abnormal lab values. |
| normal_values      | list[LabValue]                             | Yes      | N/A     | List of normal lab values. |
| notable_markers    | list[str]                                  | Yes      | N/A     | Highlights markers of interest. |
| overall_summary    | str                                        | Yes      | N/A     | Summary of the findings. |
| plain_explanation  | str                                        | Yes      | N/A     | Plain explanation for users. |
| recommended_action | str                                        | Yes      | N/A     | Actions recommended based on findings. |
| urgency            | Literal["routine", "soon", "urgent"]       | Yes      | N/A     | Urgency level for follow-up. |

**Example JSON Instance:**
```json
{
    "report_type": "Blood Test",
    "test_date": "2023-10-01",
    "abnormal_values": [{"name": "Glucose", "value": "180", "unit": "mg/dL", "reference_range": "70-99", "status": "abnormal", "plain_meaning": "High glucose levels."}],
    "normal_values": [{"name": "Hemoglobin", "value": "14.2", "unit": "g/dL", "reference_range": "13.0-17.0", "status": "normal", "plain_meaning": "Normal hemoglobin level."}],
    "notable_markers": ["Glucose"],
    "overall_summary": "High blood sugar levels detected; other parameters normal.",
    "plain_explanation": "Your blood sugar is higher than normal.",
    "recommended_action": "Consult with your doctor about managing blood sugar levels.",
    "urgency": "soon"
}
```

## CollectedPatientData Model
**Purpose:** Stores collected data about a patient relevant to medical assessments.

| Field Name | Type                             | Required | Default | Description |
|------------|----------------------------------|----------|---------|-------------|
| age        | int                              | Yes      | N/A     | Patient's age in years. |
| gender     | Literal["male", "female", "other"] | Yes      | N/A     | Patient's gender. |
| severity   | Literal["low", "medium", "high"] | Yes      | N/A     | Severity level of the symptoms. |
| duration_days | int                            | Yes      | N/A     | Duration of symptoms in days. |
| symptoms   | str                              | Yes      | N/A     | Description of the symptoms. |

**Example JSON Instance:**
```json
{
    "age": 45,
    "gender": "male",
    "severity": "medium",
    "duration_days": 7,
    "symptoms": "Coughing and mild fever"
}
```

## ChatTurn Model
**Purpose:** Represents a single conversational turn in a chatbot interaction.

| Field Name          | Type                                                           | Required | Default | Description |
|---------------------|----------------------------------------------------------------|----------|---------|-------------|
| message             | str                                                            | Yes      | N/A     | The chat message content. |
| urgency_level       | Literal["none", "low", "moderate", "high", "emergency"]       | No       | "none"  | Urgency of any action to take, if needed. |
| suggested_next_step | Literal["none", "monitor", "teleconsult", "home_visit", "specialist", "emergency"] | No | "none" | Suggested next action, if any. |
| escalation_note     | str \| None                                                   | No       | None    | Note if the situation needs to be escalated. |
| ready_to_recommend  | bool                                                           | No       | False   | Whether the system is ready to make a recommendation based on collected data. |
| patient_data        | CollectedPatientData \| None                                  | No       | None    | Data collected about the patient during conversation. |

**Example JSON Instance:**
```json
{
    "message": "I have a headache for the last two days.",
    "urgency_level": "low",
    "suggested_next_step": "monitor",
    "escalation_note": null,
    "ready_to_recommend": true,
    "patient_data": {
        "age": 30,
        "gender": "female",
        "severity": "low",
        "duration_days": 2,
        "symptoms": "Headache"
    }
}
```

## Relationships Between Models

The models interrelate as follows:
- `RecommendationResult` includes multiple `SpecialistPathwayItem` instances to offer a comprehensive view of the referral pathway based on symptoms detected.
- `ReportFindings` aggregates several `LabValue` items to deliver a detailed analysis of lab work, noting abnormalities and their meanings.
- `ChatTurn` can collect patient data using `CollectedPatientData`, which encapsulates demographic and symptom information gathered during a chatbot interaction. This data can support decision-making processes in models like `RecommendationResult`, enabling personalized recommendations.