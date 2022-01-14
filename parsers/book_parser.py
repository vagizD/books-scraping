import re

from books_scraping.locators.book_items_locators import BookItemsLocators


class BookParser:
    """
    Given BeautifulSoup object, contains book items as properties.
    """
    def __init__(self, parent):
        self.parent = parent

    def __repr__(self):
        return f'"{self.title}", rating: {self.rating}, price: £{self.price}, instock: {self.stock}'

    @property
    def title(self):
        locator = BookItemsLocators.TITLE_LOCATOR
        return self.parent.select_one(locator).attrs.get("title")

    @property
    def price(self):
        locator = BookItemsLocators.PRICE_LOCATOR
        price_string = self.parent.select_one(locator).string
        price = re.findall("[0-9]+\.[0-9]+", price_string)
        return float(price[0])

    @property
    def stock(self):
        locator = BookItemsLocators.STOCK_LOCATOR
        stock_text = self.parent.select_one(locator).text
        stock_strings = re.findall("[A-z]+", stock_text)
        if f"{stock_strings[0]} {stock_strings[1]}" == "In stock":
            return True
        else:
            return False

    @property
    def rating(self):
        locator = BookItemsLocators.RATING_LOCATOR
        classes = self.parent.select_one(locator).attrs.get('class')
        rating = [c for c in classes if c != 'star-rating'][0]
        if rating == 'One':
            return 1
        elif rating == "Two":
            return 2
        elif rating == "Three":
            return 3
        elif rating == "Four":
            return 4
        else:
            return 5
