import json

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
        string = "Ta knjižna polica vsebuje: "
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
    
    def get_books(self, authors=[], categories=[], states=[]):
        r = []
        for book in self.books:
            if authors == [] or book.author in authors:
                if categories == [] or book.category in categories:
                    if states == [] or book.state in states:
                        r.append(book)
        return r

    def list_authors(self):
        a = set()
        for book in self.books:
            a.add(book.author)
        return list(a)

    def list_categories(self):
        c = set()
        for book in self.books:
            c.add(book.category)
        return list(c)

    def list_books(self, authors=[], categories=[], states=[]):
        t = set()
        for book in self.get_books(authors, categories, states):
            t.add(book.title)
        return list(t)

    def book_number(self, authors=[], categories=[], states=[]):
        return len(self.get_books(authors, categories, states))

    def average_rates(self, authors=[], categories=[], states=[]):
        """returns the average reading rate of the group of books given
        by the constraints. If a rate for a book is calculated as 0, 
        it is not considered."""
        rates = []
        for book in self.get_books(authors, categories, states):
            if (rate := book.reading_rate()) == 0:
                pass
            else:
                rates.append(rate)
        return sum(rates) / len(rates) if len(rates) != 0 else 0

    def predict_time(self, title):
        """returns the predicted time of reading a single book. If a 
        book does not have a reading rate, the average of the bookshelf
        is used"""
        if (time := (book := self.get_book(title)).predicted_time()) != 0:
            return time
        else:
            return self.average_rates() * book.pages

    def predict_remaining_time(self, title):
        return self.predict_time(title) - self.get_book(title).time_spent

    def total_times(self, authors=[], categories=[], states=[]):
        t = 0
        for book in self.get_books(authors, categories, states):
            t += book.time_spent
        return t

    def predicted_times(self, authors=[], categories=[], states=[]):
        """Returns the predicted time of reading the selected group.
        If a book does not have a reading rate, the average rate of the
        group is used."""
        times = []
        avg = self.average_rates()
        for book in self.get_books(authors, categories, states):
            if (time := book.predicted_time()) == 0:
                times.append(book.pages * avg)
            else:
                times.append(time)
        return sum(times)

    def group_stats(self, authors=[], categories=[], states=[]):
        spent = self.total_times(authors, categories, states)
        return {"avg_rates" : str(round(self.average_rates(authors, categories, states), 2)),
                "time_spent_h" : str(round(spent / 60, 1)),
                "time_rest_h" : str(round((self.predicted_times(authors, categories, states) - spent) / 60, 1)),
                "book_number" : self.book_number(authors, categories, states),
                "finished_number" : self.book_number(authors, categories, [2])}

class Book:
    def __init__(self, title, pages, current_page=0, author="", 
                 category="", time_spent=0, state=0):
        self.title = title
        self.pages = pages
        self.current_page = current_page
        self.author = author
        self.category = category
        self.time_spent = time_spent
        self.state = 0 

    def __repr__(self):
        return ("<" + self.title + ", " + self.author + ", "
            + str(self.current_page) + "/" + str(self.pages)
            + ", " + self.category + ", " + str(self.time_spent)
            + ", " + str(self.state) + ">")

    def __str__(self):
        return (self.title + " avtorja " 
            + self.author + " v kategoriji " 
            + self.category)

    def book_dict(self):
        return {
                "title" : self.title,
                "pages" : self.pages,
                "current_page" : self.current_page,
                "author": self.author,
                "category" : self.category,
                "time_spent" : self.time_spent,
                "state" : self.state,
            }

    @staticmethod
    def book_from_dict(dictionary):
        return Book(title=dictionary["title"],
                    pages=dictionary["pages"],
                    current_page=dictionary["current_page"],
                    author=dictionary["author"],
                    category=dictionary["category"],
                    time_spent=dictionary["time_spent"],
                    state=dictionary["state"])

    def update_title(self, title):
        self.title = title

    def update_pages(self, pages):
        self.pages = pages
        if self.pages < self.current_page:
            self.current_page = self.pages
            self.state = 2

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

    def new_session(self, session_time, final_page):
        "Adds a new reading session to the book"
        self.time_spent += session_time
        if final_page >= self.pages:
            self.state = 2
        elif final_page > 0:
            self.state = 1
        self.current_page = min(self.pages, final_page)

    def reading_rate(self):
        "Returns a reading rate for current book in minutes/page"
        if self.current_page == 0:
            return 0
        else:
            return round(self.time_spent / self.current_page, 2)

    def predicted_time(self):
        return self.reading_rate() * self.pages

    def basic_stats(self):
        return {"progress_quotient" : str(self.current_page) + "/" + str(self.pages), 
                "percentage" : str(round(self.current_page / self.pages, 4) * 100) + "%",
                "time_spent_h" : str(round(self.time_spent / 60, 1)),
                "time_rest_h" : str(round((self.predicted_time() - self.time_spent) / 60, 1)),
                "reading_rate" : str(self.reading_rate())}



    


