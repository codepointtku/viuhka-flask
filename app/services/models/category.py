from app.utils.extensions.database import module as connector



class Category(connector.Model):
    __tablename__               = 'category'

    id                          = connector.Column(connector.Integer, primary_key=True)
    name                        = connector.Column(connector.String(100))


def get_categories():
    query = Category.query.all()
    return query if query else []


def get_category(id):
    query = Category.query.filter_by(id=id).first()
    return query if query else []

def get_category_by_name(name):
    query = Category.query.filter_by(name=name).first()
    return query if query else []


def amount():
    return len(Category.query.all())