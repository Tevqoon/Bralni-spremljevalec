import bottle, model, datetime, os, hashlib

accounts = {}
secret = "fruit juice runs through my veins"
filter_authors = []
filter_categories = []
filter_bookstates = []
tab_keys = {"Avtorji" : "authors", "Kategorije" : "categories", "Stanje" : "reading_states"}


if not os.path.isdir("shelves"):
    os.mkdir("shelves")

for file in os.listdir("shelves"):
    acc = model.Account.load_state(os.path.join("shelves", file))
    accounts[acc.username] = acc

def current_user_account():
    name = bottle.request.get_cookie("name", secret=secret)
    if name is None:
        bottle.redirect("/login/")
    return accounts.get(name, None)

def user_shelf():
    return current_user_account().bookshelf

def save_current_account():
    account = current_user_account()
    account.save_state(os.path.join("shelves", account.username + ".json"))

@bottle.get("/")
def start_page():
    if current_user_account() == None:
        bottle.redirect("/login/")
    else:
        bottle.redirect("/library/")

@bottle.get("/login/")
def login_get():
    return bottle.template("login.html")

@bottle.post("/login/")
def login_post():
    username = bottle.request.forms.getunicode("name")
    password = bottle.request.forms.getunicode("password")
    if username == None or password == None:
        bottle.redirect("/loginfail/")
    code = hashlib.sha256()
    code.update(password.encode(encoding="UTF-8"))
    codedpass = code.hexdigest()
    acc = accounts.get(username, None)
    if bottle.request.forms.getunicode("register") == "Registracija":
        if acc != None:
            bottle.redirect("/loginfail/")
        else:
            new_acc = model.Account(username, codedpass, bookshelf=model.Bookshelf())
            accounts[new_acc.username] = new_acc
            bottle.response.set_cookie("name", new_acc.username, path='/', secret=secret)
            save_current_account()
    if bottle.request.forms.getunicode("login") == "Prijava":
        if acc == None:
            bottle.redirect("/loginfail/")
        elif acc.authenticate(codedpass):
            bottle.response.set_cookie("name", acc.username, path='/', secret=secret)
        else:
            bottle.redirect("/loginfail/")
    bottle.redirect("/")

@bottle.get("/loginfail/")
def loginfail_get():
    return bottle.template("fail_login.html")

@bottle.post("/logout/")
def logout_get():
    bottle.response.delete_cookie("name", path="/")
    bottle.redirect("/login/")
        
@bottle.get("/library/")
def library_main():
    return library_book(None)

@bottle.post("/library/")
def library_post_no_selection():
    return library_filter_updates(None)

@bottle.get("/library/<title>/")
def library_book(title):
    tab_keys = {"Avtorji" : "authors", 
                "Kategorije" : "categories", 
                "Stanje" : "reading_states"}
    chosen_tab = bottle.request.query["tabc"]
    if chosen_tab == None:
        chosen_tab = "Avtorji"
    return bottle.template("library.html", 
                            username=current_user_account().username, 
                            shelf=user_shelf(), 
                            selected=title, 
                            active_authors=filter_authors, 
                            active_categories=filter_categories, 
                            active_bookstates=filter_bookstates, 
                            selected_filter_tab=tab_keys[chosen_tab])

@bottle.post("/library/<title>/")
def library_filter_updates(title):
    stats = (title == ("stats")) #to see where to redirect
    global filter_authors
    global filter_categories
    global filter_bookstates
    all_auths = user_shelf().list_authors()
    all_cats = user_shelf().list_categories()
    all_states = ["Nezačete", "Začete", "Prebrane"]
    chosen_tab = bottle.request.query["tabc"]
    if chosen_tab == None:
        chosen_tab = "Avtorji"

    if chosen_tab == "Avtorji":
        auths = []
        for a in all_auths:
            a = a.replace(" ", "%")
            ahat = a.replace("č", "c").replace("š", "s").replace("ž", "z")
            if bottle.request.forms.getunicode(ahat) == ahat:
                auths.append(a.replace("%", " "))
        filter_authors = auths
    elif chosen_tab == "Kategorije":
        cats = []
        for c in all_cats:
            c = c.replace(" ", "%")
            chat = c.replace("č", "c").replace("š", "s").replace("ž", "z")
            if bottle.request.forms.getunicode(chat) == chat:
                cats.append(c.replace("%", " "))
        filter_categories = cats
    elif chosen_tab == "Stanje":
        states = []
        for s in all_states:
            shat = s.replace("č", "c").replace("š", "s").replace("ž", "z")
            if bottle.request.forms.getunicode(shat) == shat:
                states.append(s)
        filter_bookstates = states
    reset = bottle.request.forms.getunicode("reset_filters")
    if reset:
        filter_authors = []
        filter_categories = []
        filter_bookstates = []
    if stats:
        return bottle.template("bookstats.html", 
                               username=current_user_account().username, 
                               shelf=user_shelf(), 
                               active_authors=filter_authors, 
                               active_categories=filter_categories, 
                               active_bookstates=filter_bookstates, 
                               selected_filter_tab=tab_keys[chosen_tab])
    else:
        return bottle.template("library.html", 
                               username=current_user_account().username, 
                               shelf=user_shelf(), 
                               selected=title, 
                               active_authors=filter_authors, 
                               active_categories=filter_categories, 
                               active_bookstates=filter_bookstates, 
                               selected_filter_tab=tab_keys[chosen_tab])

