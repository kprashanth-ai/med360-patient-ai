> Auto-generated on 2026-04-21 17:10 by `scripts/update_docs.py`. Do not edit manually.

# Data Models

This document describes the data models used across different modules of an application, highlighting their purposes, fields, and relationships. The models are used to structure data that might be stored in JSON format files or exchanged via APIs.

## SpecialistPathwayItem

### Purpose
Represents an item in a pathway, including a specialist and the reason for their recommendation.

### Fields
| Field Name | Type   | Required | Default | Description                                  |
|------------|--------|----------|---------|----------------------------------------------|
| specialist | str    | Yes      |         | Name of the specialist.                      |
| reason     | str    | Yes      |         | Justification for recommending the specialist.|

### Example JSON Instance
```json
{
  "specialist": "Cardiologist",
  "reason": "Abnormal ECG findings"
}
```

## RecommendationResult

### Purpose
Stores the result of a recommendation process, providing information on recommended specialists, urgency, and next steps.

### Fields
| Field Name                      | Type    | Required | Default | Description                                                                                |
|---------------------------------|---------|----------|---------|--------------------------------------------------------------------------------------------|
| recommended_specialist          | str     | Yes      |         | Specialist suggested after the recommendation process.                                     |
| primary_recommendation_summary  | str     | Yes      |         | Overview of the primary recommendation.                                                    |
| symptom_explanation             | str     | Yes      |         | Explanation of symptoms leading to the recommendation.                                     |
| specialist_pathway              | list    | Yes      |         | List of `SpecialistPathwayItem` objects detailing the recommended pathway.                 |
| red_flags                       | list    | Yes      |         | Significant warnings or red flags identified.                                              |
| urgency_level                   | Literal | Yes      |         | Level of urgency: "low", "moderate", "high", or "emergency".                               |
| next_step                       | Literal | Yes      |         | Suggested next action: "monitor", "teleconsult", "home_visit", "specialist", or "emergency". |
| disclaimer                      | str     | Yes      |         | Disclaimer associated with the recommendation.                                             |

### Example JSON Instance
```json
{
  "recommended_specialist": "Dermatologist",
  "primary_recommendation_summary": "Recommend specialist skin evaluation",
  "symptom_explanation": "Persistent rash and itching",
  "specialist_pathway": [{"specialist": "Dermatologist", "reason": "Rash unresponsive to initial therapy"}],
  "red_flags": ["History of melanoma"],
  "urgency_level": "moderate",
  "next_step": "teleconsult",
  "disclaimer": "Consultation does not replace professional medical advice."
}
```

## LabValue

### Purpose
Describes a laboratory value, its measurement, and analysis.

### Fields
| Field Name      | Type    | Required | Default | Description                                        |
|-----------------|---------|----------|---------|----------------------------------------------------|
| name            | str     | Yes      |         | Name of the lab test or parameter.                 |
| value           | str     | Yes      |         | Measured value of the lab test.                    |
| unit            | str     | No       | None    | Unit of measurement.                               |
| reference_range | str     | No       | None    | Normal range for comparison.                       |
| status          | Literal | Yes      |         | Indicates if the value is "normal", "abnormal", or "borderline". |
| plain_meaning   | str     | Yes      |         | Simple explanation of the lab result.              |

### Example JSON Instance
```json
{
  "name": "Hemoglobin",
  "value": "13.5",
  "unit": "g/dL",
  "reference_range": "13.0-17.0",
  "status": "normal",
  "plain_meaning": "Normal hemoglobin level"
}
```

## ReportFindings

### Purpose
Encapsulates findings from a lab report, including summaries and recommended actions.

