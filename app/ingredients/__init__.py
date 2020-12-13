from flask import Blueprint

ingredients = Blueprint('ingredients', __name__, url_prefix='/ingredients')

from . import views