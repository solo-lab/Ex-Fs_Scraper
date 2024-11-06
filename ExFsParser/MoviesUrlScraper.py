from typing import List
import requests
from bs4 import BeautifulSoup
from . import logger


class MoviesUrlScraper:
    _site_url: str = 'https://ex-fs.net'
    _movie_type: str

    def __init__(self, movie_type: str):
        self._movie_type = movie_type

    def get_movie_urls(self, page: int):
        try:
            response = requests.get(f'{self._site_url}/{self._movie_type}/page/{page}/')
        except Exception as e:
            logger.error(f"Error fetching site: {e}")
            return

        site_html = response.text
        soup = BeautifulSoup(site_html, features="html.parser")

        return self._extract_movie_urls(soup)

    def max_pages(self):
        try:
            response = requests.get(f'{self._site_url}/{self._movie_type}')
        except Exception as e:
            logger.error(f"Error fetching site: {e}")
            return

        site_html = response.text
        soup = BeautifulSoup(site_html, features="html.parser")

        nav = soup.find('div', {'class': 'navigations'})
        pages_array_str = []
        page_url = nav.find_all('a')
        for page in page_url:
            pages_array_str.append(page.text)
        pages_array_str.pop()

        pages_array = [int(num_string) for num_string in pages_array_str]
        pages_array.sort()

        return pages_array[-1]

    def _extract_movie_urls(self, soup) -> List[str]:
        """
        Extracts movie URLs from the page by finding all 'a' tags with class 'MiniPostPoster'
        and collecting their 'href' attributes.
        """
        url_elements = soup.find_all('a', {"class": "MiniPostPoster"})
        return [element['href'] for element in url_elements]
