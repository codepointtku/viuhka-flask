from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

from app.services.models.category import sequalized_categories, get_category, get_category_by_name, amount, Category
from app.services.models.category_items import CategoryItems, get_category_item_by_name
from app.services.forms.category import CategoryForm

import json


module = Blueprint('category', __name__)

_name_ = 'Categories'

@module.route('/admin/category', methods=['GET', 'POST'])
@login_required
def category():
    _type = request.args.get('type')
    id = request.args.get('id')
    if _type == 'edit':
        category = sequalized_categories(id)
        if category:
            return render_template('admin/pages/categories/_edit.html', category=category, form=CategoryForm())
        return render_template(url_for('category.categories'))
    elif _type == 'new':
        if request.method == 'GET':
            return render_template('admin/pages/categories/_new.html', form=CategoryForm(), render_type='new')
        else:
            form = CategoryForm(request.form)
            cat = Category(
                name = form.name.data
            )
            cat.save()
            for item in form.category_items.data:
                cat_items = CategoryItems(
                    category_id=cat.id,
                    text=item
                )
                cat_items.save()
            return json.dumps(
                {
                    'success':True
                }
            ), 200, {'ContentType': 'application/json' }
    elif _type == 'delete':
        category = get_category(id)
        if category:
            category.delete()
    return redirect(url_for('category.categories'))

@module.route('/admin/categories', methods=['GET'])
@login_required
def categories():
    return render_template('admin/pages/categories/categories.html', amount=amount, categories=sequalized_categories, len=len)




@module.route('/admin/category/item', methods=['POST', 'GET'])
@login_required
def category_item():
    _type = request.args.get('type')
    id = request.args.get('id')
    form = CategoryForm(request.form)
    if _type == 'add':
        cat = CategoryItems(
            category_id=id,
            text=form.text.data
        )
        cat.save()
        return json.dumps(
            {
                'success':True
            }
        ), 200, {'ContentType':'application/json'}
    elif _type == 'delete':
        for item in request.form.getlist('categoryItems[]'):
            cat = get_category_item_by_name(item)
            cat.delete()
        return json.dumps(
            {
                'success':True
            }
        ), 200, {'ContentType':'application/json'}
    return render_template(url_for('category.categories'))