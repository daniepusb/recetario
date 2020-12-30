from .              import stores
from flask          import render_template, session, request, flash, redirect, url_for
from flask_login    import login_required, current_user

import app
from app.firestore_service  import get_list_stores, get_store, put_store, update_store
from app.common_functions   import check_admin
from app.models             import StoreData, StoreModel


@stores.route('/', methods=['GET'])
@login_required
def list_stores():
    check_admin()
    title = 'Listar locales' 

    context ={
        'navbar'    : 'stores',
        'title'     : title,
        'admin'     : session['admin'],
        'stores'    : get_list_stores(),
    }

    return render_template('stores_list.html', **context)



@stores.route('/create', methods=['GET','POST'])
def create():
    check_admin()
    title   = 'Registrar local' 

    context ={
        'navbar'       : 'stores',
        'title'        : title,
        'admin'        : session['admin'],
    }

    if request.method == 'POST':
        formData = request.form

        context['form'] = formData
        
        name            = formData.get('name').upper()
        address         = formData.get('address')
        contactNumber   = int (formData.get('contactNumber'))
        email           = formData.get('email')
        telegram        = formData.get('telegram')
        instagram       = formData.get('instagram')

        store__data = StoreData(None, name, address, contactNumber, email, telegram, instagram ) 
        put_store(store__data)

        flash('Local creado')
        return redirect(url_for('stores.list_stores'))


    return render_template('store_create.html', **context)



@stores.route('select/<storeID>', methods=['GET'])
@login_required
def select(storeID):
    ##TODO: saber como hacer un buen try catch
    store__db   = get_store(storeID).to_dict()

    ## verificar que si existe este local
    if store__db is not None:
        context = {
            'navbar'    : 'stores',
            'storeID'   : storeID,
            'title'     : store__db.get('name'),
            'form'      : store__db,
            'admin'     : session['admin'],
        }

        return render_template('store_update.html', **context)
    else:
        flash('Local no encontrado')
        return redirect(url_for('stores.list_stores'))



@stores.route('update/<storeID>', methods=['POST'])
@login_required
def update(storeID):
    ##TODO: saber como hacer un buen try catch
    store__db   = get_store(storeID).to_dict()

    ## verificar que si existe este local
    if store__db is not None:
        if request.method == 'POST':
            formData = request.form

            if 'go_back_btn' in formData:
                return redirect(url_for('stores.list_stores'))
            

            name            = formData.get('name').upper()
            address         = formData.get('address')
            contactNumber   = int (formData.get('contactNumber'))
            email           = formData.get('email')
            telegram        = formData.get('telegram')
            instagram       = formData.get('instagram')

            store__data = StoreData(storeID, name, address, contactNumber, email, telegram, instagram ) 
            update_store(store__data)

            flash('Local actualizado')
            return redirect(url_for('stores.list_stores'))
    else:
        print('else')
        flash('Local no encontrado')
        return redirect(url_for('stores.list_stores'))


