# Парсинг RSS
import feedparser



# Берем срез первых 5 элементов из списка entries
def parse_rss(rss_url: str, limit: int = 5) -> list[dict[str, str]]:
    news_list = []      # список ловарей с новостями
    feed = feedparser.parse(rss_url, agent="Mozilla/5.0")
    for entry in feed.entries[:limit]:
        news_dict = {
            'published': entry.get('published', 'Не указана'),
            'title': entry.get('title', 'Не указана'),
            'link': entry.get('link', 'Не указана'),
            'description': entry.get('description', 'Не указана')
        }
        news_list.append(news_dict)
    return news_list


def print_rss(news_list: list[dict[str, str]]):
    for value in news_list:
        print(value['published'])
        print(value['title'])
        print(value['link'])
        print(value['description'])        
        print("-" * 80)


if __name__ == "__main__":
    rss_url = "https://www.wired.com/feed/tag/ai/latest/rss"
    #rss_url = "https://www.allsides.com/rss/news"
    #rss_url = "https://shir-man.com/api/rss"

    news_list = parse_rss(rss_url, 3)
    #print(news_list)
    print_rss(news_list)
    