from . import recipes
from flask import render_template, flash, redirect, url_for, session
from flask_login import login_required, current_user

import app
from app.forms import RecipesForm
from app.firestore_service import get_recipes, get_recipe, recipe_put
from app.models import RecipeData, RecipeModel


@recipes.route('/', methods=['GET'] )
@login_required
def recipes_index():
    return redirect(url_for('recipes.all_recipes'))


@recipes.route('create', methods=['GET','POST'])
@login_required
def new_recipe():
    
    recipe__form= RecipesForm()
    title       = 'Nueva receta'
    ingredients = []

    context = {
        'title'         : title,
        'recipe__form'  : recipe__form,
        'admin'         : session['admin'],
    }

    #solo si es admin debe poder hacer crear una receta
    if recipe__form.validate_on_submit():
        title       = recipe__form.title.data
        description = recipe__form.description.data
        instructions= recipe__form.instructions.data
        ingredient__name        = recipe__form.ingredient__name.data
        ingredient__quantity    = recipe__form.ingredient__quantity.data
        ingredient__unit        = recipe__form.ingredient__unit.data
        
        ingredients = {
            'GALLETA MARIA' : { 'quantity':250, 'unit':'gr','unity':'gramos'},
            ingredient__name: { 'quantity':ingredient__quantity, 'unit': ingredient__unit,'unity':'gramos'},
        }
        print(ingredients)

        recipe__data= RecipeData(title, description, instructions, ingredients)
        recipe_db   = get_recipe(recipe__data.title)

        if recipe_db.to_dict() is None:
            recipe_put(recipe__data)
            flash('Receta creada')
        else:
            flash('Ya existe Receta')


    return  render_template('newRecipe.html', **context) 


@recipes.route('all', methods=['GET','POST'])
@login_required
def all_recipes():

    if current_user.is_authenticated:
        username    = current_user.id
        recipe__form= RecipesForm()

        #solo si es admin debe poder hacer crear una receta
        if recipe__form.validate_on_submit():
            title       = recipe__form.title.data
            description = recipe__form.description.data
            
            recipe__data= RecipeData(title, description)
            recipe_doc  = get_recipe(recipe__data.title)

            if recipe_doc.to_dict() is None:
                recipe_put(recipe__data)
                flash('Receta creada')
            else:
                flash('Ya existe Receta')

        context = {
            'recipes'   : get_recipes(),
            'admin'     : session['admin'],
            'recipe__form':recipe__form
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
        return make_response(redirect('/auth/login'))

