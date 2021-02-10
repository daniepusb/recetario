from . import ingredients
from flask import render_template, flash, redirect, url_for, session, jsonify, request
from flask_login import login_required, current_user

 
import app
from app.firestore_service import get_list_ingredients, get_ingredient, put_ingredient, update_ingredient
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
        'units' : ['gr', 'ml', 'unidad'],
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
    ##TODO: con el decorador @login_required ya no es necesario preguntar si el current_user está autenticado
    if current_user.is_authenticated:
        username    = current_user.id

        ingredient_db   = get_ingredient(ingredient).to_dict()
        
        ## verificar que si existe esta receta
        if ingredient_db is not None:
            if ingredient_db.get('is_gluten_free'):
                ingredient_db['is_gluten_free'] = True
            else:
                ingredient_db['is_gluten_free'] = False

            context = {
                'title'         : ingredient,
                'form'          : ingredient_db,
                'admin'         : session['admin'],
                'navbar'        : 'ingredients',
            }
            print(ingredient_db['is_gluten_free'])
            
            return render_template('ingredient_update.html', **context)

        else:
            return redirect(url_for('ingredients.list_ingredients'))

    else:
        # usuario no autenticado
        # return make_response(redirect('/auth/login'))
        return redirect(url_for('auth.login'))


@ingredients.route('update/<ingredient>', methods=['POST'])
@login_required
def update(ingredient):
    ##TODO: saber como hacer un buen try catch
    ##TODO: detectar cambios en el formulario para mostrar el boton de guardar
    context = {
        'title'         : ingredient,
        'admin'         : session['admin'],
        'navbar'        : 'ingredient',
    }
    
    if request.method== 'POST':
        formData    = request.form
        
        if 'go_back_btn' in formData:
            return redirect(url_for('ingredient.list_ingredients'))
        else:
            print( formData.to_dict() )
    
            ##TODO: verificar el nombre receta, si cambia se debe hacer un procedimiento distinto
            title           = ingredient
            price           = float (formData.get('price') )
            quantity        = float (formData.get('quantity') )
            unit            = formData.get('unit')
            
            if formData.get('is_gluten_free'):
                is_gluten_free = True
            else:
                is_gluten_free = False
            
            ingredient__data    = IngredientData(title, price, quantity, unit, is_gluten_free)
            ingredient_db       = get_ingredient(ingredient__data.title)
            # print(ingredient_db.to_dict())

            if ingredient_db.to_dict() is not None:
                update_ingredient(ingredient__data)
                flash('Ingrediente actualizado')
                return redirect(url_for('ingredients.select', ingredient=ingredient__data.title))
            else:
                flash('No existe ingrediente para actualizar')
                return redirect(url_for('ingredients.list_ingredients'))
    
            # return redirect(url_for('ingredients.select', ingredient=ingredient__data.title))


@ingredients.route('/dropdownHTML', methods=['GET'] )
@login_required
def ajaxHTML():
    ingredients     = get_list_ingredients()

    context = {
        'ingredients__list' : ingredients,
    }

    return render_template('dropdown.html', **context)


@ingredients.route('/dropdown', methods=['GET'] )
@login_required
def ajax():
    ingredients     = get_list_ingredients()
    r=''
    i=0
    for j in ingredients:
        r += "<option>"+ j.id + "</option>"

    return r
    #return jsonify(r)