from flask import Blueprint, render_template, request, redirect, Response, url_for
from flask_login import login_required

from app.services.models.service import ( Service, get_services, find_service, 
                                        amount, get_fields, normalize, create_new, 
                                        bool_types, int_types, date_types )
from app.services.forms.service import ServiceForm
from app.services.models.category import get_category, sequalized_categories

from app.utils import root, join, exit

import json
import pickle

module = Blueprint('service', __name__)

_name_ = 'Services'


@module.route('/service/list', methods=['GET'])
def list_service():
    return render_template('splash/actions/services/list.html', services=get_services, amount=amount, fields=get_fields(), normalized_fields=normalize(get_fields()))


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

                if service.organization:   form.organization.process_data(     service.organization)
                if service.ingress:        form.ingress.process_data(          service.ingress)
                if service.description:    form.description.process_data(      service.description)
                if service.description2:   form.description2.process_data(     service.description2)
                if service.description3:   form.description3.process_data(     service.description3)
                if service.description4:   form.description4.process_data(     service.description4)
                if service.provider:       form.provider.process_data(         service.provider)
                if service.benefit_effect: form.benefit_effect.process_data(   service.benefit_effect)
                if service.constraint:     form.constraint.process_data(       service.constraint)
                if service.notes:          form.notes.process_data(            service.notes)


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
            service.save()
            return json.dumps(
                {
                    'success':True
                }
            ), 200, {'ContentType':'application/json'}
    elif _type == 'add':
        form = ServiceForm(request.form)
        service = Service(
            form=form.data,
            start=form.start.data,
            end=form.end.data
        )
        try: service.category_items = dict(enumerate(service.category_items))
        except: pass
        service.save()
        return json.dumps(
            {
                'success':True,
                'service_id': str(service.id)
            }
        ), 200, {"ContentType":"Application/Json"}
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
    return render_template('admin/pages/services/services.html', 
                        services=get_services, amount=amount, fields=get_fields(), normalized_fields=normalize(get_fields()),
                        int_types=int_types, date_types=date_types, bool_types=bool_types)