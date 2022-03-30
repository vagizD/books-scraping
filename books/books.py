import requests
import json
import aiohttp
import asyncio

from books_scraping.pages.books_on_page import BooksOnPage
from books_scraping.books.books_filename import BooksFilename


async def _fetch_page(session, url):
    async with session.get(url) as response:
        return response.content


async def get_multiple_pages(loop, *urls):
    tasks = []
    async with aiohttp.ClientSession(loop=loop) as session:
        for url in urls:
            tasks.append(_fetch_page(session, url))  # creates coroutine objects
            grouped_tasks = asyncio.gather(*tasks)
            return await grouped_tasks


def _get_books_content():
    """
    Extracts books contents from https://books.toscrape.com/catalogue/category/books_1. Uses asynchronous libraries to
    reduce the requests completion time.
    :return: list of BookParser objects.
    """
    books_catalogue = []

    loop = asyncio.get_event_loop()
    urls = [f'https://books.toscrape.com/catalogue/category/books_1/page-{i}.html' for i in range(1,51,1)]
    page_contents = loop.run_until_complete(get_multiple_pages(loop, *urls))

    for page_content in page_contents:
        books = BooksOnPage(page_content)
        books_catalogue.append(books.books)

    books_catalogue = [item for sublist in books_catalogue for item in sublist]
    return books_catalogue


# def _get_books_content():
#     """
#     Extracts books contents from https://books.toscrape.com/catalogue/category/books_1. Iterates over every page of
#     catalogue.
#     :return: list of BookParser objects.
#     """
#     books_catalogue = []
#     for i in range(1, 51, 1):
#         page_content = requests.get(f'https://books.toscrape.com/catalogue/category/books_1/page-{i}.html').content
#         books = BooksOnPage(page_content)
#         books_catalogue.append(books.books)
#     books_catalogue = [item for sublist in books_catalogue for item in sublist]
#     return books_catalogue


def _write_books_content(filename: str):
    """
    Rewrites the contents of given json file with BooksParser objects properties
    :param filename: json file to write contents to.
    """
    with open(filename, 'w') as json_file:
        books = _get_books_content()
        books_dict = {'books': []}
        for book in books:
            books_dict['books'].append({
                "name": book.title,
                "rating": book.rating,
                "stock_availability": book.stock,
                "price": book.price
            })
        json.dump(books_dict, json_file, indent=4)
        print(f"Done. {len(books)} written to {filename}.")


_write_books_content(f"{BooksFilename.JSON_FILE_PATH}{BooksFilename.JSON_FILE_NAME}")
