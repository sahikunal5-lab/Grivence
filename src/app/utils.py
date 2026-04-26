import re

# -------- PREPROCESS --------
def preprocess(text):
    text = text.lower()

    # remove special characters
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)

    # remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text


# -------- SENTIMENT --------
def get_sentiment(text):
    text = text.lower()

    negative_words = [
        "not", "bad", "angry", "frustrated", "delay",
        "urgent", "issue", "problem", "complaint",
        "worst", "poor", "dirty", "danger", "damage",
        "leakage", "overflow", "broken", "fail"
    ]

    positive_words = [
        "good", "resolved", "fixed", "clean",
        "working", "satisfied"
    ]

    if any(w in text for w in negative_words):
        return "Negative"
    elif any(w in text for w in positive_words):
        return "Positive"
    else:
        return "Neutral"


# -------- PRIORITY (HYBRID AI) --------
def get_priority(text, sentiment):
    text = text.lower()

    high_priority_words = [
        "urgent", "immediately", "asap", "danger",
        "fire", "electric shock", "accident",
        "emergency", "serious", "critical"
    ]

    medium_priority_words = [
        "problem", "issue", "delay", "not working",
        "complaint", "bad"
    ]

    # RULE 1: Critical keywords → HIGH
    if any(w in text for w in high_priority_words):
        return "High"

    # RULE 2: Negative sentiment → HIGH (probabilistic feel)
    if sentiment == "Negative":
        return "High"

    # RULE 3: Medium words → NORMAL
    if any(w in text for w in medium_priority_words):
        return "Normal"

    return "Normal"


# -------- ALERT SYSTEM --------
def check_alert(priority):
    if priority == "High":
        return "🚨 Escalated to Authority"
    return "Normal"