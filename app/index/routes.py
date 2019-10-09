from flask import Blueprint, render_template, send_from_directory


module = Blueprint('index', __name__)

_name_ = 'Splash'


@module.route('/')
def index():
    return render_template('splash/index.html')

@module.route('/info')
def info():  
    return render_template('splash/forms/info.html')


@module.route('/saavutettavuus')
def saavutettavuus():  
    return render_template('splash/forms/saavutettavuus.html')