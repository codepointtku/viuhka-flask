from app.utils.extensions.database import module as connector
from app.services.models.category_items import get_relation_type

class CategorySequalizer:
    def __init__(self, id, category):
        self.category = category
        self.items = []
        self.id = id

class Category(connector.Model):
    __tablename__               = 'category'

    id                          = connector.Column(connector.Integer, primary_key=True, nullable=False)
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


def sequalized_categories():
    seq = []
    categories = Category.query.all()
    for category in categories:
        cat = CategorySequalizer(category.id, category)
        items = get_relation_type(category.id)
        print('Number of items in Category %s: %s' % (category.name, len(items)))
        for item in items:
            cat.items.append(item)
        print('\tNumber of items added to sequalized data: %s' % (len(cat.items)))
        seq.append(cat)
    return seq

