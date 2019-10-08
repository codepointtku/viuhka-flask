from flask_login import AnonymousUserMixin

class AnonymousUser(AnonymousUserMixin):
    def __init__(self, username = 'Guest'):
        self.username = username

    def is_staff(self):
        return False

    def __str__(self):
        return self.username