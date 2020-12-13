from . import recipes
from flask import render_template, flash, redirect, url_for, session, jsonify, request
from flask_login import login_required, current_user


import app
from app.forms import RecipesForm
from app.firestore_service import get_recipes, get_recipe, recipe_put
from app.models import RecipeData, RecipeModel
from app.common_functions import check_admin


@recipes.route('/', methods=['GET'] )
@login_required
def recipes_index():
    return redirect(url_for('recipes.all_recipes'))


@recipes.route('/ajax', methods=['GET'] )
def ajax():
    
    check_admin()

    recipe__form    = RecipesForm()
    response        = recipe__form.ingredients

    return jsonify(response)



@recipes.route('create', methods=['GET','POST'])
@login_required
def new_recipe():
    
    title       = 'Nueva receta'
    context = {
        'title' : title,
        'admin' : session['admin'],
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

            return redirect(url_for('recipes.all_recipes'))
        else:
            flash('Ya existe Receta')


        return  render_template('newRecipe.html', **context) 
    else:
        flash("GET")
        return  render_template('newRecipe.html', **context) 

    return  render_template('newRecipe.html', **context) 


@recipes.route('all', methods=['GET'])
@login_required
def all_recipes():

    if current_user.is_authenticated:
        username    = current_user.id

        context = {
            'recipes'   : get_recipes(),
            'admin'     : session['admin'],
        }

        return render_template('recipes.html', **context)    
    else:
        #no autenticado
        return make_response(redirect('/auth/login'))


@recipes.route('select/<recipe>', methods=['GET'])
@login_required
def select_recipe(recipe):

    if current_user.is_authenticated:
        username    = current_user.id

        try:
            recipe__data    = get_recipe(recipe).to_dict()
            #print( recipe__data.to_dict()['description'] ) 
        except expression as identifier:
            recipe__data    = None
        else:
            pass
        finally:
            pass
            #flash('Busqueda completada')

        context = { 
            'recipe': recipe__data,
            'admin' : session['admin'],
        }
        
        return render_template('recipe.html', **context)    
    else:
        #no autenticado
        # return make_response(redirect('/auth/login'))
        return redirect(url_for('auth.login'))

