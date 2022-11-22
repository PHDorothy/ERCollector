import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

url = "https://link.springer.com/article/10.1007/s00330-022-08793-5"

html = requests.get(url)

soup = BeautifulSoup(html.text, "lxml")

author_list_item:ResultSet[Tag] = soup.find_all(name="li", class_="c-article-author-list__item")

for author_item in author_list_item:
    auth = author_item.find(attrs={"data-test": "author-name"})
    print(auth.get_text())