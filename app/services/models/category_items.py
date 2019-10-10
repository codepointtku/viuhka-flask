from app.utils.extensions.database import module as connector



class CategoryItems(connector.Model):
    __table_args__      = {
                            'extend_existing': True
                        } 


    id      = connector.Column(connector.Integer, primary_key=True)
    category_id = connector.Column(connector.Integer, primary_key=True)
    text    = connector.Column(connector.String(100))

    def __str__(self):
        return self.text




def get_relation_type(category_id):
    query = CategoryItems.query.filter_by(category_id=category_id).all()
    return query if query else []


