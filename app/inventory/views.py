from . import inventory
from flask import render_template, flash, redirect, url_for, session, jsonify, request
from flask_login import login_required, current_user

 
import app
from app.firestore_service import get_inventory_products, get_inventory_ingredients, get_list_products, get_inventory_product_info, get_product, add_inventory
from app.models import  ProductData, InventoryData
from app.common_functions import check_admin


@inventory.route('/', methods=['GET'] )
@login_required
def index():
    return redirect(url_for('inventory.list_inventory'))


@inventory.route('all', methods=['GET'])
@login_required
def list_inventory():
    ##TODO: revisar que siempre exista fullname dentro de current_user, y si es así entonces revisar que todos lo puedan usar
    context  = {
        'admin'         : session['admin'],
        'navbar'        : 'inventory',
    }
    
    if session['tenantPermits'].get('products'):
        products            = get_inventory_products()
        context['products'] = products
    if session['tenantPermits'].get('ingredients'):
        ingredients             = get_inventory_ingredients()
        context['ingredients']  = ingredients

    return render_template('inventory_list.html', **context)    


@inventory.route('add', methods=['GET','POST'])
@login_required
def add():
    
    title       = 'Agregar al inventario'
    context = {
        'title'         : title,
        'admin'         : session['admin'],
        'navbar'        : 'inventory',
        'products__list': get_list_products(),
    }
    
    if request.method== 'POST':
        formData    = request.form
        productID   = formData.get('productID')
        amount      = int (formData.get('amount'))
        

        product__db  = get_product(productID)
        if product__db is None:
            return  render_template('inventory_add.html', **context) 

        if product__db.to_dict() is None:
            return  render_template('inventory_add.html', **context) 
        else:
            # si existe, buscar producto en lista de inventario
                #si exite producto en el inventario, sumar amount + inventory.get('quantity') y actualizar
                #sino existe entonces agregar el producto con amount

            inventory  = get_inventory_product_info(productID)
            
            if inventory.to_dict() is not None:
                quantity        = inventory.get('quantity') + amount
                print(quantity)
                inventory__data = InventoryData(
                    id=productID, 
                    name=inventory.get('name'), 
                    quantity=quantity,
                    typeof=inventory.get('type')) 
                add_inventory(inventory__data)

                flash('Inventario actualizado')
                return redirect(url_for('inventory.list_inventory'))
            else:
                inventory__data = InventoryData(id=product__db.id, name=product__db.get('name'), quantity=amount, typeof='product' ) 
                add_inventory(inventory__data)

                flash('Inventario actualizado')
                return redirect(url_for('inventory.list_inventory'))

        return  render_template('inventory_add.html', **context) 

    return  render_template('inventory_add.html', **context) 

@inventory.route('delete', methods=['GET','POST'])
@login_required
def delete():
    
    title       = 'Eliminar del inventario'
    context = {
        'title'         : title,
        'admin'         : session['admin'],
        'navbar'        : 'inventory',
        'products__list': get_list_products(),
    }
    
    if request.method== 'POST':
        formData    = request.form
        productID   = formData.get('productID')
        amount      = int (formData.get('amount'))
        

        product__db  = get_product(productID)
        if product__db is None:
            return  render_template('inventory_delete.html', **context) 

        if product__db.to_dict() is None:
            return  render_template('inventory_delete.html', **context) 
        else:
            inventory  = get_inventory_product_info(productID)
            
            if inventory.to_dict() is not None:
                quantity        = inventory.get('quantity') - amount
                if quantity > 0:
                    print(quantity)
                    inventory__data = InventoryData(
                        id=productID, 
                        name=inventory.get('name'), 
                        quantity=quantity,
                        typeof=inventory.get('type')) 
                    add_inventory(inventory__data)

                    flash('Inventario actualizado')
                    return redirect(url_for('inventory.list_inventory'))
                else:
                    flash('Cantidad imposible de eliminar')
                    return redirect(url_for('inventory.list_inventory'))
            else:
                inventory__data = InventoryData(id=product__db.id, name=product__db.get('name'), quantity=amount, typeof='product' ) 
                add_inventory(inventory__data)

                flash('Inventario actualizado')
                return redirect(url_for('inventory.list_inventory'))

        return  render_template('inventory_delete.html', **context) 

    return  render_template('inventory_delete.html', **context) 



@inventory.route('ajax/<productID>',methods=['GET'])
def ajax(productID):
    response = {}
    info = get_inventory_product_info(productID).to_dict()

    if info is not None:
        response = {'response': info},200
    else:
        # response = {'response': {'name':'NULL','quantity':0,'type':'NULL','unit':'NULL'}},200
        response = {'response': 'NULL'},200

    return response