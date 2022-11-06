import time
import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from requests.models import Response

from base import Issue, Paper

DEBUG = False

class EurRadiology(object):
    def __init__(self):
        self.base_url = "https://link.springer.com/journal/330/volumes-and-issues/"

    def get_issue(self, vol: int, iss: int) -> Issue:
        issue = Issue()
        page_urls:list[str]  = []
        page_htmls:list[Response] = []
        page_soups:list[BeautifulSoup] = []
        
        issue_base_url = self.base_url + "{volumes}-{issue}".format(volumes=vol, issue=iss)
        page_urls.append(issue_base_url)
        issue.set_url(issue_base_url)

        page1_html = requests.get(issue_base_url)
        page_htmls.append(page1_html)

        page1_soup = BeautifulSoup(page1_html.text, "lxml")
        page_soups.append(page1_soup)

        # get the number of pages
        pages_set:ResultSet[Tag] = page1_soup.find_all(name="li", class_="c-pagination__item")
        for page_tag in pages_set:
            if page_tag.has_attr("data-page"):
                if (page_tag["data-page"] != "1"): # because page 1 is appended
                    issue_url_with_page = issue_base_url + "?page={p}".format(p = page_tag["data-page"])
                    page_urls.append(issue_url_with_page)

        # request all pages and parse
        for index,page_url in enumerate(page_urls):
            if index != 0 and not DEBUG:
                page_html = requests.get(page_url)
                page_htmls.append(page_html)
                page_soup = BeautifulSoup(page_html.text, "lxml")
                page_soups.append(page_soup)
                time.sleep(0.1)
        
        # get all article title and href
        for page_soup in page_soups:
            article_set:ResultSet[Tag] = page_soup.find_all(name="article", class_="c-card c-card--flush u-flex-direction-row")
            for article_tag in article_set:
                title_tag = article_tag.find(attrs={"data-track-action": "clicked article"})
                title = title_tag.get_text()
                href = title_tag["href"]
                issue.add_paper(Paper(href, title))

        return issue

# test
if __name__ == "__main__":
    if (DEBUG):
        object = EurRadiology()
        object.get_issue(32, 10)
