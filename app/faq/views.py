from flask              import render_template, session
from . import faq
import app

@faq.route('info', methods=['GET'])
def info():
    context = {}
    if session.get('admin'):
        context = {'admin' :session['admin'] }
    return render_template('faq.html', **context)


@faq.route('terms', methods=['GET'])
def termsAndConditions():
    if session.get('admin'):
        context = {'admin' :session['admin'] }
    return render_template('faq_terms_and_conditions.html')
   