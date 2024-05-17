from bs4 import BeautifulSoup as bs
from celery import Celery, Task
import requests

import constats


app = Celery("tasks", broker="redis://localhost:6379/0")


class ParseTask(Task):
    def run(self, page: int) -> None:
        url = constats.URL_PARSE + str(page)
        response = requests.get(url, headers=constats.HEADERS)
        soup = bs(response.text, "lxml")
        orders = soup.find_all("div", class_="registry-entry__header-top__icon")

        for order in orders:
            for url_view in order.find_all("a"):
                url_str = url_view.get("href")
                if "view.html" in url_str:
                    url_xml = constats.URL_HOST + url_str.replace(
                        "view.html", "viewXml.html"
                    )
                    number_order = url_xml.split("=")[-1]
                    ParseXML().run(url_xml=url_xml, number_order=number_order)


class ParseXML(Task):
    def run(self, url_xml: str, number_order: str) -> None:
        response = requests.get(url_xml, headers=constats.HEADERS)
        soup = bs(response.text, "xml")
        publish_time = soup.find("publishDTInEIS").text
        data = {number_order: publish_time}
        print(data)


if __name__ == "__main__":
    for page in range(1, 3):
        ParseTask().run(page=str(page))
