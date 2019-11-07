from flask import Blueprint, render_template, request, redirect, Response, url_for
from flask_login import login_required
from flask_wtf.csrf import validate_csrf

from app.services.models.service import ( Service, get_services, find_service, 
                                        amount, create_new )
from app.services.forms.service import ServiceForm
from app.services.models.category import get_category, sequalized_categories

from app.utils import root, join, exit, paginate

from wtforms.fields.simple import TextAreaField

import json
import pickle

module = Blueprint('service', __name__)

_name_ = 'Services'


@module.route('/service/list', methods=['GET'])
def list_service():
    page = request.args.get('page', 1, int)
    services = paginate(Service.query, page=page, per_page=25)
    return render_template('splash/actions/services/list.html', services=services, amount=amount)


@module.route('/admin/service', methods=['GET', 'POST'])
@login_required
def service():
    _type = str(request.args.get('type'))
    id = request.args.get('id') 
    if _type == 'edit':
        if request.method == 'GET':
            if id == 0:
                return redirect(url_for('service.services'))
            service = find_service(id)
            if service:
                form = ServiceForm()
                try:    
                    form.category_items.process_data([v for v in service.category_items.values()])
                except:
                    form.category_items.process_data([] if service.category_items is None else service.category_items)

                for ff in form.__dict__:
                    for sf in service.__dict__:
                        if ff == sf:
                            if isinstance(form.__dict__[ff], TextAreaField):
                                form.__dict__[ff].process_data(service.__dict__[sf])
                try:
                    if service.start:          form.start.data = str(service.start).replace(' ','T')
                    if service.end:            form.end.data = str(service.end).replace(' ','T')
                except:
                    pass

                return render_template('admin/pages/services/_edit.html', service=service, form=form, categories=sequalized_categories)
            return render_template('admin/pages/404.html', reason='Service', content='Not found')
        else:
            form = ServiceForm(request.form)
            service = find_service(id)
            if form.start.data is None and service.start is not None:
                form.start.data = service.start
            if form.end.data is None and service.end is not None:
                form.end.data = service.end

            service.__init__(**form.data)
            validate_csrf(service.csrf_token)
            service.save()
            try:
                if find_service(service.id):
                    return json.dumps({
                            'success': True
                        }), 200, {'ContentType':'application/json'}
            except:
                pass
            return json.dumps({
                    'success': False
                }), 400, {'ContentType':'application/json'}
            
    elif _type == 'add':
        form = ServiceForm(request.form)
        service = Service(
            form=form.data,
            start=form.start.data,
            end=form.end.data
        )
        validate_csrf(service.csrf_token)
        try: service.category_items = dict(enumerate(service.category_items))
        except: pass
        service.save()
        try:
            if find_service(service.id):
                return json.dumps({
                        'success': True,
                        'service_id': str(service.id)
                    }), 200, {"ContentType":"Application/Json"}
        except:
            pass
        return json.dumps({
            'success':False,
        }), 400, {'ContentType':'application/json'}
    elif _type == 'new':
        if request.method == 'GET':
            return render_template('admin/pages/services/_new.html', form=ServiceForm(), categories=sequalized_categories)
        return redirect(url_for('service.services'))
    elif _type == 'delete':
        if id == 0:
            return redirect(url_for('service.services'))
        service = find_service(id)
        if service:
            service.delete()
    return redirect(url_for('service.services'))

@module.route('/admin/services', methods=['GET'])
@login_required
def services():
    page = request.args.get('page', 1, int)
    services = paginate(Service.query, page=page, per_page=25)
    return render_template('admin/pages/services/services.html', 
                        services=services, amount=amount)