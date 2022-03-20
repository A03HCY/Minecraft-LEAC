from flask import Blueprint

api_blue = Blueprint('api', __name__, url_prefix='/api')

from . import views