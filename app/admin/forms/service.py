from wtforms_alchemy import ModelForm, QuerySelectMultipleField
from wtforms import SelectMultipleField, IntegerField
from wtforms.fields.html5 import DateTimeLocalField

from wtforms.validators import Required

from ..models.service import Service
from ..models.relations import (ServicePath, Target, Study, Classification,
                                Immigration, AgeGroup, UnemploymentDuration,
                                Health, Integration)

class ServiceForm(ModelForm):
    category_items              = SelectMultipleField('Category Items', choices=[])
    
    search_result_priority      =   IntegerField(label="Search result priority")
    start                       =   DateTimeLocalField(label="Start", format='%H:%M %d/%m/%Y', validators=[Required()])
    end                         =   DateTimeLocalField(label="End",   format='%H:%M %d/%m/%Y', validators=[Required()])

    class Meta:
        model = Service
        exclude = [
            'service_path',
            'target',
            'study',
            'classification',
            'immigration',
            'age_group',
            'unemployment_duration',
            'health',
            'integration'
            ]