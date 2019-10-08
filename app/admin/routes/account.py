from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user

from app.utils.models.account import list_accounts, find_account, Account, amount
from app.utils.models.rank import ranks
from app.admin.forms.account import AccountForm
from app.managers.password import generate_hash_pass

import json

module = Blueprint('account', __name__)

_name_ = 'Accounts'


@module.route('/accounts', methods=['GET'])
@login_required
def accounts():
    if not current_user.is_staff() or not current_user.is_authenticated:
        return redirect('/')
    return render_template('admin/pages/accounts/accounts.html', accounts=list_accounts, find=find_account, amount=amount, ranks=ranks, form=AccountForm())


@module.route('/account/', methods=['GET', 'POST'])
@login_required
def account():
    _type = request.args.get('type')
    id = request.args.get('id')
    if _type == 'edit':
        if id == 0:
            return redirect(url_for('account.accounts'))
        account = find_account(id)
        if account:
            return render_template('admin/pages/accounts/account.html', account=account, form=AccountForm(), ranks=ranks, render_type='edit')
        else:
            return render_template('admin/pages/404.html', reason='Account', content='Not found')
    elif _type == 'add':
        form = AccountForm(request.form)

        print(request.form.get('selected'))

        account = Account(
            username=form.username.data,
            password=generate_hash_pass(username=form.username.data, password=form.password.data),
            email=form.email.data,
            online=0
        )
        account.change_rank(
            level=0
        )
        account.save()
        return redirect(url_for('account.account', type='edit', id=account.id))
    elif _type == 'new':
        return render_template('admin/pages/accounts/account.html', form=AccountForm(), ranks=ranks, render_type='new')
    else:
        return redirect(url_for('account.accounts'))
