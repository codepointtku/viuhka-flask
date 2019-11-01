from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, logout_user, login_user

from app.managers.password import generate_hash_pass

from app.utils.models import Account
from app.utils.extensions.database import module as connector

from app.admin.forms.login import LoginForm
from app.admin.forms.register import RegisterForm

import json

module = Blueprint('login_manager', __name__)

_name_ = 'Admin Login'


@module.route('/admin/login', methods=['POST', 'GET'])
def admin_login():
    print('Login request: %s' % request.method)
    if request.method == 'POST':
        form = LoginForm(request.form)

        account = Account.query.filter_by(username=form.username.data, password=generate_hash_pass(form.username.data, form.password.data)).first()
        if account:
            login_user(account)
            account.set_status(online=True).save()
            return redirect(url_for('admin.index'), code=302)
        else:
            return json.dumps(
                {
                    'success': False
                }
            ), 401, {'ContentType':'application/json'}
    else:
        if current_user.is_authenticated and current_user.is_staff():
            redirect(url_for('admin.index'))
            return json.dumps(
                {
                    'success': False
                }
            ), 302, {'ContentType':'application/json'}
        
        print('Rendering page')
        return render_template('admin/pages/login.html', form=LoginForm())


@module.route('/admin/logout', methods=['GET', 'POST'])
@login_required
def admin_logout():
    if not current_user.is_authenticated:
        return redirect(url_for('login_manager.admin_login'))
    current_user.online = 0
    current_user.save()
    logout_user()
    return redirect(url_for('admin.index'))


@module.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        form = LoginForm(request.form)

        account = Account.query.filter_by(username=form.username.data, password=generate_hash_pass(form.username.data, form.password.data)).first()
        if account:
            login_user(account)
            account.set_status(online=True).save()
            return redirect(url_for('index.index'), code=302)
        else:
            return json.dumps(
                {
                    'success': False
                }
            ), 401, {'ContentType':'application/json'}
    else:
        if current_user.is_authenticated and current_user.is_staff():
            redirect(url_for('index.index'))
            return json.dumps(
                {
                    'success': False
                }
            ), 302, {'ContentType':'application/json'}
        return render_template('splash/actions/login.html', form=LoginForm())


@module.route('/logout', methods=['GET', 'POST'])
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('login_manager.login'))
    current_user.online = 0
    current_user.save()
    logout_user()
    return redirect(url_for('index.index'))


@module.route('/register', methods=['GET', 'POST'])
def register():
    callback =  {
                    'success': True,
                    'form': '',
                    'errors': []
                }
    if current_user.is_authenticated:
        logout_user()                   # How did this happen..?
        return redirect('register')

    if request.method == 'POST':
        form = RegisterForm(request.form)
        username = form.username.data
        email = form.email.data

        if not username:
            callback['success'] = False
            callback['form'] = 'username'
            callback['errors'].append('Invalid username')
            return json.dumps(callback), 400, {'ContentType':'application/json'} 
        if not email:
            callback['success'] = False
            callback['form'] = 'email'
            callback['errors'].append('Invalid email')
            return json.dumps(callback), 400, {'ContentType':'application/json'} 



        account = Account.query.filter_by(email=email).first()
        if account:
            callback['success'] = False
            callback['form'] = 'email'
            callback['errors'].append('Email already registered')
            return json.dumps(callback), 400, {'ContentType':'application/json'} 


        account = Account.query.filter_by(username=form.username.data).first()
        if account:
            callback['success'] = False
            callback['form'] = 'username'
            callback['errors'].append('Username already registered')
            return json.dumps(callback), 400, {'ContentType':'application/json'} 



        password = generate_hash_pass(username, form.password.data)
        account = Account(
            username = username,
            password = password,
            email = email
        )
        account = account.save()
        account.change_rank(
            level=1
        )
        account = Account.query.filter_by(username=username, password=password, email=email).first()
        if account:
            return json.dumps(callback), 200, {'ContentType':'application/json'}
        else:
            return json.dumps(
                {
                    'success': False
                }
            ), 401, {'ContentType':'application/json'}
    else:
        return render_template('splash/actions/register.html')