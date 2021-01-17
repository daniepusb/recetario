from . import inventory
from flask import render_template, flash, redirect, url_for, session, jsonify, request
from flask_login import login_required, current_user

 
import app
from app.firestore_service import get_list_inventory, get_list_ingredients
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
        print(current_user)
        username    = current_user.id

        context = {
            'admin'         : session['admin'],
            'navbar'        : 'inventory',
            'products'      : get_list_inventory(),
            'ingredients'   : get_list_ingredients(),
        }

        return render_template('inventory_list.html', **context)    
    else:
        #no autenticado
        return make_response(redirect('/auth/login'))

