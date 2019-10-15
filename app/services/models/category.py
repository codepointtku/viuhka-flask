from app.utils.extensions.database import module as connector
from app.services.models.category_items import get_relation_type

class CategorySequalizer:
    def __init__(self, id, category):
        self.category = category
        self.name = category.name
        self.items = []
        self.id = id

    def amount(self):
        return len(self.items)

class Category(connector.Model):
    __tablename__               = 'category'

    id                          = connector.Column(connector.Integer, primary_key=True, nullable=False)
    name                        = connector.Column(connector.String(100))


    def __init__(self, name):
        self.id = amount() + 1
        self.name = name
    
    def save(self):
        connector.session.add(self)
        connector.session.commit()
        return self

    def delete(self):
        connector.session.delete(self)
        connector.session.commit()


def get_categories():
    query = Category.query.all()
    return query if query else []


def get_category(id):
    return Category.query.filter_by(id=id).first()

def get_category_by_name(name):
    return Category.query.filter_by(name=name).first()


def amount():
    return len(Category.query.all())


def sequalized_categories(id=None):
    if id:
        category = get_category(id)
        cat = CategorySequalizer(category.id, category)
        items = get_relation_type(id)
        for item in items:
            cat.items.append(item)
        return cat
    else:
        seq = []
        categories = Category.query.all()
        for category in categories:
            cat = CategorySequalizer(category.id, category)
            items = get_relation_type(category.id)
            for item in items:
                cat.items.append(item)
            seq.append(cat)
        return seq