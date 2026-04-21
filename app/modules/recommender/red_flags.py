RED_FLAG_KEYWORDS = [
    "chest pain",
    "difficulty breathing",
    "shortness of breath",
    "severe headache",
    "sudden confusion",
    "loss of consciousness",
    "coughing blood",
    "vomiting blood",
    "stroke",
    "heart attack",
    "paralysis",
    "seizure",
    "severe allergic reaction",
    "anaphylaxis",
    "suicidal",
]


async def detect_red_flags(clinical_state: dict) -> bool:
    flags = clinical_state.get("red_flags", [])
    if flags:
        return True

    chief_complaint = (clinical_state.get("chief_complaint") or "").lower()
    symptoms = " ".join(clinical_state.get("symptoms") or []).lower()
    combined = chief_complaint + " " + symptoms

    return any(keyword in combined for keyword in RED_FLAG_KEYWORDS)
