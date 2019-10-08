from flask import Blueprint, render_template, request, redirect, Response, url_for
from flask_login import login_required

from app.admin.models.service import ( Service, get_services, find_service, 
                                        amount, get_fields, normalize, create_new, 
                                        bool_types, int_types, pickle_types, date_types )

from app.admin.forms.service import ServiceForm

from app.utils import root, join, exit

import json

module = Blueprint('service', __name__)

_name_ = 'Services'


@module.route('/admin/service', methods=['GET', 'POST'])
@login_required
def service():
    _type = str(request.args.get('type'))
    id = request.args.get('id')
    if _type == 'edit':
        if id == 0:
            return redirect(url_for('service.services'))
        service = find_service(id)
        if service:
            return render_template('admin/pages/services/service.html', service=service, form=ServiceForm(), render_type='edit')
        else:
            return render_template('admin/pages/404.html', reason='Service', content='Not found')
    elif _type == 'add':
        print('we are in ADD but cannot redirect')
        form = ServiceForm(request.form)
        service = Service(
            form=form.data
        )
        service.save()
        return json.dumps(
            {
                'success':True,
                'service_id': str(service.id)
            }
        ), 200, {"ContentType":"Application/Json"}
    elif _type == 'new':
        if request.method == 'GET':
            return render_template('admin/pages/services/service.html', form=ServiceForm(), render_type='new')
        else:
            return redirect(url_for('service.services'))
    else:
        return redirect(url_for('service.services'))

@module.route('/admin/services', methods=['GET'])
@login_required
def services():
    return render_template('admin/pages/services/services.html', 
                        services=get_services, amount=amount, fields=get_fields(), normalized_fields=normalize(get_fields()),
                        int_types=int_types, pickle_types=pickle_types, date_types=date_types, bool_types=bool_types)