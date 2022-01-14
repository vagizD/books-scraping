from bs4 import BeautifulSoup
from books_scraping.parsers.book_parser import BookParser
from books_scraping.locators.book_on_pages_locators import BooksOnPagesLocators


class BooksOnPage:
    """
    Given html item, returns list of books (bs objects).
    """
    def __init__(self, html_item):
        self.soup = BeautifulSoup(html_item, 'html.parser')

    @property
    def books(self):
        locator = BooksOnPagesLocators.BOOKS_LOCATOR
        attrs = BooksOnPagesLocators.BOOKS_ATTRS
        return [BookParser(e) for e in self.soup.find_all(locator, attrs)]
