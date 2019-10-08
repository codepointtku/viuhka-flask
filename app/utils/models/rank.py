from app.utils.extensions.database import module as connector

ranks = {
    0: 'Asiakas',
    1: 'Virkailija',
    2: 'Admin'
}


class Rank(connector.Model):
    __tablename__                           = 'rank'

    id                                      = connector.Column(connector.Integer, primary_key=True)
    level                                   = connector.Column(connector.Integer)

    def __init__(self, id, level):
        self.id = id
        self.level = level

    def __str__(self):
        return ranks[self.level]

    def save(self):
        connector.session.add(self)
        connector.session.commit()
        return self
    
    def name(self):
        if self.level > 2:
            self.level = 2
        return ranks[self.level]



def get_object(account_id):
    return Rank.query.filter_by(id=account_id).first()