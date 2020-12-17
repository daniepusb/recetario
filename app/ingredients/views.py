from . import ingredients
from flask import render_template, flash, redirect, url_for, session, jsonify, request
from flask_login import login_required, current_user


import app
from app.firestore_service import get_list_ingredients, get_ingredient, put_ingredient
from app.models import IngredientData
from app.common_functions import check_admin


@ingredients.route('/', methods=['GET'] )
@login_required
def index():
    return redirect(url_for('ingredients.list_ingredients'))



@ingredients.route('create', methods=['GET','POST'])
@login_required
def create():
    
    title       = 'Nuevo Ingrediente'
    context = {
        'title' : title,
        'admin' : session['admin'],
        'navbar': 'ingredients',
    }
    
    if request.method== 'POST':
        ingredients = {}
        formData    = request.form

        title           = formData.get('title').upper()
        price           = formData.get('price')
        quantity        = int(formData.get('quantity'))
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


@ingredients.route('all', methods=['GET'])
@login_required
def list_ingredients():

    if current_user.is_authenticated:
        username    = current_user.id

        context = {
            'ingredients'   : get_list_ingredients(),
            'admin'         : session['admin'],
            'navbar'        : 'ingredients',
        }

        return render_template('ingredients_list.html', **context)    
    else:
        #no autenticado
        return make_response(redirect('/auth/login'))


@ingredients.route('select/<ingredient>', methods=['GET'])
@login_required
def select(ingredient):

    ##TODO: saber como hacer un buen try catch
    if current_user.is_authenticated:
        username    = current_user.id

        ingredient_db   = get_ingredient(ingredient).to_dict()
        
        ## verificar que si existe esta receta
        if ingredient_db is not None:
            # a = ingredient_db
            # for i,j in a.items():
            #     print(i+str(j))
            # print(u'Document data: {}'.format(ingredient_db))
            # print( recipe_db.get('description'))
            # print( recipe_db.get('instructions'))

            # for r in mostrar:
            #     print( r.id ) 
            #     print( r.get('quantity'))
            #     print( r.get('unit'))

            context = {
                'title'         : ingredient,
                'properties'    : ingredient_db,
                'admin'         : session['admin'],
                'navbar': 'ingredients',
            }
            return render_template('ingredient.html', **context)

        else:
            return redirect(url_for('ingredients.all_recipes'))

    else:
        # usuario no autenticado
        # return make_response(redirect('/auth/login'))
        return redirect(url_for('auth.login'))

