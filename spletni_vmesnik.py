import bottle, model, datetime, os, hashlib

accounts = {}
secret = "fruit juice runs through my veins"
filter_authors = []
filter_categories = []
filter_bookstates = []

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
        return bottle.template("library.html", username=current_user_account().username, shelf=user_shelf())

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
        
@bottle.get("/library/")
def library_main():
    return bottle.template("library.html", username=current_user_account().username, shelf=user_shelf(), active_authors=filter_authors, active_categories=filter_categories, active_bookstates=filter_bookstates,)

@bottle.get("/library/<title>/")
def library_book(title):
    tab_keys = {"Avtorji" : "authors", "Kategorije" : "categories", "Stanje" : "reading_states"}
    chosen_tab = bottle.request.query["tabc"]
    if chosen_tab == None:
        chosen_tab = "Avtorji"
    return bottle.template("library.html", username=current_user_account().username, shelf=user_shelf(), selected=title, active_authors=filter_authors, active_categories=filter_categories, active_bookstates=filter_bookstates, selected_filter_tab=tab_keys[chosen_tab])

@bottle.get("/library/<title>/<test>/")
def test(title, test):
    print(test)
    bottle.redirect("/library/" + title + "/")

@bottle.post("/library/<title>/")
def library_filter_updates(title):
    global filter_authors
    global filter_categories
    global filter_bookstates
    tab_keys = {"Avtorji" : "authors", "Kategorije" : "categories", "Stanje" : "reading_states"}
    all_auths = user_shelf().list_authors()
    all_cats = user_shelf().list_categories()
    all_states = ["Nezačete", "Začete", "Prebrane"]
    chosen_tab = bottle.request.query["tabc"]
    if chosen_tab == None:
        pass
    elif chosen_tab == "Avtorji": #TODO: Fix authors/categories with spaces
        auths = []
        for a in all_auths:
            a = a.replace(" ", "%")
            print(a)
            print(bottle.request.forms.getunicode(a))
            if bottle.request.forms.getunicode(a) == a:
                auths.append(a.replace("%", " "))
        filter_authors = auths
    elif chosen_tab == "Kategorije":
        cats = []
        for c in all_cats:
            c = c.replace(" ", "%")
            if bottle.request.forms.getunicode(c) == c:
                cats.append(c.replace("%", " "))
        filter_categories = cats
    elif chosen_tab == "Stanje":
        states = []
        for s in all_states:
            print(bottle.request.forms.getunicode(s))
            if bottle.request.forms.getunicode(s) == s:
                states.append(s)
        filter_bookstates = states
    reset = bottle.request.forms.getunicode("reset_filters")
    if reset:
        filter_authors = []
        filter_categories = []
        filter_bookstates = []
    
    return bottle.template("library.html", username=current_user_account().username, shelf=user_shelf(), selected=title, active_authors=filter_authors, active_categories=filter_categories, active_bookstates=filter_bookstates, selected_filter_tab=tab_keys[chosen_tab])
    
@bottle.get("/addread/<title>/")
def get_add_read(title):
    return bottle.template("add_read.html", username=current_user_account().username, selected=title)

@bottle.get("/loginfail/")
def loginfail_get():
    return bottle.template("fail_login.html")

@bottle.post("/logout/")
def logout_get():
    bottle.response.delete_cookie("name", path="/")
    bottle.redirect("/login/")


bottle.run(debug=True, reloader=True)