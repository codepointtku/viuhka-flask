from flask import Blueprint, render_template, send_from_directory
from app.services.models.category import sequalized_categories


module = Blueprint('index', __name__)

_name_ = 'Splash'


@module.route('/')
def index():
    return render_template('splash/index.html', categories=sequalized_categories())

@module.route('/info')
def info():  
    return render_template('splash/forms/info.html')

@module.route('/saavutettavuus')
def saavutettavuus():  
    return render_template('splash/forms/saavutettavuus.html')

@module.route('/provider_info')
def provider_info():  
    return render_template('splash/forms/provider_info.html')

