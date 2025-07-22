import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from core.logger import log

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def analyze_image_with_prompt(image_url: str, prompt_path: str = "prompts/vision_prompt_v1.txt") -> dict:
    """
    Führt eine Bildanalyse mit GPT-4o durch, basierend auf einem benutzerdefinierten Prompt.
    """
    log.info(f"📷 Analyse wird gestartet für Bild: {image_url}")

    # Prompt laden
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt = f.read()
    except FileNotFoundError:
        log.error(f"❌ Promptdatei nicht gefunden unter: {prompt_path}")
        return {"error": f"Promptdatei fehlt: {prompt_path}"}

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url, "detail": "high"}}
                    ]
                }
            ],
            temperature=0.2,
            max_tokens=1500
        )

        raw = response.choices[0].message.content.strip()

        if raw.startswith("```json"):
            raw = raw.removeprefix("```json").removesuffix("```").strip()
        elif raw.startswith("```"):
            raw = raw.removeprefix("```").removesuffix("```").strip()

        try:
            parsed = json.loads(raw)
            log.success("✅ GPT-4o Analyse erfolgreich & JSON valide.")
            return parsed
        except json.JSONDecodeError:
            log.warning("⚠️ JSON nicht valide – Rückgabe als Rohtext.")
            return {"raw_output": raw}

    except Exception as e:
        log.error(f"❌ Fehler bei GPT-4o Analyse: {e}")
        return {"error": str(e)}
