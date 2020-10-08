import datetime, json

class Account:
    def __init__(self, username, password, bookshelf):
        self.username = username
        self.password = password
        self.bookshelf = bookshelf

    def authenticate(self, password):
        if self.password != password:
            raise ValueError("Napačno geslo.")

    def save_state(self, filename):
        state_dict = {
            "username": self.username,
            "password": self.password,
            "bookshelf": self.bookshelf.state_dict()
        }
        with open(filename, "w", encoding="UTF-8") as file:
            json.dump(state_dict, file, ensure_ascii=False, indent=4)

    @classmethod
    def load_state(acc, filename):
        with open(filename, encoding="UTF-8") as file:
            state_dict = json.load(file)
        name = state_dict["username"]
        password = state_dict["password"]
        bookshelf = Bookshelf.load_state_dict(state_dict["bookshelf"])
        return Account(name, password, bookshelf)

class Bookshelf:
    def __init__(self, books=set()):
        self.books = books

    def state_dict(self):
        return {
            "books" : [book.book_dict() for book in self.books]
        }

    @staticmethod
    def load_state_dict(dictionary):
        new_books = set()
        books = dictionary["books"]
        for book in books:
            new_books.add(Book.book_from_dict(book))
        return Bookshelf(new_books)

    def __str__(self):
        string = "This bookshelf contains: "
        for book in self.books:
            string += book.title + ", "
        return string[:-2] + "."

    def add_book(self, book):
        self.books.add(book)

    def get_book(self, title):
         for book in self.books:
             if book.title == title:
                 return book

    def remove_book(self, title):
        self.books.remove(self.get_book(title))
    
    def get_books(self, author=None, category=None, state=None):
        r = []
        for book in self.books:
            if author == None or book.author == author:
                if category == None or book.category == category:
                    if state == None or book.state == state:
                        r.append(book)
        return r

    def average_rates(self, author=None, category=None, state=None):
        """returns the average reading rate of the group of books given by the constraints. 
        If a rate for a book is calculated as 0, it is not considered."""
        rates = []
        for book in self.get_books(author=author, category=category, state=state):
            if (rate := book.reading_rate()) == 0:
                pass
            else:
                rates.append(rate)
        return sum(rates) / len(rates)

    def predict_time(self, title):
        """returns the predicted time of reading a single book.
        If a book does not have a reading rate, the average of the bookshelf is used"""
        if (time := (book := self.get_book(title)).predicted_time()) != 0:
            return time
        else:
            return self.average_rates() * book.pages

    def predict_remaining_time(self, title):
        return self.predict_time(title) - self.get_book(title).time_spent

    def predicted_times(self, author=None, category=None, state=None):
        """Returns the predicted time of reading the whole library.
        If a book does not have a reading rate, the average rate of the bookshelf is used."""
        times = []
        avg = self.average_rates()
        for book in self.get_books(author=author, category=category, state=state):
            if (time := book.predicted_time()) == 0:
                times.append(book.pages * avg)
            else:
                times.append(time)
        return sum(times)

class Book:
    def __init__(self, title, pages, current_page=0, author="", category="", time_spent=0, state=0, sessions=[]):
        self.title = title
        self.pages = pages
        self.current_page = current_page
        self.author = author
        self.category = category
        self.time_spent = time_spent
        self.state = 0 
# 0 = not reading, 1 = reading, 2 = finished
        self.sessions = sessions

    def __repr__(self):
        return "<" + self.title + ", " + self.author + ", " + str(self.current_page) + "/" + str(self.pages) + ", " + self.category + ", " + str(self.time_spent) + ", " + str(self.state) + ", " + str(self.sessions) + ">"

    def __str__(self):
        return self.title + " by " + self.author + " in category " + self.category

    def book_dict(self):
        return {
                "title" : self.title,
                "pages" : self.pages,
                "current_page" : self.current_page,
                "author": self.author,
                "category" : self.category,
                "time_spent" : self.time_spent,
                "state" : self.state,
                "sessions" : self.sessions
            }

    @staticmethod
    def book_from_dict(dictionary):
        return Book(title=dictionary["title"],
                    pages=dictionary["pages"],
                    current_page=dictionary["current_page"],
                    author=dictionary["author"],
                    category=dictionary["category"],
                    time_spent=dictionary["time_spent"],
                    state=dictionary["state"],
                    sessions=dictionary["sessions"])


    def progress(self):
        return (self.current_page, self.pages, self.time_spent)

    def update_title(self, title):
        self.title = title

    def update_pages(self, pages):
        self.pages = pages

    def update_author(self, author):
        self.author = author

    def update_category(self, category):
        self.category = category

    def update_state(self, new_state):
        self.state = new_state

    def reset_progress(self):
        "Resets the reading progress for given book"
        self.current_page = 0
        self.time_spent = 0
        self.state = 0
        self.sessions=[]

    def new_session(self, session_time, final_page):
        "Adds a new reading session to the book"
        self.time_spent += session_time
        if final_page >= self.pages:
            self.state = 2
        elif final_page > 0:
            self.state = 1
        self.current_page = min(self.pages, final_page)
        self.sessions.append((session_time, final_page))

    def reading_rate(self):
        "Returns a reading rate for current book in minutes/page"
        return self.time_spent / self.current_page

    def predicted_time(self):
        return self.reading_rate() * self.pages




    


b1 = Book("Phenomenology of spirit", 400, author="Hegel", category="Nonsense")
b2 = Book("Science of logic", 200, author="Hegel", category="Logic", current_page=120, time_spent=160)
b3 = Book("Critique of pure reason", 700, author="Kant", category="Nonsense", current_page=432)

shelf = Bookshelf({b1, b2, b3})

shelf.get_book("Phenomenology of spirit").new_session(30, 10)
shelf.get_book("Phenomenology of spirit").new_session(30, 30)
shelf.get_book("Phenomenology of spirit").new_session(60, 43)

print(shelf.get_book("Phenomenology of spirit"))
print(shelf.get_book("Phenomenology of spirit").progress())
print(shelf.get_book("Phenomenology of spirit").reading_rate())
print(shelf.get_book("Phenomenology of spirit").predicted_time())

print(shelf.get_book("Science of logic"))
print(shelf.get_book("Science of logic").progress())
print(shelf.get_book("Science of logic").reading_rate())
print(shelf.get_book("Science of logic").predicted_time())

print(shelf.get_book("Critique of pure reason"))
print(shelf.get_book("Critique of pure reason").progress())
print(shelf.get_book("Critique of pure reason").reading_rate())
print(shelf.get_book("Critique of pure reason").predicted_time())

print([b.title for b in shelf.get_books(author="Hegel")])
print([b.title for b in shelf.get_books(category="Nonsense")])

print(shelf.predicted_times())
print(shelf.average_rates())

shelf2 = Bookshelf.load_state_dict(shelf.state_dict())
print(shelf2)

tevqoon = Account("Tevqoon", "123", shelf)
tevqoon.save_state("tevqoon.json")

tevqoon2 = Account.load_state("tevqoon.json")