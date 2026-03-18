import os

# Define project structure
structure = {
        "services": {
            "classifier": {
                "agent.py": ""
            },
            "retriever": {
                "rag.py": "",
                "load_data.py": ""
            },
            "responder": {
                "agent.py": ""
            }
        },
        "orchestrator": {},
        "api": {},
        "ui": {},
        "evaluation": {
            "evaluator.py": "",
            "metrics.py": "",
            "dataset.json": ""
        },
        "monitoring": {
            "logger.py": "",
            "analytics.py": "",
            "storage.json": ""
        },
        "shared": {},
        "requirements.txt": ""
}


def create_structure(base_path, structure_dict):
    for name, content in structure_dict.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w") as f:
                f.write(content)

if __name__ == "__main__":
    base_dir = os.getcwd()
    create_structure(base_dir, structure)
    print("✅ Project scaffold created successfully!")