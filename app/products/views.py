from . import products
from flask import render_template, flash, redirect, url_for, session, jsonify, request
from flask_login import login_required, current_user

 
import app
from app.firestore_service import get_list_products, get_product, update_product
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
        'navbar': 'ingredients',
    }
    
    if request.method== 'POST':
        ingredients = {}
        formData    = request.form

        title           = formData.get('title').upper()
        price           = float (formData.get('price'))
        quantity        = float (formData.get('quantity'))
        unit            = formData.get('unit')
        
        if formData.get('is_gluten_free'):
            is_gluten_free = True
        else:
            is_gluten_free = False
        ##TODO: cuando falla el post no mantiene el valor de checkbox

        context['form']     = formData

        ingredient__data= IngredientData(title, price, quantity, unit, is_gluten_free)
        #print(ingredient__data.is_gluten_free)

        ingredient__db   = get_ingredient(title)
        if ingredient__db.to_dict() is None:
            put_ingredient(ingredient__data)
            flash('Ingrediente creado')

            return redirect(url_for('ingredients.list_ingredients'))
        else:
            flash('Ya existe Ingrediente')


        return  render_template('ingredient_create.html', **context) 

    return  render_template('ingredient_create.html', **context) 


@products.route('all', methods=['GET'])
@login_required
def list_products():
    context = {
        'products'  :   get_list_products(),
        'admin'     :   session['admin'],
        'navbar'    :   'products',
    }

    return render_template('products_list.html', **context)    


@products.route('select/<product>', methods=['GET'])
@login_required
def select(product):
    """
    Function return a render_template to see the properties of the product selected
    """
    product_db   = get_product(product).to_dict()
    
    ## verificar que si existe esta receta  
    if product_db is not None:
        context = {
            'id'            : product,
            'title'         : product_db.get('name'),
            'form'          : product_db,
            'admin'         : session['admin'],
            'navbar'        : 'products',
        }
        
        return render_template('product_update.html', **context)

    else:
        ##TODO: esto es un recordatorio para crear un codigo de error y poder loguearlo en bD como un log y luego poder registrarlo en caso de que el usuario haga un mal request
        flash('Producto no encontrado')
        return redirect(url_for('products.list_products'))


@products.route('update/<product>', methods=['POST'])
@login_required
def update(product):
    context = {
        'admin'         : session['admin'],
        'navbar'        : 'product',
    }
    
    if request.method== 'POST':
        ##TODO: verificar requet.form y sus inputs
        formData    = request.form
        
        if 'go_back_btn' in formData:
            return redirect(url_for('products.list_products'))
        else:
            price   = float (formData.get('price') )
            
            product_db      = get_product(product)
            
            if product_db.to_dict() is not None:
                product__data   = ProductData(id=product, name=product_db.get('name'), price=price, tenant=product_db.get('tenant'))
                update_product(product__data)

                flash('Producto actualizado')
                return redirect(url_for('products.select', product=product))
            else:
                flash('No existe producto para actualizar')
                return redirect(url_for('products.list_products'))
    
    return redirect(url_for('products.select', product=product))


@products.route('/dropdownHTML', methods=['GET'] )
@login_required
def ajaxHTML():
    ingredients     = get_list_ingredients()

    context = {
        'ingredients__list' : ingredients,
    }

    return render_template('dropdown.html', **context)

@products.route('/dropdown', methods=['GET'] )
@login_required
def ajax():
    ingredients     = get_list_ingredients()
    r=''
    i=0
    for j in ingredients:
        r += "<option>"+ j.id + "</option>"

    return r
    #return jsonify(r)