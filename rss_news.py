# Парсинг RSS с переводом на русский язык
import feedparser
from translate import Translator



# Берем срез первых 5 элементов из списка entries
def parse_rss(rss_source: str, limit: int = 5) -> list[dict[str, str]]:
    news_list = []      # список ловарей с новостями
    feed = feedparser.parse(rss_source, agent="Mozilla/5.0")
    for entry in feed.entries[:limit]:
        news_dict = {
            'published': entry.get('published', 'Не указана'),
            'title': entry.get('title', 'Не указана'),
            'link': entry.get('link', 'Не указана'),
            'description': entry.get('description', 'Не указана')
        }
        news_list.append(news_dict)
    return news_list


def translate_to_ru(items: list[dict[str, str]], from_lang: str = "en") -> list[dict[str, str]]:
    translator = Translator(from_lang=from_lang, to_lang="ru")
    for item in items:
        item['title'] = translator.translate(item['title'])
        item['description'] = translator.translate(item['description'])
    return items

def print_rss(news_list: list[dict[str, str]]):
    for value in news_list:
        print(value['published'])
        print(value['title'])
        print(value['link'])
        print(value['description'])        
        print("-" * 80)


if __name__ == "__main__":
    rss_source = "https://www.wired.com/feed/tag/ai/latest/rss"
    #rss_source = "https://www.allsides.com/rss/news"
    #rss_url = "https://shir-man.com/api/rss"

    news_list = parse_rss(rss_source, 10)
    news_list_ru = translate_to_ru(news_list)
    print_rss(news_list_ru)
    