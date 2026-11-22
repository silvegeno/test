# Парсинг RSS
import feedparser



# Берем срез первых 5 элементов из списка entries
def parse_rss(rss_url: str, limit: int = 5) -> list[dict[str]]:
    news_dict = {}
    news_list = []
    feed = feedparser.parse(rss_url, agent="Mozilla/5.0")
    for entry in feed.entries[:limit]:
        news_dict = {
            'published': entry.get('published', 'Не указана'),
            'title': entry.title,
            'link': entry.link,
            'summary': entry.summary
        }
        news_list.append(news_dict)
    return news_list


def print_rss(news_list: dict[str]):
    for value in news_list:
        print(value['published'])
        print(value['title'])
        print(value['link'])
        print(value['summary'])        
        print("-" * 60)


if __name__ == "__main__":
    rss_url = "https://www.wired.com/feed/tag/ai/latest/rss"
    # https://techcrunch.com/category/artificial-intelligence/feed/#

    news_list = parse_rss(rss_url, 3)
    print_rss(news_list)
    