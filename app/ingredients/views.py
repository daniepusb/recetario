from . import ingredients
from flask import render_template, flash, redirect, url_for, session, jsonify, request
from flask_login import login_required, current_user


import app
from app.firestore_service import get_list_ingredients, get_ingredient
from app.models import RecipeData, RecipeModel
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

        title       = formData.get('title').upper()
        description = formData.get('description')
        instructions= formData.get('instructions')
        # print( formData.to_dict() )

        context['form']     = formData
        context['zipped']   = zip( formData.getlist('ingredients-name'),formData.getlist('ingredients-quantity'),formData.getlist('ingredients-unit'))
        
        for k in context['zipped']:
            ingredients[ k[0] ] = { 'quantity':k[1], 'unit': k[2]}
        #print(ingredients)

        recipe__data= RecipeData(title, description, instructions, ingredients)
        print(recipe__data)

        recipe_db   = get_recipe(recipe__data.title)
        if recipe_db.to_dict() is None:
            recipe_put(recipe__data)
            flash('Receta creada')

            return redirect(url_for('ingredients.list_ingredients'))
        else:
            flash('Ya existe Receta')


        return  render_template('recipe_create.html', **context) 

    return  render_template('recipe_create.html', **context) 


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

        return render_template('ingredients.html', **context)    
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

