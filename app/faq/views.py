from flask              import render_template
from . import faq
import app

@faq.route('info', methods=['GET'])
def info():
    return render_template('faq.html')
   
@faq.route('starters', methods=['GET'])
def starters():
    return render_template('starters.html')
   
   
