from datetime import datetime

def format_confidence(confidence: float) -> str:
    return f"{confidence * 100:.2f}%"

def format_timestamp(dt: datetime | None = None) -> str:
    dt = dt or datetime.now()
    return dt.strftime("%d %b %Y, %I:%M %p")

def get_top_prediction(all_probs: dict) -> tuple[str, float]:
    top_class = max(all_probs, key=all_probs.get)
    return top_class, all_probs[top_class]