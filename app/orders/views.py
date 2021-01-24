from .              import orders
from flask          import render_template, session, url_for, request, redirect, flash
from flask_login    import login_required, current_user

import app
from app.firestore_service  import get_list_orders, get_order, get_list_stores, get_recipes, put_order, get_order_products
from app.common_functions   import check_admin
from app.models             import OrderData, OrderModel


@orders.route('/', methods=['GET'])
@login_required
def list_orders():
    check_admin()
    title   = 'Historial de pedidos' 

    context ={
        'navbar'    : 'orders',
        'title'     : title,
        'admin'     : session['admin'],
        'title'     : title,
        'orders'    : get_list_orders(),
    }
    return render_template('orders_list.html', **context)



@orders.route('/create', methods=['GET','POST'])
@login_required
def create():
    check_admin()
    title   = 'Registrar pedido' 

    context ={
        'navbar'        : 'orders',
        'title'         : title,
        'admin'         : session['admin'],
        'stores__list'  : get_list_stores(),
    }

    context['products__list']={}

    for j in get_recipes():
        if j.get('product'):
            context['products__list'][j.id] = j
    ##TODO: context['products__list'] contiene los productos para mostrar en el dropdown
        ##sin embargo para cada producto se debe tener en cuenta el servings porque en el input de cantidad el min y el step debe ser igual a servings y eso es un trabajo

    if request.method == 'POST':
        formData = request.form
        context['form']  = formData
        # print(formData)

        store           = formData.get('store-name')
        deliveryDate    = formData.get('delivery-date')
        #deliveryDate    = datetime (formData.get('delivery-date') )

        # agrupo los productos de la misma manera que los ingredientes para que sean una subcoleccion dentro de la base de datos en orders        
        products = {}
        context['zipped']   = zip( formData.getlist('product-name'),formData.getlist('product-quantity'))
        for k in context['zipped']:
            products[ k[0] ] = { 'quantity':k[1] }
        # print(products)

        order__data = OrderData(store,deliveryDate,products)
        try:
            orderID = put_order(order__data)
        except expression as identifier:
            flash('Error: ' + orderID)
            print('ocurrio un error: '+ str(orderID))
        finally:
            flash('Pedido registrado: ' + orderID)
            return redirect(url_for('orders.list_orders'))


        return render_template('order_create.html', **context)
        #return redirect(url_for('orders.create'))




    return render_template('order_create.html', **context)



@orders.route('/select/<orderID>' , methods=['GET'])
@login_required
def select(orderID):
    check_admin()
    title   = 'Ver Pedido' 

    order__db   = get_order(orderID).to_dict()
        
    ##verificar que si existe este pedido para ese ID
    if order__db is not None:
        products__db = get_order_products(orderID)

        context ={
            'navbar'        : 'orders',
            'title'         : title,
            'admin'         : session['admin'],
            'form'          : order__db,
            'stores__list'  : get_list_stores(),
            'products'      : products__db,
            'id'            : orderID,
        }
        ##TODO: ojo que el parametro order de esta funcion se está usando sin ninguna restriccion en get_order()

        return render_template('order_update.html' , **context)


    else:
        return redirect(url_for('orders.list_orders'))








@orders.route('/update' , methods=['POST'])
@login_required
def update():
    check_admin()
    title   = 'Ver Pedido' 

    if request.method == 'POST':
        formData = request.form

        context ={
            'navbar'    : 'orders',
            'title'     : title,
            'admin'     : session['admin'],
            'title'     : title,
            'form'      : formData,
        }
        ##TODO: ojo que el parametro order de esta funcion se está usando sin ninguna restriccion en get_order()

        return redirect(url_for('orders.list_orders'))

    else:
        return redirect(url_for('orders.list_orders'))


@orders.route('/simulate' , methods=['GET','POST'])
@login_required
def simulate():
    pass



