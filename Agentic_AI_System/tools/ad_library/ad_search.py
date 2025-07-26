import os
from typing import List, Dict
from core.logger import log
from .dummy_search import search_ads as dummy_search
from .meta_api import search_meta_ads
from .google_api import search_google_ads


def search_ads(query: str, region: str, platform: str, num_ads: int, timeframe: str) -> List[Dict]:
    """Search ads via API if available, otherwise return dummy data."""
    use_api = os.getenv("USE_AD_LIBRARY_API", "0") == "1"
    if not use_api:
        return dummy_search(query, region, platform, num_ads, timeframe)

    ads: List[Dict] = []
    try:
        if platform == "Meta":
            ads = search_meta_ads(query, region, num_ads, timeframe)
        elif platform == "Google":
            ads = search_google_ads(query, region, num_ads, timeframe)
        else:
            half = num_ads // 2
            ads = search_meta_ads(query, region, half, timeframe)
            ads += search_google_ads(query, region, num_ads - len(ads), timeframe)
    except NotImplementedError as e:
        log.warning(f"API search not implemented: {e}. Using dummy data instead.")
        ads = dummy_search(query, region, platform, num_ads, timeframe)
    except Exception as e:
        log.error(f"Ad search failed: {e}")
        ads = dummy_search(query, region, platform, num_ads, timeframe)
    return ads
