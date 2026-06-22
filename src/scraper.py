import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

SOURCES = {
    "Hacker News": {
        "url": "https://news.ycombinator.com/",
        "tag": "span",
        "class": "titleline",
        "link_tag": "a",
    },
    "BBC News": {
        "url": "https://feeds.bbci.co.uk/news/rss.xml",
        "tag": "title",
        "class": None,
        "is_rss": True,
    },
    "Times of India": {
        "url": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
        "tag": "title",
        "class": None,
        "is_rss": True,
    },
}

def fetch_headlines(source_name, source_config, limit=10):
    """
    Fetch headlines from a news source.
    Supports both HTML scraping and RSS/XML feeds.
    Returns a list of dicts with title, source, and timestamp.
    """
    headlines = []
    try:
        response = requests.get(
            source_config["url"],
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()

        # RSS/XML feed path
        if source_config.get("is_rss"):
            soup = BeautifulSoup(response.content, "xml")
            items = soup.find_all("item")
            for item in items[:limit]:
                title_tag = item.find("title")
                if title_tag:
                    text = title_tag.get_text(strip=True)
                    # Skip the channel title (first item is usually feed name)
                    if text and len(text) > 10 and text != source_name:
                        headlines.append({
                            "title": text,
                            "source": source_name,
                            "url": source_config["url"],
                            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })

        # Regular HTML scraping path
        else:
            soup = BeautifulSoup(response.text, "lxml")
            if source_config["class"]:
                elements = soup.find_all(
                    source_config["tag"],
                    class_=source_config["class"]
                )
            else:
                elements = soup.find_all(source_config["tag"])

            for el in elements[:limit]:
                text = el.get_text(strip=True)
                if text and len(text) > 10:
                    headlines.append({
                        "title": text,
                        "source": source_name,
                        "url": source_config["url"],
                        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })

    except requests.exceptions.ConnectionError:
        print(f"  [ERROR] Cannot reach {source_name}. Check your internet.")
    except requests.exceptions.Timeout:
        print(f"  [TIMEOUT] {source_name} took too long to respond.")
    except requests.exceptions.HTTPError as e:
        print(f"  [HTTP ERROR] {source_name}: {e}")
    except Exception as e:
        print(f"  [UNKNOWN ERROR] {source_name}: {e}")

    return headlines

def scrape_all(limit=10):
    """Scrape headlines from all configured sources."""
    all_headlines = []
    for name, config in SOURCES.items():
        print(f" Fetching from {name}...")       
        results = fetch_headlines(name, config, limit=limit)
        all_headlines.extend(results) 
        print (f" Got {len(results)} headlines from {name}")
    return all_headlines

def save_to_csv(headlines, output_dir="data"):
    """Save headlines list to a timestamped CSV file."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")   
    filename = os.path.join(output_dir, f"headlines_{timestamp}.csv")

    fieldnames =["title", "source", "url", "scraped_at"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(headlines)

    print(f"\n saved {len(headlines)} headlines to {filename}")
    return filename