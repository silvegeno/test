# Парсинг RSS
import feedparser

print("Старт")

rss_url = "https://www.wired.com/feed/tag/ai/latest/rss"
# https://techcrunch.com/category/artificial-intelligence/feed/#


feed = feedparser.parse(rss_url, agent="Mozilla/5.0")

# Берем срез первых 5 элементов из списка entries


def parse_rss(xml_text: str, limit: int = 5) -> list[dict[str, str]]:
    for entry in feed.entries[:limit]:
        print(entry.get('published', 'Не указана'))
        print(entry.title)
        print(entry.link)
        print(entry.description)
        print("-" * 60)


if __name__ == "__main__":
    parse_rss(feed, 5)