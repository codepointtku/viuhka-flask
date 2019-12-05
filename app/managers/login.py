from flask_login                                import LoginManager, current_user
from app.utils.models.account                   import find_account
from app.admin.models.anonymoususer             import AnonymousUser





login_manager = LoginManager()

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(id):
    return find_account(id)