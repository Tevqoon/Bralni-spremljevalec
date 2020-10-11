import model

FILTER_AUTHOR = []
FILTER_CATEGORY = []
FILTER_READING = []

def blue(string):
    return f'\033[1;94m{string}\033[0m'

def red(string):
    return f'\033[1;91m{string}\033[0m'

def save():
    USER.save_state(FILENAME)

def force_positive_integer(allow_empty=False, default="", leq_on=False):
    while True:
        choice = input("* ")
        if choice == "" and allow_empty:
            return default
        if leq_on:
            if not(choice.isnumeric() and int(choice) >= 0):
                print(red("Prosimo vnesite veljavno izbiro."))
            else:
                return int(choice)
        else:
            if not(choice.isnumeric() and int(choice) > 0):
                print(red("Prosimo vnesite veljavno izbiro."))
            else:
                return int(choice)

def make_choice(choices, multi=False):
    while True:
        for n, c in enumerate(choices):
<<<<<<< HEAD
            if c in ["Nazaj", "Vse"]:
=======
            if c == "Nazaj":
>>>>>>> ed3c69fcfd501c994c7f853cafe6b96a26666463
                c = blue(c)
            print(blue(str(n + 1)) + ") " + c)
        if multi:
            r = []
            choice = str(force_positive_integer(allow_empty=True))
            if choice == "":
                return []
            else:
                for i in range(1, 1 + len(choices)):
                    if str(i) in choice:
                        r.append(choices[i - 1])
                return r
        else:
            choice = force_positive_integer()
            return choices[choice - 1]

def init():
    choice = make_choice(["novo", "obstoječo"])
    global USER
    global FILENAME
    if choice == "novo":
        print("""Prosimo vnesite uporabniško ime.""")
        username = input("* ")
        print("""Prosimo vnesite ime datoteke (brez končnice .json), kamor boste shranili svoj račun.""")
        FILENAME = input("* ") + ".json"
        USER = model.Account(username, "", model.Bookshelf())
        save()
        print("""Hvala. Uživajte v uporabi.""")
    elif choice == "obstoječo":
        print("""prosimo vnesite ime datoteke (brez končnice .json), ki jo želite naložiti.""")
        FILENAME = input("* ") + ".json"
        try:
            USER = model.Account.load_state(FILENAME)
        except FileNotFoundError:
            print(red("Neveljavno ime datoteke. Prosimo, poskusite še enkrat."))
            init()

def group_statistics(authors=[], categories=[], states=[]):
    s = USER.bookshelf.group_stats(authors, categories, states)
    if s["book_number"] != 0:
        print("Prebrane knjige: " + str(s["finished_number"]) + "/" + str(s["book_number"])
          + " (" + str(round((s["finished_number"] / s["book_number"]) * 100, 2)) + "%)")
        print("Skupni čas branja: " + s["time_spent_h"] + " ur.")
        print("Predviden preostali skupni čas: " + s["time_rest_h"] + " ur.")
        print("Povprečna hitrost branja: " + s["avg_rates"] + " minut/stran.")
    else:
        print("V tej skupini še ni knjig.")

def book_statistics(title):
    s = USER.bookshelf.get_book(title).basic_stats()
    rem_time = round(USER.bookshelf.predict_remaining_time(title) / 60, 1)
    print("Prebrane strani: " + s["progress_quotient"] + " (" + s["percentage"] + ")")
    print("Trenutni čas branja: " + s["time_spent_h"] + " ur.")
    print("Predviden preostali čas: " + str(rem_time) + " ur.")
    print("Povprečna hitrost branja: " + s["reading_rate"] + " minut/stran.")

def book_adder():
    print("Prosimo, vnesite naslov knjige" + red("(obvezno)") + ": ")
    title = input("* ")
    while title == "" or title in USER.bookshelf.list_books():
        if title == "":
            print(red("Prosimo, vnesite naslov."))
        else:
            print(red("Naslovi se ne smejo ponavljati."))
        title = input("* ")
    print("Prosimo, vnesite število strani" + red("(obvezno)") + ": ")
    pages = force_positive_integer()
    print("Vnesite trenutno stran (Če še ne berete, pustite prazno):")
    current_page = force_positive_integer(allow_empty=True, default=0, leq_on=True)
    print("Vnesite avtorja (ni obvezno):")
    author = input("* ")
    print("Vnesite kategorijo knjige (ni obvezno):")
    category = input("* ")
    print("Koliko časa že berete knjigo v minutah? (Če še ne, pustite prazno):")
    time_spent = force_positive_integer(allow_empty=True, default=0, leq_on=True)
    book = model.Book(title, pages, current_page, author, category, time_spent)
    USER.bookshelf.add_book(book)
    print("Knjiga uspešno dodana.")

def list_filters():
    stanja = ["nezačete", "brane", "prebrane"]
    if FILTER_AUTHOR == [] and FILTER_CATEGORY == [] and FILTER_READING == []:
        print("Trenutno ni aktivnih filtrov.")
    elif FILTER_AUTHOR != []:
        string = ""
        for i in FILTER_AUTHOR:
            string += i + ", "
        print("Trenutno filtrirate po avtorjih: " + string[:-2] + ".")
        
        if FILTER_CATEGORY != []:
            string = "" 
            for i in FILTER_CATEGORY:
                string += i + ", "
            print("In po kategorijah: " + string[:-2] + ".")
    elif FILTER_CATEGORY != []:
        string = ""
        for i in FILTER_CATEGORY:
                string += i + ", "
        print("Trenutno filtrirate po kategorijah: " + string[:-2] + ".")
    if FILTER_READING != []:
        if len(FILTER_READING) == 1:
            print("Trenutno prikazujete le " + stanja[FILTER_READING[0]] + " knjige.")
        elif len(FILTER_READING) == 2:
            print("Trenutno prikazujete le " + stanja[FILTER_READING[0]] + " ter "
                  + stanja[FILTER_READING[1]] + " knjige.")

