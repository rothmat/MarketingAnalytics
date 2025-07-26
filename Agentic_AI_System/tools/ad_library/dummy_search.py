from typing import List, Dict
import os


def search_ads(query: str, region: str, platform: str, num_ads: int, timeframe: str) -> List[Dict]:
    """Return dummy ads for the demo application."""
    sample_images = [
        "1174849481039965_2.jpg",
        "1320229502575547_2.jpg",
        "1361467541792536_2.jpg",
        "8156426677815477_2.jpg",
        "8156426677815477_3.jpg",
        "8156426677815477_7.jpg",
    ]

    ads = []
    for idx, img in enumerate(sample_images[:num_ads]):
        ads.append(
            {
                "id": f"dummy_{idx}",
                "platform": "Meta" if idx % 2 == 0 else "Google",
                "image_path": os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", img)),
                "snapshot_url": f"https://example.com/snapshot/{idx}",
                "api_data": {
                    "query": query,
                    "region": region,
                    "timeframe": timeframe,
                },
            }
        )
    return ads

