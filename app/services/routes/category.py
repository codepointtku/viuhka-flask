from flask                                  import Blueprint, render_template, request, redirect, url_for
from flask_login                            import login_required
from flask_wtf.csrf                         import validate_csrf

from app.services.models.category           import sequalized_categories, get_category, get_category_by_name, amount, Category
from app.services.models.category_items     import CategoryItems, get_category_item_by_name
from app.services.forms.category            import CategoryForm

import json


module = Blueprint('category', __name__)

_name_ = 'Categories'

@module.route('/admin/category', methods=['GET', 'POST'])
@login_required
def category():
    _type = request.args.get('type')
    id = request.args.get('id')
    if _type == 'edit':
        if request.method == 'GET':
            category = sequalized_categories(id)
            if category:
                return render_template('admin/pages/categories/_edit.html', category=category, form=CategoryForm())
            return render_template(url_for('category.categories'))
        else:
            form = CategoryForm(request.form)
            cat = get_category(form.id.data)
            del form.id
            category_items = form.category_items.data
            del form.category_items
            if cat:
                cat.__init__(**form.data)
            else:
                cat = Category(**form.data)
            validate_csrf(cat.csrf_token)
            cat.save()
            return json.dumps(
                {
                    'success':True
                }
            ), 200, {'ContentType':'application/json'}
    elif _type == 'new':
        if request.method == 'GET':
            return render_template('admin/pages/categories/_new.html', form=CategoryForm(), render_type='new')
        else:
            form = CategoryForm(request.form)
            del form.id
            category_items = form.category_items.data
            del form.category_items
            cat = Category(
                **form.data
            )
            cat.save()
            for item in category_items:
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
    if _type == 'add':
        cat = CategoryItems(
            category_id=id,
            text=request.form.get('text')
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