import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scraper import scrape_all, save_to_csv
from src.display import print_banner, print_headlines, print_summary


def main():
    parser = argparse.ArgumentParser(
        description="News Headline Scraper — Project 02/100"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of headlines per source (default: 10)"
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save headlines to a CSV file in data/"
    )
    parser.add_argument(
        "--no-display",
        action="store_true",
        help="Skip terminal display (useful with --save)"
    )
    args = parser.parse_args()

    print_banner()
    print("  Scraping headlines...\n")

    headlines = scrape_all(limit=args.limit)

    if not args.no_display:
        print_headlines(headlines)
        print_summary(headlines)

    if args.save:
        save_to_csv(headlines)
    else:
        print("  Tip: Run with --save to export headlines to CSV\n")


if __name__ == "__main__":
    main()