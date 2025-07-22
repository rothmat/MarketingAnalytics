import os

project_structure = {
    "agents": [
        "decision_layer.py",
        "evaluation_agent.py",
        "vision_agent.py",
        "nlp_agent.py",
        "orchestrator.py"
    ],
    "tools/vision": [
        "yolo_tool.py",
        "openai_tool.py"
    ],
    "tools/text": [
        "classifier_tool.py",
        "sentiment_tool.py",
        "prompt_optimizer_tool.py"
    ],
    "tools/reporting": [
        "export_tools.py",
        "report_builder.py"
    ],
    "analytics": [
        "aggregate_kpis.py",
        "csv_report.py",
        "evaluation_metrics.py"
    ],
    "core": [
        "config.py",
        "logger.py",
        "utils.py"
    ],
    "memory/chroma": [],
    "memory/logs": [],
    "interface": [
        "gui.py"
    ],
    "input": [
        "images_to_analyze.json"
    ],
    "prompts": [
        "json_analysis.txt"
    ],
    "outputs": [],
    "tests": [],
}

root_files = ["main_agent.py", "requirements.txt", ".env", "setup_venv.sh"]

# Erstellen der Ordner und Dateien
for folder, files in project_structure.items():
    os.makedirs(folder, exist_ok=True)
    for file in files:
        path = os.path.join(folder, file)
        with open(path, "w", encoding="utf-8") as f:
            f.write("")  # Leere Datei anlegen

# Root-Dateien anlegen
for file in root_files:
    with open(file, "w", encoding="utf-8") as f:
        f.write("")

print("✅ Projektstruktur erfolgreich erstellt.")
