from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user


import json

from ..forms.login import LoginForm


module = Blueprint('admin', __name__)

_name_ = 'Flask Admin'



@module.route('/admin', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return render_template('admin/index.html')
    return redirect(url_for('login_manager.login'))