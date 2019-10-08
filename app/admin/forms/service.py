from wtforms_alchemy import ModelForm, QuerySelectMultipleField
from wtforms import SelectMultipleField, IntegerField

from ..models.service import Service
from ..models.relations import (ServicePath, Target, Study, Classification,
                                Immigration, AgeGroup, UnemploymentDuration,
                                Health, Integration)

class ServiceForm(ModelForm):
    service_path                =   QuerySelectMultipleField(
        'Service path',
        query_factory=lambda: ServicePath.query.all()
    )
    target                      =   QuerySelectMultipleField(
        'Target',
        query_factory=lambda: Target.query.all()
    )
    study                       =   QuerySelectMultipleField(
        'Study',
        query_factory=lambda: Study.query.all()
    )
    classification              =   QuerySelectMultipleField(
        'Classification',
        query_factory=lambda: Classification.query.all()
    )
    immigration                 =   QuerySelectMultipleField(
        'Immigration',
        query_factory=lambda: Immigration.query.all()
    )
    age_group                   =   QuerySelectMultipleField(
        'Age Group',
        query_factory=lambda: AgeGroup.query.all()
    )
    unemployment_duration       =   QuerySelectMultipleField(
        'Unemployment Duration',
        query_factory=lambda: UnemploymentDuration.query.all()
    )
    health                      =   QuerySelectMultipleField(
        'Health',
        query_factory=lambda: Health.query.all()
    )
    integration                 =   QuerySelectMultipleField(
        'Integration',
        query_factory=lambda: Integration.query.all()
    )
    
    search_result_priority      =   IntegerField(label="Search result priority")

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