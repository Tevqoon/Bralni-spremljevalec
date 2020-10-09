import model

global FILENAME
global USER

def blue(string):
    return f'\033[1;94m{string}\033[0m'

def red(string):
    return f'\033[1;91m{string}\033[0m'

def save():
    pass

def make_choice(choices):
    while True:
        for n, c in enumerate(choices):
            print(str(n + 1) + ")" + c)
        choice = input("* ")
        if not(int(choice) & int(choice) > 0):
            print(red("Prosimo vnesite veljavno izbiro."))
        else:
            return choice

def init():
    print("""Pozdravljeni v knjižnem pomagaču. 
          Želite ustvariti novo knjižno polico ali naložiti obstoječo?""")
    load_init()

def load_init():
    choice = make_choice(["novo", "obstoječo"])
    if choice == "1":
        print("""Prosimo vnesite uporabniško ime. V tekstovnem vmesniku je geslo prazno.""")
        username = input("* ")
        print("""Prosimo vsenite ime datoteke, kamor boste
              shranili svoj račun.""")
        FILENAME = input("* ")
        USER = model.Account(username, "", model.Bookshelf())
        USER.save_state(FILENAME)
        print("""Hvala. Uživajte v uporabi.""")

    elif choice == "2":
        print("""prosimo vnesite ime datoteke, ki jo želite naložiti.""")
        FILENAME = input("* ")
        try:
            USER = model.Account.load_state(FILENAME)
        except FileNotFoundError:
            print(red("Neveljavno ime datoteke. Prosimo, poskusite še enkrat."))
            load_init()


def main():
    pass

init()


b1 = model.Book("Fenomenologija duha", 400, author="Hegel", category="Nonsens")
b2 = model.Book("Znanost logike", 200, author="Hegel", category="Logika", current_page=120, time_spent=160)
b3 = model.Book("Kritika čistega razuma", 700, author="Kant", category="Nonsens", current_page=432)

shelf = model.Bookshelf({b1, b2, b3})

jure = model.Account("Jure", "", shelf)
jure.save_state("jure.json")