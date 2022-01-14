import matplotlib.pyplot as plt
import json

from books_scraping.books.books_filename import BooksFilename


def _get_books():
    with open(f"{BooksFilename.JSON_FILE_PATH}{BooksFilename.JSON_FILE_NAME}", 'r') as file:
        return json.load(file)


def _get_attribute(books_list, attribute: str):
    """
    :param books_list: list of books
    :param attribute: one of available attributes: ['price', 'rating', 'stock_availability', 'name']
    :return: attribute list
    """
    return [book[attribute] for book in books_list['books']]


def _rating_savefig():
    books = _get_books()
    fig, ax = plt.subplots(figsize=(12,7))

    x = _get_attribute(books, 'rating')

    ax.hist(x=x, align='mid', bins=[0.5, 1.5, 2.5, 3.5, 4.5, 5.5])
    ax.set(title="Rating Distribution",
           xlabel="Rating",
           ylabel="Number of books")

    plt.savefig('rating.png')


def _price_savefig():
    books = _get_books()
    fig, ax = plt.subplots(figsize=(12,7))

    x = _get_attribute(books, 'price')
    bins = 20

    ax.hist(x=x, align='mid', bins=bins, label=f"Range: ${(max(x) - min(x))/bins:.2f}")
    ax.set(title="Price Distribution",
           xlabel="Price",
           ylabel="Number of books within range",
           xticks=[5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65])

    ax.legend()

    plt.savefig('price.png')


_price_savefig()
_rating_savefig()
