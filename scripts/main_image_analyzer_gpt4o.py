from tools.vision.gpt4o_vision_tool import GPT4oVisionTool
from core.output_manager import save_output
from core.logger import log

def run_analysis():
    image_url = input("📸 Bitte Bild-URL angeben: ").strip()
    tool = GPT4oVisionTool()
    result = tool.analyze_image(image_url)  # ✅ direkter Methodenaufruf

    output_data = {
        "image_url": image_url,
        "output": result
    }

    save_output(output_data)
    log.success("✅ Analyse abgeschlossen und gespeichert.")

# Optional sofort ausführbar machen
if __name__ == "__main__":
    run_analysis()
