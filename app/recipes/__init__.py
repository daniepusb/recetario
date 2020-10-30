from flask import Blueprint

auth = Blueprint('recipes', __name__, url_prefix='/recipes')

from . import views