from flask                              import Blueprint

module = Blueprint('javascripts', __name__)

_name_ = 'JSScripts'

@module.route('/getAmount')
def get_amount():
    return amount()