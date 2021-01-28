from . import products
from flask import render_template, flash, redirect, url_for, session, jsonify, request
from flask_login import login_required, current_user

 
import app
from app.firestore_service import get_list_products, get_list_vendors, get_product, update_product, put_product
from app.models import ProductData
from app.common_functions import check_admin


@products.route('/', methods=['GET'] )
@login_required
def index():
    return redirect(url_for('products.list_products'))


@products.route('create', methods=['GET','POST'])
@login_required
def create():
    
    title       = 'Nuevo Producto'
    context = {
        'title' : title,
        'admin' : session['admin'],
        'navbar': 'inventory',
        'vendors__list': get_list_vendors(),
    }
    
    if request.method== 'POST':
        products    = {}
        formData    = request.form

        name        = formData.get('name').upper()
        description = formData.get('description')
        price       = float (formData.get('price'))
        vendor      = formData.get('vendor').upper()

        context['form'] = formData

        product__data= ProductData(id=None, name=name, description=description, price=price, vendor=vendor)

        product__db   = None #get_product(name)
        if product__db is None and product__db is None:
            put_product(product__data)
            flash('Producto creado')

            return redirect(url_for('products.list_products'))
        else:
            flash('Ya existe producto')


        return  render_template('product_create.html', **context) 

    return  render_template('product_create.html', **context) 


@products.route('all', methods=['GET'])
@login_required
def list_products():
    context = {
        'products'  :   get_list_products(),
        'admin'     :   session['admin'],
        'navbar'    :   'inventory',
    }

    return render_template('products_list.html', **context)    


@products.route('select/<product>', methods=['GET'])
@login_required
def select(product):
    """
    Function return a render_template to see the properties of the product selected
    """
    ##TODO: ojo que get_produdct() puede arrojar un None
    product_db   = get_product(product).to_dict()
    
    ## verificar que si existe esta receta  
    if product_db is not None:
        context = {
            'id'            : product,
            'title'         : product_db.get('name'),
            'form'          : product_db,
            'admin'         : session['admin'],
            'navbar'        : 'inventory',
        }
        
        return render_template('product_update.html', **context)

    else:
        ##TODO: esto es un recordatorio para crear un codigo de error y poder loguearlo en bD como un log y luego poder registrarlo en caso de que el usuario haga un mal request
        flash('Producto no encontrado')
        return redirect(url_for('products.list_products'))


@products.route('update/<product>', methods=['POST'])
@login_required
def update(product):
    if request.method== 'POST':
        ##TODO: verificar requet.form y sus inputs
        formData    = request.form
        
        if 'go_back_btn' in formData:
            return redirect(url_for('products.list_products'))
        else:
            price   = float (formData.get('price') )
            
            product_db      = get_product(product)
            
            if product_db.to_dict() is not None:
                product__data   = ProductData(id=product, name=product_db.get('name'),description=product_db.get('description'), price=price, vendor=product_db.get('vendor'))
                update_product(product__data)

                flash('Producto actualizado')
                return redirect(url_for('products.select', product=product))
            else:
                flash('No existe producto para actualizar')
                return redirect(url_for('products.list_products'))
    
    return redirect(url_for('products.select', product=product))

