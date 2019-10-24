from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user

from app.utils.models.account import list_accounts, find_account, Account, amount, find_account_by_username, find_account_by_email
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
    print(_type, id)
    if _type == 'edit':
        if id == 0:
            return redirect(url_for('account.accounts'))
        account = find_account(id)
        if account:
            print('Editing account (%s) %s, request by: %s' % (account.id, account.username, current_user.username))
            return render_template('admin/pages/accounts/account.html', account=account, form=AccountForm(), render_type='edit', redirect=redirect)
        else:
            return render_template('admin/pages/404.html', reason='Account', content='Not found')
    elif _type == 'add':
        form = AccountForm(request.form)
        
        if not form.username.data or form.username.data is None or len(form.username.data) < 3:
            return json.dumps({
                'success':False,
                'message':'Invalid username value'
            }), 400, {'ContentType':'application/json'}

        if not form.password.data or form.password.data is None or len(form.password.data) < 6:
            return json.dumps({
                'success':False,
                'message':'Invalid password value'
            }), 400, {'ContentType':'application/json'}

        if not form.email.data or form.email.data is None or len(form.email.data) < 6:
            return json.dumps({
                'success':False,
                'message':'Invalid email value'
            }), 400, {'ContentType':'application/json'}

        
        account = find_account_by_username(form.username.data) or find_account_by_email(form.email.data)
        if account:
            return json.dumps({
                'success':False,
                'message':'Account already exists.'
            }), 400, {'ContentType':'application/json'}

        account = Account(
            username=form.username.data,
            password=generate_hash_pass(username=form.username.data, password=form.password.data),
            email=form.email.data,
            online=0
        )
        account.change_rank(
            level=int(form.rank.data)
        )
        account.save()
        return json.dumps({
            'success':True
        }), 200, {'ContentType':'application/json'}
    elif _type == 'new':
        return render_template('admin/pages/accounts/account.html', form=AccountForm(), ranks=ranks, render_type='new')
    elif _type == 'delete':
        account = find_account(id)
        if account:
            print('Username: %s' % account.username)
            account.delete()
            return redirect(url_for('account.accounts'))
        else:
            return json.dumps({
                'success':False,
                'message':'Account not found.'
            }), 400, {'ContentType':'application/json'}

    else:
        return redirect(url_for('account.accounts'))
