from flask              import render_template, session, redirect, flash, url_for, make_response, request
from flask_login        import login_user, login_required, logout_user, current_user
from werkzeug.security  import generate_password_hash,  check_password_hash


from . import profile
from app.forms              import LoginForm, GuestForm 
from app.firestore_service  import get_all_users, get_user_with_tenant
from app.models             import UserData, UserModel, GuestData, GuestModel
from datetime               import timedelta

import app

@profile.route('/', methods=['GET'])
@login_required
def index():
    return redirect(url_for('profile.list_users'))


@profile.route('users',methods=['GET'])
@login_required
def list_users():
    title = 'Listar usuarios'

    users = get_all_users()
    users_without_admin={}

    if users is not None:
        for i in users:
            print ('i:', i.id, i)
            if i.id != 'ADMIN':
                users_without_admin[i.id]= i.to_dict()
            
    print(users_without_admin)
    
    context = {
        'title' :   title,
        'users' :   users_without_admin,
        'admin' :   session['admin'],
        'navbar':   'profile',
    }
    
    return render_template('profile_user_list.html', **context) 


@profile.route('signup',methods=['GET', 'POST'])
@login_required
def signup_user():
    context={}
    if session.get('admin') and session.get('admin')== True:
        context = {
            'admin' : session['admin'],
            'navbar': 'profile',
        }

        if request.method == 'POST':
            formData = request.form
            username = formData.get('username').upper()
            password = formData.get('password')
            fullname = formData.get('fullname')
            gender   = formData.get('gender').upper()

            # print(formData)
            context['form']=formData

            user__db = get_user_with_tenant(username,session['tenant'])
            if user__db.to_dict() is None:
                password__hash  = generate_password_hash(password)
                user__data      = UserData(username=username, password=password__hash, admin=False, tenant=session['tenant'], fullname=fullname, gender=gender)

                user_put(user__data)
               
                flash('Usuario '+ username +' registrado', category='info')
                return redirect(url_for('orders.list_orders'))
            else:
                flash('El usuario existe.')
                
        return render_template('signup.html', **context)
    else: 
        flash('No tiene permisos de administrador', category='info')
        return redirect(url_for('orders.list_orders'))


@profile.route('select/<userid>' , methods=['GET'])
@login_required
def select(userid):
    """
    Allows to see user profile
    """

    title= 'Perfil del usuario'
    user = get_user_with_tenant(userid, session['tenant'])
    context = {
        'title' :   title,
        'admin' :   session['admin'],
        'navbar':   'profile',
        'form'  :   user,
    }
    print(user.to_dict())

    return render_template('profile_user_upgrade.html', **context)


@profile.route('profile',methods=['GET'])
@login_required
def profile():
    flash('Ver perfil')
    return render_template('base.html')
