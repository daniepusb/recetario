from . import inventory
from flask import render_template, flash, redirect, url_for, session, jsonify, request
from flask_login import login_required, current_user

 
import app
from app.firestore_service import get_inventory_products, get_inventory_ingredients
from app.models import IngredientData, InventoryData
from app.common_functions import check_admin


@inventory.route('/', methods=['GET'] )
@login_required
def index():
    return redirect(url_for('inventory.list_inventory'))


@inventory.route('all', methods=['GET'])
@login_required
def list_inventory():

    if current_user.is_authenticated:
        fullname    = current_user.fullname

        context  = {
            'admin'         : session['admin'],
            'navbar'        : 'inventory',
        }
        
        products    = get_inventory_products()
        ingredients = get_inventory_ingredients()

        if products is not None:
            context['products']    = products
        if products is not None:
            context['ingredients'] = ingredients


        return render_template('inventory_list.html', **context)    
    else:
        #no autenticado
        return make_response(redirect('/auth/login'))


@inventory.route('create', methods=['GET','POST'])
@login_required
def create():
    
    title       = 'Agregar al inventario'
    context = {
        'title' : title,
        'admin' : session['admin'],
        'navbar': 'inventory',
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

            return redirect(url_for('inventory.list_inventory'))
        else:
            flash('Ya existe Ingrediente')


        return  render_template('inventory_add.html', **context) 

    return  render_template('inventory_add.html', **context) 
