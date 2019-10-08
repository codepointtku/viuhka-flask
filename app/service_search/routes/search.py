from flask import Blueprint, render_template
from app.admin.models.service import Service, get_services, find_service, amount



module = Blueprint('search', __name__)


_name_ = 'Search'



@module.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('splash/actions/search/search.html', services=get_services, amount=amount)

@module.route('/search/<id>', methods=['GET', 'POST'])
def search_id(id):
    return render_template('splash/actions/search/modal.html', service=find_service(id))