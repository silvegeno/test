# Парсинг RSS
import feedparser

print("Старт")

rss_url = "https://www.wired.com/feed/tag/ai/latest/rss"
# https://techcrunch.com/category/artificial-intelligence/feed/#


# Берем срез первых 5 элементов из списка entries
def parse_rss(rss_url: str) -> list[dict[str]]:
    feed = feedparser.parse(rss_url, agent="Mozilla/5.0")
    print(feed.entries)
    return feed


def print_rss(rss_url: str, limit: int = 5):
    for entry in feed.entries[:limit]:
        print(entry.get('published', 'Не указана'))
        print(entry.title)
        print(entry.link)
        print(entry.summary)        
        print("-" * 60)


if __name__ == "__main__":
    feed = parse_rss(rss_url)
    print_rss(feed, 5)