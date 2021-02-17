from .              import orders
from flask          import render_template, session, url_for, request, redirect, flash
from flask_login    import login_required, current_user

import app
from app.firestore_service  import get_daily_list_transactions, put_transaction,check_products_if_exists, get_list_products, get_list_orders, get_order, get_list_stores, get_recipes, put_order, get_order_products
from app.common_functions   import check_admin
from app.models             import OrderData, TransactionData


@orders.route('/', methods=['GET'])
@login_required
def index():

    title = 'Caja'
    
    context = {
        'title'                 : title,
        'navbar'                : 'orders',
        'admin'                 : session['admin'],
        'products__list'        : get_list_products(),
    }
    
    return render_template('order_index.html', **context)


@orders.route('/checkout', methods=['POST'])
@login_required
def checkout():

    if request.method =='POST':
        formData            = request.form
        products__from__form= {}
        products__to__put   = {}
        sumTotal            = 0

        pp = zip( formData.getlist('product'),formData.getlist('quantity'),formData.getlist('price'))
        for k in pp:
            products__from__form[ k[0] ] = { 'quantity':k[1], 'price':k[2] }
        
        # check if this products exist in DB
        products__db    = check_products_if_exists(products__from__form)

        if products__db is not None:
            for key_db in products__db:
                product_in_db   =  products__db[key_db].to_dict()
                name_db         =  product_in_db.get('name')
                price_db        =  product_in_db.get('price')

                quantity__form  = products__from__form[key_db].get('quantity')
                sumTotal       += float(quantity__form) * float(price_db)


                product_in_db['quantity'] = quantity__form
                del product_in_db['description']
                del product_in_db['vendor']
                
                products__to__put[key_db] = product_in_db

            

            # print('total', sumTotal, formData.get('total'))
            if float(formData.get('total')) == float(sumTotal):
                print(products__to__put)
            
                # Create transaction
                transaction = TransactionData(customer="", paymentMethod=formData.get('payment'), price=sumTotal, products=products__to__put, state="", typeof="sell")
                put_transaction(transaction)

            else:
                # reject post action, aperently the price is not the same
                flash("Ocurrio un error: nsd765dahdas98y98apol")
                return redirect(url_for('orders.index'))
        else:
            # reject post action, aperently is missing that product in the DB
            flash("Ocurrio un error: nsd765dahdas98y98apol")
            return redirect(url_for('orders.index'))

    else:
        flash("Ocurrio un error: nsd765dahdas98y98apol")
    return redirect(url_for('orders.index'))
    # return render_template('order_index.html', **context)


@orders.route('/daily', methods=['GET'])
@login_required
def daily():
    """
    """
    title = 'Ventas de hoy'
    list__db = get_daily_list_transactions()
    daily__transactions__list ={}
    
    for i in list__db:
        p=i.to_dict()
        daily__transactions__list[i.id] = p
    # print(daily__transactions__list)

    context = {
        'title'                     : title,
        'navbar'                    : 'orders',
        'admin'                     : session['admin'],
        'daily__transactions__list' : list__db,
    }
    
    return render_template('orders_daily.html', **context)


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



