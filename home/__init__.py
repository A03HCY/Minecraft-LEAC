from flask import Blueprint

home_blue = Blueprint('home', __name__, url_prefix='/')

from . import views