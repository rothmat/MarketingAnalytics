import os
import json
from core.logger import log
from openai import OpenAI
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

class GPT4oVisionTool:
    def __init__(self):
        self.name = "gpt4o_vision_tool"
        self.description = (
            "Analysiert ein Bild anhand eines strukturierten Prompts zu Online-Werbung "
            "und liefert eine vollständige JSON-Ausgabe mit visuellen, textuellen und semantischen Elementen."
        )

        prompt_relative_path = os.path.join("prompts", "vision_prompt_v1.txt")
        prompt_path = os.path.abspath(prompt_relative_path)

        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                self.prompt = f.read()
        except FileNotFoundError:
            log.error(f"❌ vision_prompt_v1.txt nicht gefunden unter: {prompt_path}")
            self.prompt = None

    def analyze_image(self, image_url: str) -> dict:
        """
        Normale Methode für direkten Aufruf (ohne Agent).
        """
        log.info(f"📷 Starte Bildanalyse für: {image_url}")

        if not self.prompt:
            return {"error": "Prompt fehlt – konnte nicht geladen werden."}

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": [
                        {"type": "text", "text": self.prompt},
                        {"type": "image_url", "image_url": {"url": image_url, "detail": "high"}}
                    ]}
                ],
                temperature=0.2,
                max_tokens=1500
            )

            result = response.choices[0].message.content.strip()

            if result.startswith("```json"):
                result = result.removeprefix("```json").removesuffix("```").strip()
            elif result.startswith("```"):
                result = result.removeprefix("```").removesuffix("```").strip()

            try:
                parsed = json.loads(result)
                log.success("✅ GPT-4o Analyse erfolgreich und JSON valide.")
                return parsed
            except json.JSONDecodeError:
                log.warning("⚠️ Rückgabe war kein valides JSON. Rohtext wird zurückgegeben.")
                return {"raw_output": result}

        except Exception as e:
            log.error(f"❌ Fehler bei GPT-4o Analyse: {e}")
            return {"error": str(e)}

    @tool("gpt4o_vision_tool")
    def run(self, image_url: str) -> dict:
        """
        Agent-kompatible Schnittstelle – ruft intern analyze_image auf.
        """
        return self.analyze_image(image_url)
