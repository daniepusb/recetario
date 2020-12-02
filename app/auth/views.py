from flask import render_template, session, redirect, flash, url_for, make_response
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash,  check_password_hash

from . import auth
from app.forms import LoginForm
from app.common_functions import generarQR, isLogin
from app.firestore_service import get_user, user_put
from app.models import UserData, UserModel

import app

@auth.route('signup', methods=['GET','POST'])
def signup():
    signup__form = LoginForm()
    
    context = {
        'signup__form' : signup__form
    }

    if signup__form.validate_on_submit():
        username = signup__form.username.data
        password = signup__form.password.data

        user__doc = get_user(username)

        if user__doc.to_dict() is None:
            password__hash  = generate_password_hash(password)
            user__data      = UserData(username,password__hash)
            user_put(user__data)

            user = UserModel(user__data)

            login_user(user)
            flash('Bienvenido')

            return redirect(url_for('recipes'))
        else:
            flash('El usuario existe.')


    return render_template('signup.html', **context)


@auth.route('/login', methods=['GET','POST'])
def login():

    login__form = LoginForm()
    template    = 'login.html'
    context = {
        'user__ip'      : session.get('user__ip'),
        'login__form'   : login__form,
        'template'      : template,
        'func__redirect': '/recipes/list',
    }

    #asi preguntamos para metodo POST
    #No es necesario un else
    if login__form.validate_on_submit():
        username = login__form.username.data
        password = login__form.password.data

        user__doc = get_user(username)

        if user__doc.to_dict() is not None:
            if check_password_hash(user__doc.to_dict()['password'], password):
                user__data  = UserData(username, password)
                user        = UserModel(user__data) 
                
                login_user(user)
                session['username'] = username

                flash('Bienvenido de nuevo')
                
                response = make_response(redirect('/recipes/all'))
            else:
                flash('La informacion no coincide')
                response = render_template(template, **context)
        else:
            flash('El usuario no existe')
            response = render_template(template, **context)
    

    #si el usuario está logueado, redireccionar a recipes
    if current_user.is_authenticated:
        response = make_response(redirect('/recipes/all'))
    else:
        response = render_template(template, **context)

    return response


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    session['username']=''
    logout_user()
    flash('Logout done')
    #todo: agregar una prueba para asegurar que en la cookie no quedan datos del usuario
    return redirect(url_for('auth.login'))
