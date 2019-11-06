from wtforms_alchemy import ModelForm, QuerySelectMultipleField
from wtforms import StringField, SelectMultipleField, IntegerField
from flask_wtf import FlaskForm

from app.services.models.category import Category
from app.services.models.category_items import CategoryItems


class CategoryForm(ModelForm, FlaskForm):
    id                  = IntegerField()
    category_items      = SelectMultipleField('Category Items', choices=[])

    class Meta:
        model = Category
    

