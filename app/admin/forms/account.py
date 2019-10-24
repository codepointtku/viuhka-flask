from wtforms_alchemy import ModelForm
from wtforms import SelectField, SelectField
from app.utils.models.account import Account
from app.utils.models.rank import ranks

class AccountForm(ModelForm):
    rank                    =   SelectField('Rank', choices=tuple([(k, ranks[k]) for k in ranks]))

    class Meta:
        model = Account
