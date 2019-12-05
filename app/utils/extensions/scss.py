#ignore

from flask import Blueprint
from sassutils.wsgi import SassMiddleware


module = Blueprint('scss', __name__)

_name_ = 'SCSS Loader'