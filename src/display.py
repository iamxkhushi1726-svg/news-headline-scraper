from colorama import Fore, Style, init

init(autoreset=True)

SOURCE_COLORS = {
    "Times of India": Fore.CYAN,
    "Hacker News": Fore.YELLOW,
    "BBC News": Fore.GREEN,
}

def print_banner():
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + "     NEWS HEADLINE SCRAPER")
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print()       

def print_headlines(headlines):
    """Print headlines grouped by source with colour coding."""    
    if not headlines:
        print(Fore.RED + "No headlines were fetched. Check your connection.")
        return
    
    current_source = None
    count = 1

    for item in headlines:
        if item["source"] != current_source:
            current_source = item["source"]
            color = SOURCE_COLORS.get(current_source, Fore.WHITE)
            print()
            print(color + Style.BRIGHT + f"[ {current_source.upper()} ]")
            print(color + "_" * 50)

        color = SOURCE_COLORS.get(item["source"], Fore.WHITE)
        title = item["title"]
        if len(title) > 80:
            title = title[:77] + "..."
        
        print(f" {Fore.WHITE}{count:>2}. {color}{title}")
        count += 1
    
    print()
    print(Fore.WHITE + Style.BRIGHT + f"   Total: {len(headlines)} headlines scraped")
    print(Fore.WHITE + f"  Time: {headlines[0]['scraped_at']}")
    print()

def print_summary(headlines):
    """Print a count summary per source."""
    print(Fore.CYAN +Style.BRIGHT + "\n[ SUMMARY BY SOURCE ]")
    sources = {}
    for h in headlines:
        sources[h["source"]] = sources.get(h["source"], 0) + 1
    for src, count in sources.items():
        color = SOURCE_COLORS.get(src, Fore.WHITE)
        bar = "#" * count
        print(f"    {color}{src:<20} {bar} ({count})")