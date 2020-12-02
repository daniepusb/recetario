from . import recipes
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

import app
from app.forms import RecipesForm
from app.firestore_service import get_recipes, get_recipe, recipe_put
from app.models import RecipeData, RecipeModel

@recipes.route('/', methods=['GET'] )
@login_required
def recipes_index():
    return redirect(url_for('recipes.all_recipes'))

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
            'admin'     : True, #current_user.admin,
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
            recipe__data    = get_recipe(recipe)
        except expression as identifier:
            recipe__data    = None
        else:
            pass
        finally:
            flash('Busqueda completada')
            print(recipe__data.id)

        context = { 
            'recipe'    :   recipe__data,
        }
        print
        return render_template('recipe.html', **context)    
    else:
        #no autenticado
        return make_response(redirect('/auth/login'))

