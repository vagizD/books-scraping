import json


def _list():
    with open('books/books.json', 'r') as file:
        books = json.load(file)['books']
    b = [f"{book['name']}, rating: {book['rating']}, price: £{book['price']}, available in stock: {book['stock_availability']}"
         for book in books]
    for book in b:
        print(book)


def _search():
    name = input('What book are you looking for? ')
    with open('books/books.json', 'r') as file:
        books = json.load(file)['books']
        book_names = [book['name'].title() for book in books]
    if name.title() in book_names:
        book = books[book_names.index(name.title())]
        print('This book is on website.')
        print(f"{book['name']}, rating: {book['rating']}, price: £{book['price']}")
        if book['stock_availability']:
            print('Book is also in stock, you can buy it.')
        else:
            print('Book is out of stock, no opportunity to buy it.')


def _menu():
    print(TOOLS)
    func = input("Enter needed tool: ")
    if func not in TOOLS_FUNC.keys():
        print("Wrong tool. Enter on more time.")
        _menu()
    else:
        TOOLS_FUNC[func]()

    _menu()


TOOLS = """
    'list': 'list all books',
    'search': 'search by name',
    'exit': 'exit the program'
        """

TOOLS_FUNC = {
    'list': _list,
    'search': _search,
    'exit': exit
}


_menu()
