from flask import Blueprint

vendors = Blueprint('vendors',  __name__, url_prefix='/vendors')

from . import views