@bottle.get("/addread/<title>/")
def get_add_read(title):
    return bottle.template("add_read.html", 
                           username=current_user_account().username, 
                           selected=title)

@bottle.post("/addread/<title>/")
def post_add_read(title):
    if bottle.request.forms.getunicode("cancel"):
        bottle.redirect("/library/" + title + "/")
    reading_time = bottle.request.forms.getunicode("time")
    final_page = bottle.request.forms.getunicode("page")
    # Get data by POST
    if reading_time.isnumeric() and final_page.isnumeric(): # Check validity
        book = user_shelf().get_book(title.replace("%", " "))
        book.new_session(int(reading_time), int(final_page))
        save_current_account()
        bottle.redirect("/library/" + title + "/")
        # Add reading session and redirect
    else: # In case of fail, redirect to failing page
        return bottle.template("fail_readadd.html", 
                               username=current_user_account().username, 
                               selected=title)

@bottle.get("/deleter/<title>/")
def get_deleter(title):
    return bottle.template("book_deleter.html", 
                           username=current_user_account().username, 
                           selected=title)

@bottle.post("/deleter/<title>/")
def post_deleter(title):
    if bottle.request.forms.getunicode("cancel"):
        bottle.redirect("/library/" + title + "/")
    elif bottle.request.forms.getunicode("confirm"):
        user_shelf().remove_book(title)
        save_current_account()
        bottle.redirect("/library/")
        
@bottle.get("/addbook/")
def get_bookadd():
    return bottle.template("book_adder.html", 
                           username=current_user_account().username)

@bottle.post("/addbook/")
def post_bookadd():
    if bottle.request.forms.getunicode("cancel"):
        bottle.redirect("/library/")
    title = bottle.request.forms.getunicode("book_title")
    pages = bottle.request.forms.getunicode("pages")
    current_page = bottle.request.forms.getunicode("current_page")
    author = bottle.request.forms.getunicode("author")
    category = bottle.request.forms.getunicode("category")
    time_spent = bottle.request.forms.getunicode("time_spent")
    # Grab data by POST
    if not((title or pages) 
           and (current_page.isnumeric() or current_page == "") 
           and (time_spent.isnumeric() or time_spent == "")):
        return bottle.template("fail_addbook.html", 
                               username = current_user_account().username)
    # Check validity of data
    pages = int(pages)
    current_page = 0 if current_page == "" else int(current_page)
    time_spent = 0 if time_spent == "" else int(time_spent)
    if current_page > pages:
        current_page = pages
    # Convert numeric data into numbers
    book = model.Book(title, pages, 
                      current_page, author, 
                      category, time_spent)
    # Create a new book object with said data
    user_shelf().add_book(book)
    save_current_account()
    bottle.redirect("/library/")
    # Add the new book to user's library and redirect.

@bottle.get("/editbook/<title>/")
def get_editbook(title):
    book = user_shelf().get_book(title.replace("%", " "))
    return bottle.template("book_editor.html", 
                           username=current_user_account().username,
                           selected=title, book=book)

@bottle.post("/editbook/<title>/")
def post_editbook(title):
    if bottle.request.forms.getunicode("cancel"):
        bottle.redirect("/library/" + title + "/")
    new_title = bottle.request.forms.getunicode("book_title")
    pages = bottle.request.forms.getunicode("pages")
    current_page = bottle.request.forms.getunicode("current_page")
    author = bottle.request.forms.getunicode("author")
    category = bottle.request.forms.getunicode("category")
    time_spent = bottle.request.forms.getunicode("time_spent")
    # Grab data by POST 
    if not((pages.isnumeric() or pages == "")
            and (current_page.isnumeric() or current_page == "") 
            and (time_spent.isnumeric() or time_spent == "")):
        return bottle.template("fail_edit.html", 
                               username=current_user_account().username,
                               selected=title)
    # Check validity of data
    book = user_shelf().get_book(title.replace("%", " "))
    if new_title != "":
        title = new_title.replace(" ", "%")
        book.update_title(new_title)
    if pages != "":
        book.update_pages(int(pages))
    if author != "":
        book.update_author(author)
    if category != "":
        book.update_category(category)
    if current_page != "":
        book.update_current_page(int(current_page))
    if time_spent != "":
        book.update_time_spent(int(time_spent))
    # If a value is to be changed, update the given argument
    save_current_account()
    bottle.redirect("/library/" + title + "/")
    # Save account and redirect

@bottle.get("/bookstats/")
def get_stats():
    chosen_tab = bottle.request.query["tabc"]
    if chosen_tab == None:
        chosen_tab = "Avtorji"
    return bottle.template("bookstats.html", 
                        username=current_user_account().username, 
                        shelf=user_shelf(), 
                        active_authors=filter_authors, 
                        active_categories=filter_categories, 
                        active_bookstates=filter_bookstates, 
                        selected_filter_tab=tab_keys[chosen_tab])

@bottle.post("/bookstats/")
def stats_filter_updates():
    return library_filter_updates(("stats"))

bottle.run()