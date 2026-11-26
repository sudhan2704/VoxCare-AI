
import re


def analyze_sentiment(transcript: str) -> str:
    text = transcript.lower()

    positive_words = [
        "thank you", "thanks", "helpful",
        "satisfied", "resolved", "appreciate"
    ]

    negative_words = [
        "angry", "upset", "frustrated",
        "problem", "complaint", "unhappy",
        "delay", "not satisfied"
    ]

    positive_count = sum(
        word in text for word in positive_words
    )

    negative_count = sum(
        word in text for word in negative_words
    )

    if positive_count > negative_count:
        return "positive"

    if negative_count > positive_count:
        return "negative"

    return "neutral"


def detect_intent(transcript: str) -> str:
    text = transcript.lower()

    intent_keywords = {
        "appointment_status": [
            "appointment", "booking", "schedule"
        ],
        "billing_query": [
            "bill", "payment", "invoice", "charge"
        ],
        "information_request": [
            "information", "details", "explain"
        ],
        "complaint": [
            "complaint", "unhappy", "problem"
        ],
        "general_support": [
            "help", "support", "assistance"
        ]
    }

    for intent, keywords in intent_keywords.items():
        if any(word in text for word in keywords):
            return intent

    return "unknown"


def generate_summary(transcript: str) -> str:
    cleaned_text = re.sub(
        r"\s+", " ", transcript
    ).strip()

    if not cleaned_text:
        return "No transcript available."

    sentences = re.split(
        r"(?<=[.!?])\s+", cleaned_text
    )

    return " ".join(sentences[:2])


def analyze_call(transcript: str) -> dict:
    if not transcript or not transcript.strip():
        raise ValueError("Transcript cannot be empty.")

    sentiment = analyze_sentiment(transcript)
    intent = detect_intent(transcript)

    return {
        "analysis_method": "rule_based",
        "summary": generate_summary(transcript),
        "customer_intent": intent,
        "sentiment": sentiment,
        "follow_up_required": (
            sentiment == "negative"
            or intent == "unknown"
        )
    }
