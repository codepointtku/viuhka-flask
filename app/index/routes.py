from flask import Blueprint, render_template, send_from_directory, request, redirect, url_for, abort

from app.utils import paginate, paginate_id
from app.services.models.category import sequalized_categories
from app.services.models.service import Service, services_from_category, find_service, amount
from app.services.models.category_items import get_category_item_by_name
from app.services.forms.service import ServiceForm
from flask_login import login_required
from wtforms.fields.simple import TextAreaField

import json

module = Blueprint('index', __name__)

_name_ = 'Splash'


@module.route('/')
def index():
    _type = request.args.get('type')
    if _type is None or _type is not 'show':
        return render_template('splash/index.html', categories=sequalized_categories(), services=services_from_category(), total=amount())
    else:
        id = request.json.get('categoryname')
        return render_template('splash/index.html', categories=sequalized_categories(), services=services_from_category(id), total=amount())

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

@module.route('/edit/<id>', methods=['GET','POST'])
def edit(id):
    if request.method == 'GET':
        if id:
            service = find_service(id)
            if service:
                form = ServiceForm()
                for ff in form.__dict__:
                    for sf in service.__dict__:
                        if ff == sf:
                            if isinstance(form.__dict__[ff], TextAreaField):
                                form.__dict__[ff].process_data(service.__dict__[sf])
                return render_template('splash/actions/services/edit.html', service=service, form=form)
        return abort(404)
    else:
        form = ServiceForm(request.form)
        service = find_service(id)
        owner = service.owner_id

        category_items = service.category_items

        service.__init__(
            **form.data
        )
        service.category_items = category_items
        service.owner_id = owner
        service.save()
        if find_service(id):
            return json.dumps({
                'success':True
            }), 200, {'ContentType':'application/json'}
        return abort(400)
    
@module.route('/contact')
def contact():  
    return render_template('splash/forms/contact.html')
