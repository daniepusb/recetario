from flask import Blueprint

recipes = Blueprint('recipes', __name__, url_prefix='/recipes')

from . import views