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
    
    #recipe__form= RecipesForm()    #not use wtforms
    title       = 'Nueva receta'

    context = {
        'title'         : title,
        #'recipe__form'  : recipe__form,
        'admin'         : session['admin'],
    }
    
    if request.method== 'POST':
        flash("POST")
        # context = context + { 
        #     'post' : True,
        # }
        return  render_template('newRecipe.html', **context) 
    else:
        flash("GET")
        return  render_template('newRecipe.html', **context) 



    # if not recipe__form.validate_on_submit():
    #     flash("GET")
    #     #print (recipe__form)                           #prints an objeto
    #     #print (recipe__form.ingredients)               #prints html
    #     print (recipe__form.ingredients.data)           #prints a dict
    #     print("**********************************************")

    #solo si es admin debe poder hacer crear una receta
    # if recipe__form.validate_on_submit():
    #     title       = recipe__form.title.data
    #     description = recipe__form.description.data
    #     instructions= recipe__form.instructions.data
    #     ingredients = recipe__form.ingredients.data
    #     #print ( jsonify(recipe__form.ingredients.get('name')) )
    #     print ( recipe__form.ingredients) 
    #     print ( recipe__form.ingredients.data)

        # ingredients = {
        #     ingredients__form.get('name'): { 'quantity':ingredients__form.get('quantity'), 'unit': ingredients__form.get('unit')},
        # }
        # print(ingredients)

        # recipe__data= RecipeData(title, description, instructions, ingredients)
        # recipe_db   = get_recipe(recipe__data.title)

        # if recipe_db.to_dict() is None:
        #     recipe_put(recipe__data)
        #     flash('Receta creada')

            #return redirect(url_for('recipes.all_recipes'))
        # else:
        #     flash('Ya existe Receta')


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

