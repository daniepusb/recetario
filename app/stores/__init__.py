from flask import Blueprint

stores = Blueprint('stores',  __name__, url_prefix='/stores')

from . import views