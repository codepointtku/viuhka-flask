from wtforms_alchemy import ModelForm, QuerySelectMultipleField
from wtforms import SelectMultipleField, IntegerField
from wtforms.fields.html5 import DateTimeLocalField

from wtforms.validators import Required

from ..models.service import Service

class ServiceForm(ModelForm):
    category_items              =   SelectMultipleField('Category Items', choices=[])
    
    search_result_priority      =   IntegerField(label="Search result priority")
    start                       =   DateTimeLocalField(label="Start", format='%Y-%m-%dT%H:%M', validators=[Required()])
    end                         =   DateTimeLocalField(label="End",   format='%Y-%m-%dT%H:%M', validators=[Required()])

    class Meta:
        model = Service
        exclude = [
            'category_items'
        ]