import json
from typing import List, Dict

from core.logger import log
from core.output_manager import save_output
from tools.vision.gpt4o_vision_tool import GPT4oVisionTool
from analytics.merge_prompt_outputs import merge_prompt_outputs


class MultiPromptVisionAgent:
    """Führt eine Bildanalyse mit drei unterschiedlichen Prompts durch
    und fasst die Ergebnisse zu einem Dictionary zusammen."""

    def __init__(self) -> None:
        # Drei Varianten des gleichen Tools mit unterschiedlichen Prompts
        self.tools = [
            GPT4oVisionTool("vision_prompt_v1.txt"),
            GPT4oVisionTool("vision_prompt_v2.txt"),
            GPT4oVisionTool("vision_prompt_v3.txt"),
        ]

    def analyze(self, image_url: str) -> Dict:
        log.info(f"🔎 Starte Multi-Prompt Analyse für {image_url}")
        results = []
        for tool in self.tools:
            result = tool.analyze_image(image_url)
            results.append(result)

        merged = merge_prompt_outputs(results)

        aggregated = {
            "image_url": image_url,
            "prompt_outputs": results,
            "merged_output": merged,
        }
        # Speichern zur Nachverfolgung
        save_output(aggregated)
        return aggregated

    def analyze_batch(self, urls: List[str]) -> List[Dict]:
        batch_results = []
        for url in urls:
            batch_results.append(self.analyze(url))
        return batch_results
