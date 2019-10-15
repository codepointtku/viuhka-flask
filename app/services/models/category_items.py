from app.utils.extensions.database import module as connector



class CategoryItems(connector.Model):
    __table_args__      = {
                            'extend_existing': True
                        } 


    id          = connector.Column(connector.Integer, primary_key=True)
    category_id = connector.Column(connector.Integer)
    text        = connector.Column(connector.String(100))

    def __str__(self):
        return self.text

    def __init__(self, category_id, text):
        self.id = amount() + 1
        self.category_id = category_id
        self.text = text
    
    def save(self):
        connector.session.add(self)
        connector.session.commit()
        return self

    def delete(self):
        connector.session.delete(self)
        connector.session.commit()


def get_relation_type(category_id):
    query = CategoryItems.query.filter_by(category_id=category_id).all()
    return query if query else []

def amount():
    return len(CategoryItems.query.all())


def get_category_item_by_name(name):
    return CategoryItems.query.filter_by(text=name).first()

