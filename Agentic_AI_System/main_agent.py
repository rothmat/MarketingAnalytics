from langchain.agents import initialize_agent, Tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from core.logger import log
from core.output_manager import save_output
from tools.text.dummy_tool import DummyTool
from tools.vision.gpt4o_vision_tool import GPT4oVisionTool
from scripts.main_image_analyzer_gpt4o import run_analysis as run_gpt4o_script  # ✅ CLI-external tool
import os

# 🔐 .env laden
load_dotenv()

log.info("🔁 Agent gestartet.")

# 🔧 Tool-Auswahl
print("\n📌 Welches Tool möchtest du verwenden?")
print("1 - Dummy Tool")
print("2 - GPT-4o Vision Tool (Agent)")
print("3 - GPT-4o Vision Tool (direktes Skript ohne Agent)")

choice = input("🔢 Auswahl (1/2/3): ").strip()

# 🚀 Sonderfall: Externes Skript direkt ausführen
if choice == "3":
    run_gpt4o_script()  # ruft das vision-analyse-skript direkt auf
    exit()

# 🧠 LLM Setup
llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-4o"
)

# 🔌 Tools registrieren (je nach Auswahl)
tools = []

if choice == "1":
    dummy = DummyTool()
    tools.append(Tool(name=dummy.name, func=dummy.run, description=dummy.description))
    log.debug(f"🛠️ Tool geladen: {dummy.name}")

elif choice == "2":
    vision = GPT4oVisionTool()
    tools.append(Tool(name=vision.name, func=vision.run, description=vision.description))
    log.debug(f"🛠️ Tool geladen: {vision.name}")

else:
    log.error("❌ Ungültige Auswahl. Beende.")
    exit()

# 🤖 Agent Setup
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True
)

# 📤 Test-Query (diese kann später ersetzt werden durch dynamische Eingaben)
if __name__ == "__main__":
    query = "Analysiere dieses Bild mit einem Tool: https://raw.githubusercontent.com/rothmat/MarketingAnalytics/1932b066b56f2919b318223ae47d9ea6df481e4f/1036160865297465.png"
    log.info(f"📝 Eingabe: {query}")

    try:
        result = agent.invoke(query)
        output = result.get("output") if isinstance(result, dict) else result
        log.info(f"📤 Ausgabe: {output}")

        save_output({
            "input": query,
            "output": output
        })

        log.success("✅ Agentenlauf erfolgreich abgeschlossen.")

    except Exception as e:
        log.error(f"❌ Fehler während des Agentenlaufs: {e}")
