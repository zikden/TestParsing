from bs4 import BeautifulSoup as bs
from celery import Celery, Task
import requests

import constats


app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)


class ParseTask(Task):
    name = "parse_main_page"

    def run(self, page: str,  *args, **kwargs):
        print("good")
        url = constats.URL_PARSE + page
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
                    ParseXML().apply_async(args=(url_xml, number_order))


class ParseXML(Task):
    name = "parse_xml_order"

    def run(self, url_xml: str, number_order: str, *args, **kwargs):
        print("good")
        response = requests.get(url_xml, headers=constats.HEADERS)
        soup = bs(response.text, "xml")
        publish_time = soup.find("publishDTInEIS").text
        data = {number_order: publish_time}
        print(data)


app.register_task(ParseTask)
app.register_task(ParseXML)
