# News Headline Scraper

> Project 02/100 — Building a strong GitHub portfolio from scratch.

Scrapes live news headlines from multiple sources (Times of India, Hacker News, BBC News),
displays them in colour-coded terminal output, and optionally exports to a timestamped CSV file.

## Features

- Scrapes from 3 live news sources simultaneously
- Colour-coded terminal output grouped by source
- Summary bar chart per source in terminal
- Export to timestamped CSV in data/
- Graceful error handling (timeout, HTTP errors, connection failure)
- Configurable headline limit via CLI flag

## Tech Stack

- Python 3.x
- requests (HTTP fetching)
- BeautifulSoup4 + lxml (HTML parsing)
- colorama (terminal colours)
- csv (data export)
- argparse (CLI interface)

## Installation

```bash
git clone https://github.com/iamxkhushi1726-svg/news-headline-scraper.git
cd news-headline-scraper
pip install -r requirements.txt
```

## Usage

```bash
# Scrape and display headlines (10 per source)
python src/main.py

# Limit to 5 headlines per source
python src/main.py --limit 5

# Scrape and save to CSV
python src/main.py --save

# Scrape 8 headlines per source and save
python src/main.py --limit 8 --save
```

## Project Structure

```
news-headline-scraper/
├── src/
│   ├── scraper.py    # Fetching and CSV export logic
│   ├── display.py    # Terminal display and formatting
│   └── main.py       # CLI entry point
├── data/             # CSV exports go here (gitignored)
├── requirements.txt
├── .gitignore
└── README.md
```

## What I Learned

- How to send HTTP requests with custom headers to avoid bot detection
- How to parse HTML with BeautifulSoup and extract specific elements
- How to handle multiple error types (timeout, HTTP, connection)
- How to separate concerns: scraping logic vs display logic vs entry point
- How to export structured data to CSV with Python's csv module

## Part of 100 Projects Challenge

Project 02 of my 100-project challenge to secure AI/ML and software engineering internships.

Follow my progress: [GitHub Profile](https://github.com/iamxkhushi1726-svg)