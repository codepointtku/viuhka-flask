from wtforms_alchemy                                import ModelForm, QuerySelectMultipleField
from wtforms                                        import SelectMultipleField, IntegerField, BooleanField
from wtforms.fields.html5                           import DateTimeLocalField

from wtforms.validators                             import Required

from flask_wtf                                      import Form

from ..models.service                               import Service

class ServiceForm(ModelForm, Form):
    category_items              =   SelectMultipleField('Category Items', choices=[])
    
    search_result_priority      =   IntegerField(label="Search result priority")
    start                       =   DateTimeLocalField(label="Start", format='%Y-%m-%dT%H:%M', validators=[Required()])
    end                         =   DateTimeLocalField(label="End",   format='%Y-%m-%dT%H:%M', validators=[Required()])
    published                   =   BooleanField(label="Published", default=False)
    open_ended                  =   BooleanField(label="Open ended", default=False)

    class Meta:
        model = Service
        exclude = [
            'category_items'
        ]