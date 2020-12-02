from flask import Flask
from flask import request, make_response, redirect, flash, session, url_for
from flask import render_template # allow to render from templates
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired
from flask_login import login_required, current_user

import qrcode # allow make qrCode
import unittest

from app import create_app

from app.common_functions import generarQR
from app.firestore_service import get_recipes, get_recipe, recipe_put, get_user

app = create_app()

todos       = ['Comprar cafe', 'Enviar solicitud de compra', 'Entregar video a productor ']
imgAddress  = 'assets/img/'
recipes     = ['Lemon Pie','Tres Leches','Donas']

#
#Para TEST UNITARIOS
#
@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

#
#Para manejo de errores
#
@app.errorhandler(500)
def server_error(error):
    return render_template('400.html', error=error)

@app.errorhandler(404)
def error(error):
    return render_template('404.html', error=error)





#
#RUTAS
#
@app.route('/qrcode')
def qrcode():
    user_ip = request.cookies.get('user_ip')
    #user_name = request.cookies.get('user_name')

    #obtener en un input
    inputURL = 'https://daniepusb.github.io/'

    context = {
        'user_ip': user_ip,
        'todos': todos,
        'qrcode':generarQR(inputURL)
        #'todos': get_todos(user_id=username),
        #'username': username,
        #'todo_form': todo_form,
        #'delete_form': delete_form,
        #'update_form': update_form
    }
    
    #return 'Hello World, ' + user_ip
    return render_template('base.html', **context)


@app.route('/recipes/create', methods=['GET','POST'])
@login_required
def new_recipe():
    title       = 'Nueva receta'
    recipe__form= RecipesForm()
    context = {
        'title'     : title,
        'recipe__form': recipe__form,
    }

    return  render_template('newRecipe.html', **context) 



@app.route('/')
def index():
    #obtener IP
    user__ip = request.remote_addr
    session['user__ip'] = user__ip
    response = make_response(redirect('/auth/login'))

    return response


