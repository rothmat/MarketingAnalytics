import os
from typing import List, Dict
import requests
from datetime import datetime
from core.logger import log
from .search_utils import expand_search_terms


def _parse_timeframe(timeframe: str) -> Dict[str, str]:
    params = {}
    if timeframe and "-" in timeframe:
        start, end = [t.strip() for t in timeframe.split("-")]
        try:
            datetime.fromisoformat(start)
            datetime.fromisoformat(end)
            params["ad_delivery_date_min"] = start
            params["ad_delivery_date_max"] = end
        except ValueError:
            log.warning("Ungültiger Datumsbereich, ignoriere timeframe")
    return params


def search_meta_ads(query: str, region: str, num_ads: int, timeframe: str) -> List[Dict]:
    """Search Meta Ad Library for political ads."""
    token = os.getenv("META_ACCESS_TOKEN")
    if not token:
        raise ValueError("META_ACCESS_TOKEN not set")

    base_url = "https://graph.facebook.com/v18.0/ads_archive"
    results: List[Dict] = []

    for term in expand_search_terms(query):
        params = {
            "search_terms": term,
            "ad_type": "POLITICAL_AND_ISSUE_ADS",
            "ad_reached_countries": region,
            "limit": num_ads,
            "access_token": token,
        }
        params.update(_parse_timeframe(timeframe))
        try:
            resp = requests.get(base_url, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json().get("data", [])
        except Exception as e:
            log.error(f"Meta API request failed for term '{term}': {e}")
            continue

        for ad in data:
            results.append(
                {
                    "id": ad.get("ad_archive_id") or ad.get("id"),
                    "platform": "Meta",
                    "image_path": "",
                    "snapshot_url": ad.get("ad_snapshot_url"),
                    "api_data": ad,
                }
            )
            if len(results) >= num_ads:
                return results[:num_ads]
    return results[:num_ads]
