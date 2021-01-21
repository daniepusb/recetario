from flask import Blueprint

faq = Blueprint('faq', __name__, url_prefix='/faq')

from . import views