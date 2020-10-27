from flask import render_template, session, redirect, flash, url_for, make_response

from . import auth
from app.forms import LoginForm
from app.common_functions import generarQR, isLogin

import app


@auth.route('/login', methods=['GET','POST'])
def login():
    user__ip=   session.get('user__ip')
    title   =   'login'
    template=   'login.html'
    func__redirect  = '/recipes'
    is__login       = isLogin()
    login__form     = LoginForm()
    
    context = {
        'user__ip'  : user__ip,
        'title'     : title,
        'is__login' : is__login,
        'login__form':login__form
    }

    if login__form.validate_on_submit():
        username = login__form.username.data
        session['username'] = username
        flash('Nombre de usario registrado con éxito!')
        session['is__login'] = True
        return make_response(redirect(func__redirect))

    if is__login:
        #print("SESSION_LOGIN_DONE")
        response = make_response(redirect(func__redirect))
    else:
        #print("SESSION_LOGIN_NOT_DONE")
        response = render_template(template, **context)

    return response


