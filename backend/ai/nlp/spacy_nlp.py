import re
from typing import Optional

def extract_email(text: str) -> Optional[str]:
    # Basic email regex
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    return match.group(0) if match else None

def extract_phone(text: str) -> Optional[str]:
    # Basic phone regex
    match = re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
    return match.group(0) if match else None

def extract_entities(text: str) -> dict:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        return {"name": None, "location": None}
    
    doc = nlp(text)
    person_names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    locations = [ent.text for ent in doc.ents if ent.label_ in ("GPE", "LOC")]
    
    return {
        "name": person_names[0] if person_names else None,
        "location": locations[0] if locations else None
    }
