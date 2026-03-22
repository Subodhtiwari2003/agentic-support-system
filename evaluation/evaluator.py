import json
from orchestrator.graph import graph
from evaluation.metrics import evaluate_response

def run_evaluation():
    with open("evaluation/dataset.json") as f:
        dataset = json.load(f)

    results = []

    for item in dataset:
        result = graph.invoke({"query": item["query"]})

        metrics = evaluate_response(
            result["response"],
            item["expected_answer"]
        )

        results.append({
            "query": item["query"],
            "response": result["response"],
            "metrics": metrics
        })

    return results


if __name__ == "__main__":
    output = run_evaluation()
    print(output)