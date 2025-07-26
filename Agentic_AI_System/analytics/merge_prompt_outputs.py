import os
import json
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI
from core.logger import log

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MERGE_PROMPT_PATH = os.path.join("prompts", "merge_prompt.txt")


def _load_merge_prompt() -> str:
    try:
        with open(MERGE_PROMPT_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        log.error(f"Merge-Prompt nicht gefunden: {MERGE_PROMPT_PATH}")
        return ""


def merge_prompt_outputs(outputs: List[Dict]) -> Dict:
    """Combine multiple prompt outputs using an LLM."""
    merge_prompt = _load_merge_prompt()
    if not merge_prompt:
        return {"error": "merge prompt missing"}

    try:
        messages = [
            {"role": "system", "content": merge_prompt},
            {"role": "user", "content": json.dumps(outputs, ensure_ascii=False)},
        ]
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.2,
            max_tokens=1500,
        )
        result = response.choices[0].message.content.strip()
        if result.startswith("```json"):
            result = result.removeprefix("```json").removesuffix("```").strip()
        elif result.startswith("```"):
            result = result.removeprefix("```").removesuffix("```").strip()
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            log.warning("Konsolidiertes Ergebnis war kein valides JSON")
            return {"raw_output": result}
    except Exception as e:
        log.error(f"Fehler bei der Ergebnis-Konsolidierung: {e}")
        return {"error": str(e)}