### Fields
| Field Name         | Type    | Required | Default | Description                                               |
|--------------------|---------|----------|---------|-----------------------------------------------------------|
| report_type        | str     | Yes      |         | Type of the lab report.                                   |
| test_date          | str     | No       | None    | Date when the test was conducted.                         |
| abnormal_values    | list    | Yes      |         | List of `LabValue` objects that are abnormal.             |
| normal_values      | list    | Yes      |         | List of `LabValue` objects that are normal.               |
| notable_markers    | list    | Yes      |         | Specific markers of interest in the report.               |
| overall_summary    | str     | Yes      |         | Summary of the report findings.                           |
| plain_explanation  | str     | Yes      |         | Simplified explanation of the report results.             |
| recommended_action | str     | Yes      |         | Actions recommended based on the report findings.         |
| urgency            | Literal | Yes      |         | Urgency of action: "routine", "soon", or "urgent".        |

### Example JSON Instance
```json
{
  "report_type": "Complete Blood Count",
  "test_date": "2023-08-15",
  "abnormal_values": [{"name": "WBC", "value": "11.0", "unit": "x10^9/L", "reference_range": "4.0-10.5", "status": "abnormal", "plain_meaning": "Elevated white blood cells"}],
  "normal_values": [],
  "notable_markers": ["WBC"],
  "overall_summary": "Leukocytosis indicated by elevated WBC",
  "plain_explanation": "High white cell count may suggest an infection",
  "recommended_action": "Follow up with additional tests to investigate cause of leukocytosis",
  "urgency": "soon"
}
```

## CollectedPatientData

### Purpose
Captures demographic and symptom information from a patient.

### Fields
| Field Name   | Type    | Required | Default | Description                                       |
|--------------|---------|----------|---------|---------------------------------------------------|
| age          | int     | Yes      |         | Age of the patient.                               |
| gender       | Literal | Yes      |         | Gender of the patient: "male", "female", or "other". |
| severity     | Literal | Yes      |         | Severity of the condition: "low", "medium", or "high". |
| duration_days| int     | Yes      |         | Duration of the symptoms in days.                  |
| symptoms     | str     | Yes      |         | Description of the symptoms.                       |

### Example JSON Instance
```json
{
  "age": 35,
  "gender": "female",
  "severity": "medium",
  "duration_days": 7,
  "symptoms": "Persistent headache and slight fever"
}
```

## ChatTurn

### Purpose
Details a single turn in a conversation with a chatbot, including suggestions and patient data.

### Fields
| Field Name           | Type    | Required | Default  | Description                                                                          |
|----------------------|---------|----------|----------|--------------------------------------------------------------------------------------|
| message              | str     | Yes      |          | Content of the chat message.                                                         |
| urgency_level        | Literal | No       | "none"   | Assessed urgency of the chat content: "none", "low", "moderate", "high", or "emergency". |
| suggested_next_step  | Literal | No       | "none"   | Recommended action following the chat: "none", "monitor", "teleconsult", "home_visit", "specialist", or "emergency". |
| escalation_note      | str     | No       | None     | Additional notes if escalation is needed.                                            |
| ready_to_recommend   | bool    | No       | False    | Indicates if a recommendation can be made based on this chat turn.                    |
| patient_data         | object  | No       | None     | `CollectedPatientData` object detailing patient demographics and symptoms if applicable. |

### Example JSON Instance
```json
{
  "message": "I have a slight fever and a headache for 5 days",
  "urgency_level": "moderate",
  "suggested_next_step": "teleconsult",
  "escalation_note": "Consider following up with a general practitioner",
  "ready_to_recommend": true,
  "patient_data": {
    "age": 28,
    "gender": "male",
    "severity": "medium",
    "duration_days": 5,
    "symptoms": "Fever, headache"
  }
}
```

## Relationships Between Models

- **RecommendationResult** relies on **SpecialistPathwayItem** objects to build the pathway to a recommended specialist.
- **ReportFindings** includes lists of **LabValue** objects to determine and explain report outcomes.
- **ChatTurn** optionally holds **CollectedPatientData** to store patient input and context for automated conversations. This model also utilizes urgency levels and suggested actions which can overlap with similar fields in **RecommendationResult** for consistency in patient care paths.