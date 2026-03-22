from typing import Literal

def classify_query(query: str) -> Literal["billing", "technical", "general"]:
    query = query.lower()

    if any(word in query for word in ["refund", "payment", "bill"]):
        return "billing"
    elif any(word in query for word in ["error", "bug", "issue", "not working"]):
        return "technical"
    else:
        return "general"