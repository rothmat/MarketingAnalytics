import os
from datetime import date
from tools.ad_library.ad_search import search_ads
from agents.multi_prompt_vision_agent import MultiPromptVisionAgent
from tools.utils.screenshot import capture as capture_screenshot
from core.logger import log


def main() -> None:
    query = input("Suchbegriffe: ").strip()
    region = input("Region: ").strip()
    platform = input("Plattform (Meta/Google/Beide): ").strip() or "Beide"
    num_ads = int(input("Anzahl Ads: ") or "3")
    start_date = input("Startdatum (YYYY-MM-DD): ") or str(date.today())
    end_date = input("Enddatum (YYYY-MM-DD): ") or str(date.today())

    timeframe = f"{start_date} - {end_date}"
    ads = search_ads(query, region, platform, num_ads, timeframe)
    agent = MultiPromptVisionAgent()

    snap_dir = os.path.join("outputs", "snapshots")
    os.makedirs(snap_dir, exist_ok=True)

    for ad in ads:
        log.info(f"Analysiere Ad {ad['id']} von {ad['platform']}")
        screenshot_path = os.path.join(snap_dir, f"{ad['id']}.png")
        analyze_path = ad.get("image_path")
        if ad.get("snapshot_url"):
            try:
                capture_screenshot(ad['snapshot_url'], screenshot_path)
                analyze_path = screenshot_path
            except Exception as e:
                log.warning(f"Screenshot fehlgeschlagen: {e}")

        result = agent.analyze(analyze_path)
        log.success(f"Fertig: {result['image_url']}")


if __name__ == "__main__":
    main()
