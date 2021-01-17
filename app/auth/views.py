from flask              import render_template, session, redirect, flash, url_for, make_response, request
from flask_login        import login_user, login_required, logout_user, current_user
from werkzeug.security  import generate_password_hash,  check_password_hash


from . import auth
from app.forms              import LoginForm, GuestForm 
from app.common_functions   import generarQR, isLogin
from app.firestore_service  import get_user, user_put, get_guest, guest_put
from app.models             import UserData, UserModel, GuestData, GuestModel
from datetime               import timedelta

import app

@auth.route('signup', methods=['GET','POST'])
@login_required
def signup():
    ##TODO: verificar que al momento de generar la contraseña esté sumando un SAL, un código adicional al final para que no sea reversible y mas seguro
    if ( session['admin'] ):
        signup__form = LoginForm()
        
        context = {
            'signup__form'  : signup__form,
            'admin'         : session['admin'],
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
                flash(username +', Bienvenid@', category='info')

                # next = flask.request.args.get('next')
                # is_safe_url should check if the url is safe for redirects.
                # See http://flask.pocoo.org/snippets/62/ for an example.
                # if not is_safe_url(next):
                #     return flask.abort(400)


                return redirect(url_for('recipes.list_recipes'))
            else:
                flash('El usuario existe.')


        return render_template('signup.html', **context)
    else: 
        return redirect(url_for('recipes.list_recipes'))


@auth.route('signupGuest', methods=['GET','POST'])
def signup_guest():
    #TODO: add captcha
    signup__guest__form = GuestForm()
    
    context = {
        'signup__guest__form' : signup__guest__form
    }

    if signup__guest__form.validate_on_submit():
        name = signup__guest__form.name.data
        email = signup__guest__form.email.data
        phone = signup__guest__form.phone.data

        guest__doc = get_guest(email)
        


        if guest__doc.to_dict() is None:
            guest__data = GuestData(name,email,phone)
            
            guest = GuestModel(guest__data)
            guest_put(guest)

            flash('Gracias por usar Recetario, muy pronto será invitado')
            #TODO:Luego de invitarlo aqui pudiera mostrar un manual de las bondades de RECETARIO, el "how it works"

            #next = request.args.get('next')
            ##TODO: is_safe_url should check if the url is safe for redirects.
            ## See http://flask.pocoo.org/snippets/62/ for an example.
            #if not is_safe_url(next):
            #    return flask.abort(400)


            return render_template('signupGuestDone.html', **context)
        else:
            flash('El invitado existe')
    else:
        flash('Por favor, sirvase de introducir sus datos para poder ser invitado por el admin ')

    return render_template('signupGuest.html', **context)


@auth.route('login', methods=['GET','POST'])
def login():

    context = {
        'user__ip'      : session.get('user__ip'),
    }
    
    response = render_template('login.html', **context)
    
    if request.method == 'POST':
        formData    = request.form
        tenant      = formData.get('tenant').upper()
        username    = formData.get('username').upper()
        password    = formData.get('password')

        # print(formData)
        context['form'] = formData

        user__db = get_user(username).to_dict()

        if user__db is not None:
            if check_password_hash(user__db['password'], password):
                if tenant == user__db['tenant']:
                    user__data  = UserData(username=username,password=password, admin=user__db['admin'], tenant=user__db['tenant'], fullname=user__db['fullname'], gender=user__db['gender'] )
                    user        = UserModel(user__data) 

                    login_user(user, remember=False, duration=None, force=False, fresh=True)
                    session['tenant']   = user.tenant
                    session['username'] = username
                    session['admin']    = user.admin
                    session['fullname'] = user.fullname
                    session['gender']   = user.gender
                    
                    print(session)

                    if user.gender =='male':
                        flash(user.fullname +', Bienvenido de nuevo', category='info')
                    elif user.gender =='female':
                        flash(user.fullname +', Bienvenida de nuevo', category='info')

                    response = make_response(redirect('/recipes/all'))
                else:
                    response = render_template('login.html', **context)
            else:
                flash('La informacion no coincide', category='warning')
                response = render_template('login.html', **context)
        else:
            flash('El usuario no existe', category='error')
            ##TODO: customize los flash con colores
            ##TODO: quizas un mensaje diferente flash('La informacion no coincide')
            response = render_template('login.html', **context)
    

    #si el usuario está logueado, redireccionar a recipes
    if current_user.is_authenticated:
        response = make_response(redirect('/recipes/all'))

    return response


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    session.pop('username')
    session.pop('admin')
    ##TODO: saber si es necesario o no lo session.pop()
    logout_user()
    flash('Logout done')
    #todo: agregar una prueba para asegurar que en la cookie no quedan datos del usuario
    return redirect(url_for('auth.login'))
