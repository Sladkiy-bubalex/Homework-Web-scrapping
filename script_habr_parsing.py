import re
import bs4
import requests
from datetime import datetime as dt
from fake_headers import Headers


response = requests.get(
    "https://habr.com/ru/articles/",
    headers=Headers(browser="chrome", os="windows").generate(),
)

KEYWORDS = ["дизайн", "фото", "web", "python"]


def find_match(text):
    for word in KEYWORDS:
        pattern = re.compile(rf"\b{word}\b")
        found = bool(pattern.search(text))
        if found:
            return True


soup = bs4.BeautifulSoup(response.text, features="lxml")
news = soup.select_one("div.pull-down")
articles = news.select("article.tm-articles-list__item")

data_info = []
for article in articles:
    link = "https://habr.com" + article.select_one("a.tm-title__link")["href"]
    response = requests.get(link)
    article_soup = bs4.BeautifulSoup(response.text, features="lxml")

    preview_text = article_soup.select_one("h1").text
    article_text = article_soup.find("div", id="post-content-body").get_text()
    time = article_soup.select_one("time")["datetime"]

    if find_match(preview_text):
        data_info.append({"date": time, "header": preview_text, "url": link})
    elif find_match(article_text):
        data_info.append({"date": time, "header": preview_text, "url": link})

for data in data_info:
    print(
        f"Дата публикации: {dt.strptime(data['date'],'%Y-%m-%dT%H:%M:%S.%fZ')}",
        f"Заголовок: {data['header']}",
        f"Cсылка: {data['url']}"
    )