def set_filters():
    list_filters()
    reading_level = {"Nezačete" : 0, "Začete" : 1, "Prebrane" : 2}
    global FILTER_AUTHOR
    global FILTER_CATEGORY
    global FILTER_READING
    print("Kaj želite storiti?")
    choice = make_choice(["Izprazni filtre", "Nastavi avtorje", "Nastavi kategorije", "Nastavi stanje knjige", "Nazaj"])
    if choice == "Izprazni filtre":
        FILTER_AUTHOR = []
        FILTER_CATEGORY = []
        FILTER_READING = []
        set_filters()
    elif choice == "Nastavi avtorje":
        print("Izberite avtorje (vpišite številke vseh, ki jih želite v filtru).")
        mchoice = make_choice(["Vse"] + sorted(USER.bookshelf.list_authors()), multi=True)
        FILTER_AUTHOR = [] if "Vse" in mchoice else mchoice
        set_filters()
    elif choice == "Nastavi kategorije":
        print("Izberite kategorije (vpišite številke vseh, ki jih želite v filtru).")
        mchoice = make_choice(["Vse"] + sorted(USER.bookshelf.list_categories()), multi=True)
        FILTER_CATEGORY = [] if "Vse" in mchoice else mchoice
        set_filters()
    elif choice == "Nastavi stanje knjige":
        print("Katere vrste knjig želite?")
        mchoice = make_choice(["Vse", "Nezačete", "Začete", "Prebrane"], multi=True)
        FILTER_READING  = [] if "Vse" in mchoice else [reading_level[i] for i in mchoice]
        set_filters()
    elif choice == "Nazaj":
        pass

def book_editor(book_title):
    book = USER.bookshelf.get_book(book_title)
    print(book_title)
    print("Kaj želite urediti?")
    choices = ["Naslov", "Strani", "Avtor", "Kategorija", "nazaj"]
    choice = make_choice(choices)
    if choice == "Naslov":
        print("Vnesite nov naslov knjige:")
        t = input("* ")
        book.update_title(t)
    elif choice == "Strani":
        print("Vnesite novo število strani:")
        new_pages = force_positive_integer()
        book.update_pages(new_pages)
    elif choice == "Avtor":
        print("Vnesite novega avtorja:")
        book.update_author(input("* "))
    elif choice == "Kategorija":
        print("Vnesite novo kategorijo:")
        book.update_category(input("* "))
    elif choice == "Nazaj":
        pass

def book_deleter(book_title):
    print(red("Ste prepričani da želite izbrisati knjigo " + book_title + "?"))
<<<<<<< HEAD
    print("Po izbrisu si ni mogoče premisliti.")
=======
    print("Po izbrisu se ni mogoče premisliti.")
>>>>>>> ed3c69fcfd501c994c7f853cafe6b96a26666463
    choice = make_choice(["Da", "Ne"])
    if choice == "Da":
        USER.bookshelf.remove_book(book_title)
        print("Izbrisano.")
<<<<<<< HEAD
        list_books()
    if choice == "Ne":
        print("Brisanje preklicano.")
        book_menu(book_title)
=======
    if choice == "Ne":
        print("Brisanje preklicano.")
>>>>>>> ed3c69fcfd501c994c7f853cafe6b96a26666463

def book_menu(book_title):
    reading_level = ["Nezačeta", "Začeta", "Prebrana"]
    book = USER.bookshelf.get_book(book_title)
    print(blue(book_title))
    book_statistics(book.title)
    print("Avtor: " + book.author)
    print("Kategorija: " + book.category)
    print("Stanje knjige: " + reading_level[book.state] + " (" + str(book.current_page) + "/" + str(book.pages) + ")")
    choice = make_choice(["Uredi podatke", "Zabeleži branje", "Izbriši knjigo", "Nazaj"])
    if choice == "Uredi podatke":
        book_editor(book.title)
        book_menu(book.title)
    elif choice == "Zabeleži branje":
        print("Koliko časa ste brali (v minutah)?")
        session_time = force_positive_integer()
        print("Do katere strani ste prišli?")
        new_current_page = force_positive_integer()
        book.new_session(session_time, new_current_page)
        book_menu(book.title)
    elif choice == "Izbriši knjigo":
        book_deleter(book_title)
    elif choice == "Nazaj":
        pass

def list_books():
    choice = make_choice(["Nazaj"] + sorted(USER.bookshelf.list_books(FILTER_AUTHOR, FILTER_CATEGORY, FILTER_READING)))
    if choice == "Nazaj":
        pass
    else:
        book_menu(choice)

def main_menu():
    book_number = USER.bookshelf.book_number(FILTER_AUTHOR, FILTER_CATEGORY, FILTER_READING) 
    if book_number != 0:
        list_filters()
    group_statistics(FILTER_AUTHOR, FILTER_CATEGORY, FILTER_READING)
    choice = make_choice(["Seznam knjig", "Dodaj knjigo", "Nastavi filtre"])
    if choice == "Seznam knjig":
        list_books()
    elif choice == "Dodaj knjigo":
        book_adder()
    elif choice == "Nastavi filtre":
        set_filters()


def main():
    print("Dobrodošli v Bralnem spremljevalcu.")
<<<<<<< HEAD
    print("Želite ustvariti novo knjižno polico ali naložiti obstoječo?")
=======
    print("Želite ustvariti novo knjižno polico ali naložiti obstoječo?""")
>>>>>>> ed3c69fcfd501c994c7f853cafe6b96a26666463
    init()
    while True:
        main_menu()

main()
