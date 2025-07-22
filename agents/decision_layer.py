# agents/decision_layer.py
from tools.text.dummy_tool import DummyTool
from tools.vision.gpt4o_vision_tool import GPT4oVisionTool
from core.logger import log
from scripts.main_image_analyzer_gpt4o import run_analysis as run_gpt4o_script

def tool_selection():
    tools = {
        "1": ("Dummy Tool", DummyTool()),
        "2": ("GPT-4o Vision Tool (direkt)", "gpt4o_script"),
        # Weitere Tools hier ergänzen …
    }

    print("\n🧰 Verfügbare Tools:")
    for key, (label, _) in tools.items():
        print(f"{key}. {label}")

    choice = input("🔢 Bitte wähle ein Tool (Zahl eingeben): ").strip()

    if choice not in tools:
        log.error("❌ Ungültige Auswahl.")
        return None

    label, selected = tools[choice]
    log.info(f"✅ Gewähltes Tool: {label}")
    return selected
