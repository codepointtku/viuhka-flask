from wtforms_alchemy import ModelForm
from wtforms import SelectField
from app.utils.models.account import Account
from app.utils.models.rank import ranks

class AccountForm(ModelForm):
    class Meta:
        model = Account
