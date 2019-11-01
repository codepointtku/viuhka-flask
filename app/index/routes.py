from flask import Blueprint, render_template, send_from_directory, request, redirect, url_for
from app.services.models.category import sequalized_categories
from app.services.models.service import services_from_category
from app.services.models.category_items import get_category_item_by_name
from app.services.forms.service import ServiceForm
from flask_login import login_required

from app.services.models.service import ( Service, get_services, find_service, 
                                        amount, get_fields, normalize, create_new, 
                                        bool_types, int_types, date_types )
from app.services.models.category import get_category, sequalized_categories

from app.utils import root, join, exit

import json
import pickle


module = Blueprint('index', __name__)

_name_ = 'Splash'


@module.route('/')
def index():
    _type = request.args.get('type')
    if _type is None or _type is not 'show':
        return render_template('splash/index.html', categories=sequalized_categories(), services=services_from_category())
    else:
        id = request.json.get('categoryname')
        return render_template('splash/index.html', categories=sequalized_categories(), services=services_from_category(id))

@module.route('/info')
def info():  
    return render_template('splash/forms/info.html')

@module.route('/saavutettavuus')
def saavutettavuus():  
    return render_template('splash/forms/saavutettavuus.html')

@module.route('/provider_info')
def provider_info():  
    return render_template('splash/forms/provider_info.html')

@module.route('/service')
def service():
    return redirect(url_for('index.index'))
    
@module.route('/form', methods=['GET', 'POST'])
@login_required
def form():  
    return render_template('splash/forms/form.html', form=ServiceForm()) 