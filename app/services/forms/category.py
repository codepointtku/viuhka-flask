from wtforms_alchemy import ModelForm, QuerySelectMultipleField
from wtforms import StringField, SelectMultipleField

from app.services.models.category import Category
from app.services.models.category_items import CategoryItems


class CategoryForm(ModelForm):
    text = StringField()
    category_items = SelectMultipleField('Category Items', choices=[])

    class Meta:
        model = Category
    

