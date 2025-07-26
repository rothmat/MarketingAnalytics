import argparse
from datetime import date
from tools.ad_library.meta_api import search_meta_ads
from tools.ad_library.google_api import search_google_ads
from core.logger import log


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search political ads on Meta and Google")
    parser.add_argument("query", help="Search terms or initiative")
    parser.add_argument("--region", default="CH", help="Country code")
    parser.add_argument("--platform", choices=["Meta", "Google", "Both"], default="Both")
    parser.add_argument("--num_ads", type=int, default=10)
    parser.add_argument("--start_date", help="YYYY-MM-DD")
    parser.add_argument("--end_date", help="YYYY-MM-DD")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    start = args.start_date or str(date.today())
    end = args.end_date or str(date.today())
    timeframe = f"{start} - {end}"

    ads = []
    if args.platform == "Meta":
        ads = search_meta_ads(args.query, args.region, args.num_ads, timeframe)
    elif args.platform == "Google":
        ads = search_google_ads(args.query, args.region, args.num_ads, timeframe)
    else:
        half = args.num_ads // 2
        ads = search_meta_ads(args.query, args.region, half, timeframe)
        ads += search_google_ads(args.query, args.region, args.num_ads - len(ads), timeframe)

    for ad in ads:
        log.info(f"{ad['platform']} Ad {ad['id']} -> {ad.get('snapshot_url')}")


if __name__ == "__main__":
    main()
