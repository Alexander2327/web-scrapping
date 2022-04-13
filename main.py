import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

KEYWORDS = ['Паттерны', 'PyTorch', 'Конфликтов', 'python']
URL = 'https://habr.com/ru/all/'
ua = UserAgent()
HEADERS = {
    'user-agent': ua.random
}


def get_html(url, params=None):
    res = requests.get(url, headers=HEADERS, params=params)
    return res


def get_page_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find_all('a', class_='tm-pagination__page')
    return int(pages[-1].get_text().strip())


def get_content(html, words):
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('article')

    set_words = set(i.lower() for i in words)
    art = set()
    for article in articles:
        heads = article.find_all('span', class_=None)[:-1]
        texts = article.find_all('p')
        for text in texts:
            art.update(text.text.strip().lower().split(' '))
        for head in heads:
            art.update(head.text.strip().lower().split(' '))
        if set_words & art:
            print(
                f'date = {article.find("time").text.strip()}, head = {article.find_all("span")[3].text.strip()},'
                f' link = https://habr.com{article.find_all("a")[2]["href"]}')
        art.clear()


def parse(pages):
    html = get_html(URL)
    if html.status_code == 200:
        if pages:
            pages_count = pages
        else:
            pages_count = get_page_count(html.text)
        for page in range(1, pages_count + 1):
            html = get_html(URL + f'page{page}/')
            get_content(html.text, KEYWORDS)
    else:
        print('Parse ERROR')


if __name__ == '__main__':
    page = int(input('Введите количество страниц для парсинга (по умолчанию все страницы): '))
    parse(page)
