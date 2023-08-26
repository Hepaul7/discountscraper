import requests
from bs4 import BeautifulSoup
from requests import Response
from typing import Optional, Set
from urllib.parse import urljoin

URL = 'https://www.uoftbookstore.com/general-books/genres?page=1'


class WebScrapper:
    """ Class for

    """
    def __init__(self, url) -> None:
        self.url = url
        self.response = None
        self.soup = None

    def get_response(self) -> Response:
        """ Sends an HTTP GET request to the given URL, Return the Response
        """
        self.response = requests.get(self.url)
        return self.response if self.response.status_code == 200 else None

    def get_soup(self) -> Optional[BeautifulSoup]:
        """ Returns a BeautifulSoup object of the website if page retrieved"""
        response = self.response if self.response else self.get_response()
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.text, 'html.parser')
            return self.soup
        return None

    def check_soup(self) -> Optional[BeautifulSoup]:
        soup = self.soup if self.soup else self.get_soup()
        return soup

    def get_page_title(self) -> str:
        """ Sends an HTTP GET request to the given URL and returns the
        title of the webpage.
        """
        soup = self.check_soup()
        if not soup:
            return "Failed to retrieve webpage"

        # find and extract the title tag
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text()
        else:
            return "No title found on the webpage."

    def get_links(self) -> Optional[Set[str]]:
        """ Return a set of all the links that could be branched into
        from the main link"""
        soup = self.check_soup()
        if not soup:
            return
        # extract all anchor tags (links) from the page
        anchor_tags = soup.find_all('a', href=True)

        base_url = self.response.url
        full_urls = {urljoin(base_url, tag['href']) for tag in anchor_tags}

        return full_urls


def get_all_products(scrapper: WebScrapper) -> Optional[Set[str]]:
    """ Return a set of products (meant for UofT BookStore Website)
    """
    all_urls = scrapper.get_links()
    products = set()
    for url in all_urls:
        if 'uoftbookstore' not in str(url):
            continue
        print(url, products)
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            if soup.find(class_='product-details-full'):
                products.add(url)
    return products


def check_discount(products: Set[str]) -> Optional[Set[str]]:
    """ For each of the products, check if there is a
    discount, return a set of all products with discounts"""

    for product in products:
        ...


page_title = WebScrapper(URL).get_page_title()
all_a = WebScrapper(URL).get_links()
all_p = get_all_products(WebScrapper(URL))

print(f"Page Title: {page_title}")
print(f"a: {all_a}")
