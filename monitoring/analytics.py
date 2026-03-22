import json

def get_stats():
    with open("monitoring/storage.json") as f:
        logs = json.load(f)

    total = len(logs)

    avg_latency = sum(l["latency"] for l in logs) / total if total else 0

    intents = {}
    for l in logs:
        intent = l.get("intent", "unknown")
        intents[intent] = intents.get(intent, 0) + 1

    return {
        "total_requests": total,
        "avg_latency": avg_latency,
        "intent_distribution": intents
    }