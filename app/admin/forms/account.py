from wtforms_alchemy import ModelForm
from wtforms import SelectField, IntegerField
from flask_wtf import FlaskForm

from app.utils.models.account import Account
from app.utils.models.rank import ranks

class AccountForm(ModelForm, FlaskForm):
    id                      =   IntegerField('Id')
    rank                    =   SelectField('Rank', choices=tuple([(k, ranks[k]) for k in ranks]))

    class Meta:
        model = Account
