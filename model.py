import datetime

class Book:
    def __init__(self, title, pages, current_page=1, author="", category="", time_spent=0, state=0, sessions=[]):
        self.title = title
        self.pages = pages
        self.current_page = current_page
        self.author = author
        self.category = category
        self.time_spent = time_spent
        self.state = 0 
# 0 = not reading, 1 = reading, 2 = finished
        self.sessions = sessions

    def update_state(self, new_state):
        self.state = new_state

    def new_session(self, session_time, final_page):
        self.time_spent += session_time
        if final_page >= self.pages:
            self.state = 2
        elif final_page > 1:
            self.state = 1
        self.page = min(final_page, self.pages)
        self.sessions.append((session_time, final_page))

