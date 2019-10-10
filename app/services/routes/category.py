from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

from app.services.models.category import get_categories, get_category, get_category_by_name, amount



module = Blueprint('category', __name__)

_name_ = 'Categories'

@module.route('/admin/category', methods=['GET', 'POST'])
@login_required
def category():
    _type = request.args.get('type')
    id = request.args.get('id')
    if _type == 'edit':
        pass
    elif _type == 'new':
        pass
    elif _type == 'add':
        pass
    else:
        pass
    return redirect(url_for('category.categories'))

@module.route('/admin/categories', methods=['GET'])
@login_required
def categories():
    return render_template('admin/pages/categories/categories.html', amount=amount, categories=get_categories)