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
    "Times of India": {
        "url": "https://timesofindia.indiatimes.com/",
        "tag": "a",
        "class": "YAhrn",
    },
    "Hacker News": {
        "url": "https://news.ycombinator.com/",
        "tag": "span",
        "class": "titleline",
    },
    "BBC News": {
         "url": "https://www.bbc.com/news",
        "tag": "h3",
        "class": None,
    },
}

def fetch_headlines(source_name, source_config, limit=10):
    """
    Fetch headlines from a news source.
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

        soup = BeautifulSoup(response.text, "lxml")

        if source_config["class"]:
            elements = soup.find_all(
                source_config["tag"],
                class_= source_config["class"]
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
        print(f" [ERROR] cannot reach {source_name}. Check your internet.")
    except requests.exceptions.Timeout:
        print(f" [TIMEOUT] {source_name} took too long to respond.")
    except requests.exceptions.HTTPError as e:
        print(f" [HTTP ERROR] {source_name}: {e}")
    except Exception as e:
        print(f" [UNKNOWN ERROR] {source_name}: {e}")

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