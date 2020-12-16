from . import recipes
from flask import render_template, flash, redirect, url_for, session, jsonify, request
from flask_login import login_required, current_user


import app
from app.forms import RecipesForm
from app.firestore_service import get_recipes, get_recipe, get_recipe_ingredients, recipe_put, recipe_update
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
    ##TODO: cuando la receta viene sin nombre de receta lanza un error de google
    title       = 'Nueva receta'
    context = {
        'title' : title,
        'admin' : session['admin'],
        'navbar': 'recipes',
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


        return  render_template('recipe_create.html', **context) 

    return  render_template('recipe_create.html', **context) 


@recipes.route('all', methods=['GET'])
@login_required
def all_recipes():

    if current_user.is_authenticated:
        username    = current_user.id

        context = {
            ##TODO: colocar un try catch
            'recipes'   : get_recipes(),
            'admin'     : session['admin'],
            'navbar'    : 'recipes',
        }

        return render_template('recipes_list.html', **context)    
    else:
        #no autenticado
        return make_response(redirect('/auth/login'))


@recipes.route('select/<recipe>', methods=['GET'])
@login_required
def select(recipe):

    ##TODO: saber como hacer un buen try catch
    try:
        pass
    except expression as identifier:
        recipe_db        = None
        ingredients__db  = None
    else:
        pass
    finally:
        pass

    if current_user.is_authenticated:
        username    = current_user.id

        recipe_db   = get_recipe(recipe).to_dict()
        
        ## verificar que si existe esta receta
        if recipe_db is not None:
            ingredients__db = get_recipe_ingredients(recipe)
            
            # a = recipe_db
            # for i,j in a.items():
            #     print(i+str(j))
            # print(u'Document data: {}'.format(recipe_db))
            # print( recipe_db.get('description'))
            # print( recipe_db.get('instructions'))
            # print( recipe_db.get('servings'))
            
            # mostrar = ingredients__db
            # for r in mostrar:
            #     print( r.id ) 
            #     print( r.get('quantity'))
            #     print( r.get('unit'))

            context = {
                'title'         : recipe,
                'form'          : recipe_db,
                'ingredients'   : ingredients__db,
                'admin'         : session['admin'],
                'navbar'        : 'recipes',
            }
            return render_template('recipe_update.html', **context)

        else:
            return redirect(url_for('recipes.all_recipes'))

    else:
        # usuario no autenticado
        # return make_response(redirect('/auth/login'))
        return redirect(url_for('auth.login'))


@recipes.route('update/<recipe>', methods=['POST'])
@login_required
def update(recipe):
    ##TODO: saber como hacer un buen try catch
    ##TODO: esta comprobacion ya no es necesario porque tiene el decorador @login_required
    ##TODO: detectar cambios en el formulario para mostrar el boton de guardar
    context = {
        'title'         : recipe,
        'admin'         : session['admin'],
        'navbar'        : 'recipes',
    }
    
    if request.method== 'POST':
        formData    = request.form
        
        if 'go_back_btn' in formData:
            return redirect(url_for('recipes.all_recipes'))

        else:
            ingredients = {}
            
            #print( formData.to_dict() )

            ##TODO: verificar el nombre receta, si cambia se debe hacer un procedimiento distinto
            title       = recipe
            description = formData.get('description')
            instructions= formData.get('instructions')
            servings    = formData.get('servings')
            
            context['form']     = formData
            context['zipped']   = zip( formData.getlist('ingredients-name'),formData.getlist('ingredients-quantity'),formData.getlist('ingredients-unit'))
            
            for k in context['zipped']:
                ingredients[ k[0] ] = { 'quantity':k[1], 'unit': k[2]}
            print(ingredients)

            recipe__data    = RecipeData(title, description, instructions, servings, ingredients)
            recipe_db       = get_recipe(recipe__data.title)

            if recipe_db.to_dict() is not None:
                recipe_update(recipe__data)
                flash('Receta actualizada')
                return redirect(url_for('recipes.select', recipe=recipe__data.title))
            else:
                flash('No existe receta para actualizar')
                return  render_template('recipe_update.html', **context) 
    else:
        ##GET
        recipe_db   = get_recipe(recipe).to_dict()
        
        if recipe_db is not None:
            ingredients__db = get_recipe_ingredients(recipe)
            
            # a = recipe_db
            # for i,j in a.items():
            #     print(i+str(j))
            # print(u'Document data: {}'.format(recipe_db))
            # print( recipe_db.get('description'))
            # print( recipe_db.get('instructions'))
            # print( recipe_db.get('servings'))
            
            # mostrar = ingredients__db
            # for r in mostrar:
            #     print( r.id ) 
            #     print( r.get('quantity'))
            #     print( r.get('unit'))

            context = {
                'title'         : recipe,
                'form'          : recipe_db,
                'ingredients'   : ingredients__db,
                'admin'         : session['admin'],
                'navbar'        : 'recipes',
            }
            return render_template('recipe_update.html', **context)

        else:
            flash('No existe esa receta')
            return redirect(url_for('recipes.all_recipes'))


