import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time


def get_first_news():#
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }

    url = "https://www.securitylab.ru/news/" #Ссылка на ресурс
    r = requests.get(url=url, headers=headers)# url адрес запроса, и параметры закпроса

    soup = BeautifulSoup(r.text, "lxml")#r.text полученная страница, lxml парсер
    articles_cards = soup.find_all("a", class_="article-card")#Указываем контейнер с которого будем собирать информацию

    news_dict = {}#Словарь для статей, он заполняется на каждой итерации цикла где id это ключ
    for article in articles_cards: #В теле цикла указаны эллементы страницы которые нужно спарсить, циклом пробегаемся по этим элем и собираем инфу
        article_title = article.find("h2", class_="article-card-title").text.strip()
        article_desc = article.find("p").text.strip()
        article_url = f'https://www.securitylab.ru{article.get("href")}'#Получаем ссылку статьи

        article_date_time = article.find("time").get("datetime")
        date_from_iso = datetime.fromisoformat(article_date_time)
        date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S")
        article_date_timestamp = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple())
        #Преобразуем Unix timestamp


        #print(f"{article_title} | {article_url} | {article_date_timestamp}")
        article_id = article_url.split("/")[-1]#Получаем id новости. Берется он из ссылки на статью и вычитаем 4 последних символа
        article_id = article_id[:-4]#Все еще id новости

        news_dict[article_id] = {
            "article_date_timestamp": article_date_timestamp,
            "article_title": article_title,
            "article_url": article_url,
            "article_desc": article_desc
        }#Инструкция сохранения контента id ключ получ данные это значения

        with open("news_dict.json", "w",) as file:#Сохраняем результат работы в json файл
            json.dump(news_dict, file, indent=4, ensure_ascii=False)

def check_news_update():
    with open("news_dict.json", encoding='utf-8') as file:
        news_dict = json.load(file)

    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }

    url = "https://www.securitylab.ru/news/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("a", class_="article-card")

    fresh_news = {}
    for article in articles_cards:
        article_url = f'https://www.securitylab.ru{article.get("href")}'
        article_id = article_url.split("/")[-1]
        article_id = article_id[:-4]

        if article_id in news_dict:
            continue
        else:
            article_title = article.find("h2", class_="article-card-title").text.strip()
            article_desc = article.find("p").text.strip()

            article_date_time = article.find("time").get("datetime")
            date_from_iso = datetime.fromisoformat(article_date_time)
            date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S")
            article_date_timestamp = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple())

            news_dict[article_id] = {
                "article_date_timestamp": article_date_timestamp,
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc
            }

            fresh_news[article_id] = {
                "article_date_timestamp": article_date_timestamp,
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc
            }

        with open("news_dict.json", "w", encoding='utf-8') as file:
            json.dump(news_dict, file, indent=4, ensure_ascii=False)

        return fresh_news

def main():
    get_first_news()


if __name__ == "__main__":
    main()