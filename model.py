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
# 0 = not started, 1 = reading, 2 = finished
        self.sessions = sessions

    def update_state(self, new_state):
        self.state = new_state

    def new_session(self, session_time, final_page):
        self.time_spent += session_time
        if self.current_page >= self.pages:
            self.state = 2
            self.current_page = self.pages
        else:
            self.current_page = final_page
        self.sessions.append((session_time, final_page))