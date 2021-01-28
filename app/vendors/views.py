from .              import vendors
from flask          import render_template, session, request, flash, redirect, url_for
from flask_login    import login_required, current_user

import app
from app.firestore_service import get_list_vendors, get_vendor, put_vendor, update_vendor
from app.models             import VendorData, VendorModel


@vendors.route('/', methods=['GET'])
@login_required
def list_vendors():
    title = 'Listar Vendedores' 

    context ={
        'admin'     : session['admin'],
        'navbar'    : 'inventory',
        'title'     : title,
        'vendors'   : get_list_vendors(),
    }

    return render_template('vendors_list.html', **context)



@vendors.route('/create', methods=['GET','POST'])
def create():
    title   = 'Registrar vendedor' 

    context ={
        'admin'        : session['admin'],
        'navbar'       : 'inventory',
        'title'        : title,
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

        vendor__data = VendorData(None, name, address, contactNumber, email, telegram, instagram ) 
        put_vendor(vendor__data)

        flash('Vendedor creado')
        return redirect(url_for('vendors.list_vendors'))


    return render_template('vendor_create.html', **context)



@vendors.route('select/<vendorID>', methods=['GET'])
@login_required
def select(vendorID):
    ##TODO:try catch
    vendor__db   = get_vendor(vendorID).to_dict()

    ## verificar que si existe este vendedor
    if vendor__db is not None:
        context = {
            'navbar'    : 'inventory',
            'vendorID'  : vendorID,
            'title'     : vendor__db.get('name'),
            'form'      : vendor__db,
            'admin'     : session['admin'],
        }

        return render_template('vendor_update.html', **context)
    else:
        flash('Vendedor no encontrado')
        return redirect(url_for('vendors.list_vendors'))



@vendors.route('update/<vendorID>', methods=['POST'])
@login_required
def update(vendorID):
    ##TODO: saber como hacer un buen try catch
    vendor__db   = get_vendor(vendorID).to_dict()

    ## verificar que si existe este local
    if vendor__db is not None:
        if request.method == 'POST':
            formData = request.form

            if 'go_back_btn' in formData:
                return redirect(url_for('vendors.list_vendors'))
            

            name            = formData.get('name').upper()
            address         = formData.get('address')
            contactNumber   = int (formData.get('contactNumber'))
            email           = formData.get('email')
            telegram        = formData.get('telegram')
            instagram       = formData.get('instagram')

            vendor__data = VendorData(vendorID, name, address, contactNumber, email, telegram, instagram ) 
            update_vendor(vendor__data)

            flash('Vendedor actualizado')
            return redirect(url_for('vendors.list_vendors'))
    else:
        flash('Vendedor no encontrado')
        return redirect(url_for('vendors.list_vendors'))


