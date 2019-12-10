from random                         import randint

from flask_login                    import UserMixin
from sqlalchemy                     import func

from app.utils.extensions.database  import module as connector
from app.utils.models.rank          import Rank, get_object
from app.managers.password          import generate_hash_pass, validate_hash_pass

class Account(UserMixin, connector.Model):
    __tablename__                           = 'account'
    
    id                                      = connector.Column(connector.Integer, primary_key=True, autoincrement=True)
    username                                = connector.Column(connector.String(32))
    email                                   = connector.Column(connector.String(100))
    password                                = connector.Column("sha_pass_hash", connector.String(40))
    online                                  = connector.Column("online", connector.Integer, primary_key=True)
    is_active                               = connector.Column("active", connector.Boolean)


    def __init__(self, *args, **kwargs):
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.online = kwargs.get('online') if kwargs.get('online') is not None else 0
        self.is_active = True

    
    def __str__(self):
        return self.username


    def __repr__(self):
        return "<Account %r>" % self.id

    def set_status(self, online):
        if online:
            self.online = 1
            return self
        self.online = 0
        return self

    def validate(self, password):
        return validate_hash_pass(password)

    def save(self):
        connector.session.add(self)
        connector.session.commit()
        return self
    
    def delete(self):
        self.rank().delete()
        connector.session.delete(self)
        connector.session.commit()

    def is_staff(self):
        return self.rank().level >= 1
    
    def rank(self):
        rank = get_object(self.id)
        if rank:
            return rank
        return Rank(
                id=self.id,
                level=0
        ).save()
    
    def change_rank(self, level):
        rank = self.rank()
        if level >= self.rank().level:
            return self
        rank.level = level
        rank.save()
        return self



def find_account(id):
    return Account.query.filter(Account.id==id).first()

def find_account_by_username(name):
    return Account.query.filter(func.upper(Account.username) == func.upper(name)).first()

def find_account_by_email(email):
    return Account.query.filter(func.upper(Account.email) == func.upper(email)).first()

def list_accounts():
    return Account.query.all()

def amount():
    return len(Account.query.all())