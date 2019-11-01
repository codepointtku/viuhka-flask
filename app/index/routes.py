from flask import Blueprint, render_template, send_from_directory, request, redirect, url_for, abort
from app.services.models.category import sequalized_categories
from app.services.models.service import services_from_category, find_service
from app.services.models.category_items import get_category_item_by_name
from app.services.forms.service import ServiceForm
from flask_login import login_required

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

@module.route('/search', methods=['GET'])
def search():
    return redirect(url_for('index.index'))


@module.route('/details/<id>')
def details(id):
    if id:
        service = find_service(id)
        if service:
            return render_template('splash/actions/services/view.html', service=service)
    abort(404)