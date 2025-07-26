import os
from typing import List, Dict
import requests
from datetime import datetime
from core.logger import log
from .search_utils import expand_search_terms

GOOGLE_API_URL = "https://politicaladsreporting.googleapis.com/v1/ads:search"


def _parse_timeframe(timeframe: str) -> Dict[str, str]:
    params = {}
    if timeframe and "-" in timeframe:
        start, end = [t.strip() for t in timeframe.split("-")]
        try:
            datetime.fromisoformat(start)
            datetime.fromisoformat(end)
            params["startDate"] = start
            params["endDate"] = end
        except ValueError:
            log.warning("Ungültiger Datumsbereich, ignoriere timeframe")
    return params


def search_google_ads(query: str, region: str, num_ads: int, timeframe: str) -> List[Dict]:
    """Search Google Ads Transparency API for political ads."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not set")

    results: List[Dict] = []

    for term in expand_search_terms(query):
        params = {
            "query": term,
            "regionCode": region,
            "pageSize": num_ads,
            "key": api_key,
        }
        params.update(_parse_timeframe(timeframe))
        try:
            resp = requests.get(GOOGLE_API_URL, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json().get("ads", [])
        except Exception as e:
            log.error(f"Google API request failed for term '{term}': {e}")
            continue

        for ad in data:
            results.append(
                {
                    "id": ad.get("adId") or ad.get("id"),
                    "platform": "Google",
                    "image_path": "",
                    "snapshot_url": ad.get("adSnapshotUrl"),
                    "api_data": ad,
                }
            )
            if len(results) >= num_ads:
                return results[:num_ads]
    return results[:num_ads]
