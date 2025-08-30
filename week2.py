class Book:
    def __init__(self, title, author, isbn, availability):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.availability = availability

class Library:
    def __init__(self, books):
        self.books = books

    def add_book(self, title, author, isbn):
        self.books.append(Book(title, author, isbn, True))

    def find_book(self, title):
        for book in self.books:
            if book.title == title:
                return book
        print("Book not found")
        return None

    def borrow_book(self, title):
        book = self.find_book(title)
        if book.availability:
            book.availability = False
        else:
            print("Book is already borrowed")

    def return_book(self, title):
        book = self.find_book(title)
        if not book.availability:
            book.availability = True
        else:
            print("Book is not borrowed")