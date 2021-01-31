from flask              import render_template, session, redirect, flash, url_for, make_response, request
from flask_login        import login_user, login_required, logout_user, current_user
from werkzeug.security  import generate_password_hash,  check_password_hash


from . import auth
from app.forms              import LoginForm, GuestForm 
from app.common_functions   import generarQR, isLogin
from app.firestore_service  import user_put, get_guest, guest_put, get_user_with_tenant, get_tenat_info, user_put_into_newsletter, create_demo_tenant_and_demo_user
from app.models             import UserData, UserModel, GuestData, GuestModel
from datetime               import timedelta

import app

@auth.route('signup', methods=['GET','POST'])
@login_required
def signup():
    ##TODO: verificar que al momento de generar la contraseña esté sumando un SAL, un código adicional al final para que no sea reversible y mas seguro
    context={}
    if session.get('admin'):
        context = {
            'admin': session['admin'],
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


@auth.route('demo',methods=['GET'])
def demo():
    flash('Recuerda que podrás usar la plataforma, pero todos tus cambios se guardarán solo por 24 horas')
    return render_template('demo_login.html')


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
    """
    In order to authentificate a user

    type__of__tenant has two options: tenant or sandbox
    """
    context = {}
    
    response = render_template('login.html', **context)
    
    if request.method == 'POST':
        ##TODO: creear funncion que asegure el input del login
        formData    = request.form
        
        user__db    = ''
        tenant      = ''
        password    = ''
        temrs       = ''
        username    = ''

        if formData.get('tenant'):
            tenant      = formData.get('tenant').upper()
        if formData.get('tenant_store'):
            tenant      = formData.get('tenant_store').upper()

        if formData.get('password'):
            password    = formData.get('password')
        if formData.get('password_store'):
            password    = formData.get('password_store')

        if formData.get('terms'):
            terms       = formData.get('terms').upper()
        if formData.get('terms_store'):
            terms       = formData.get('terms_store').upper()
        
        if formData.get('username'):
            username       = formData.get('username').upper()
        if formData.get('username_store'):
            username       = formData.get('username_store').upper()

        if tenant=='DEMO_VENDOR' and password=='contraseñanosegurademo':
            session['type__of__tenant'] =   'sandbox'
            session['tenant']           =   username
            tenant                      =   username

            user__db = get_user_with_tenant(username,username).to_dict()

            if user__db is None:
                password__hash  = generate_password_hash(password)
                create_demo_tenant_and_demo_user(username,password__hash,'VENDOR')
                user_put_into_newsletter(username,username)
                user__db = get_user_with_tenant(username,username).to_dict()

        elif tenant=='DEMO_STORE' and password=='contraseñanosegurademo':
            session['type__of__tenant'] =   'sandbox'
            session['tenant']           =   username
            tenant                      =   username
            user__db = get_user_with_tenant(username,username).to_dict()
            
            if user__db is None:
                password__hash  = generate_password_hash(password)
                create_demo_tenant_and_demo_user(username,password__hash,'STORE')
                user_put_into_newsletter(username,username)
                user__db        = get_user_with_tenant(username,username).to_dict()
            
        else:
            session['type__of__tenant'] ='tenant'
            session['tenant']           = tenant
            context['form']             = formData
            user__db = get_user_with_tenant(username,tenant).to_dict()


        
        if user__db is not None:
            if check_password_hash(user__db['password'], password):
                if tenant == user__db['tenant']:
                    user__data  = UserData(username=username,password=password, admin=user__db['admin'], tenant=user__db['tenant'], fullname=user__db['fullname'], gender=user__db['gender'] )
                    user        = UserModel(user__data) 
                    # search tenant info (like imageURL)
                    tenant = get_tenat_info(tenant)

                    ##TODO: llamar a una funcion que agregue todos estos
                    ##TODO: crear una funcion que los quite y usar esa funcion en log_out
                    session['admin']            = user.admin
                    session['fullname']         = user.fullname
                    session['gender']           = user.gender
                    session['tenant']           = user.tenant
                    session['tenantImageURL']   = tenant.get('imageURL')
                    session['tenantName']       = tenant.get('name')
                    session['tenantType']       = tenant.get('type')
                    session['tenantPermits']    = tenant.get('permits')
                    session['tenantPayments']   = tenant.get('payments')
                    session['username']         = user.id

                    login_user(user, remember=False, duration=None, force=False, fresh=True)

                    if user.gender =='male':
                        flash(user.fullname +', Bienvenido', category='info')
                    elif user.gender =='female':
                        flash(user.fullname +', Bienvenida', category='info')

                    response = make_response(redirect('/orders'))
                else:
                    flash('La informacion no coincide', category='warning')
                    response = render_template('login.html', **context)
            else:
                flash('La informacion no coincide', category='warning')
                response = render_template('login.html', **context)
        else:
            flash('La informacion no coincide', category='error')
            ##TODO: customize los flash con colores
            ##TODO: quizas un mensaje diferente flash('La informacion no coincide o el usuario no existe')
            response = render_template('login.html', **context)
    

    #si el usuario está logueado, redireccionar a recipes
    if current_user.is_authenticated:
        response = make_response(redirect('/orders'))

    return response


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    session.pop('admin')
    session.pop('fullname')
    session.pop('gender')
    session.pop('tenant')
    session.pop('tenantImageURL')
    session.pop('tenantName')
    session.pop('tenantType')
    session.pop('tenantPermits')
    session.pop('tenantPayments')
    session.pop('username')

    ##TODO: saber si es necesario o no lo session.pop()
    logout_user()
    flash('Logout done')
    #todo: agregar una prueba para asegurar que en la cookie no quedan datos del usuario
    return redirect(url_for('auth.login'))
