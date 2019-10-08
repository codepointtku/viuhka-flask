from flask import Blueprint, render_template, send_from_directory


module = Blueprint('index', __name__)

_name_ = 'Splash'


@module.route('/')
def index():
    return render_template('splash/index.html')