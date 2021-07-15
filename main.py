import qrcode # allow make qrCode
import unittest
import stripe
from flask import Flask
from flask import request, make_response, redirect, session, url_for
from flask import render_template 
from flask import jsonify

from app import create_app

from app.common_functions import generarQR
from app.firestore_service import  import__export_data, backend_only_create_tenant, backend_only_sandbox_reset

app = create_app()

todos       = ['Comprar cafe', 'Enviar solicitud de compra', 'Entregar video a productor ']
imgAddress  = 'assets/img/'
recipes     = ['Lemon Pie','Tres Leches','Donas']

#
#Para TEST UNITARIOS
#
@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

#
#Para manejo de errores
#
@app.errorhandler(500)
def server_error(error):
    context = {
        'admin' : session['admin'],
    }
    return render_template('400.html', error=error, **context)

    
@app.errorhandler(404)
def error(error):
    context={}
    if session.get('admin'):
        context['admin']= session['admin']
    return render_template('404.html', error=error, **context)





#
#RUTAS
#
@app.route('/qrcode')
def qrcode():
    user_ip = request.cookies.get('user_ip')
    #user_name = request.cookies.get('user_name')

    #obtener en un input
    inputURL = 'https://daniepusb.github.io/'

    context = {
        'user_ip': user_ip,
        'todos': todos,
        'qrcode':generarQR(inputURL)
        #'todos': get_todos(user_id=username),
        #'username': username,
        #'todo_form': todo_form,
        #'delete_form': delete_form,
        #'update_form': update_form
    }
    
    #return 'Hello World, ' + user_ip
    return render_template('base.html', **context)





@app.route('/')
def index():
    #obtener IP
    user__ip = request.remote_addr
    session['user__ip'] = user__ip
    response = make_response(redirect('/auth/login'))

    return response


"""
it is use in create_payment()
"""
def calculate_order_amount(items):
    # buscar API Stripe para buscar amount
    stripe.api_key = "pk_test_51IcKJFHn1TLFiHT2yyAyH4Mw5ICQ7YduTCu4nBvQyqfkYt4dmC55n3Ns3RJVD1ZhhRmjwmmnjrNvZKFgRSIEGWdF00hBIKrvSw"

    price= stripe.Price.retrieve("price_1IgNtSHn1TLFiHT2RXzSzrY4",)
    print(price)
    print(price['unit_amount_decimal'])
    print(price['currency'])

    return 30000


@app.route('/api/create-payment-intent', methods=['POST'])
def create_payment():
    """
        Procedure to checkout
        http://domain.com/api/create-payment-intent
    """
    try:
        data = json.loads(request.data)
        print(data)
        
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data['items']),
            currency='usd'
        )

        return jsonify({
          'clientSecret': intent['client_secret']
        })
    except Exception as e:
        print(type(e))    # the exception instance
        print(e.args)     # arguments stored in .args
        print(e)          # __str__ allows args to be printed directly,
                          # but may be overridden in exception subclasses
        return jsonify(error=str(e)), 403




       
@app.route('/api/import', methods=['GET'])
def importJson():
    try:
        import__export_data()

        return {'message': 'Done'},200
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly,
                             # but may be overridden in exception subclasses
        return {'message': 'Error importing or exporting data'},400


@app.route('/api/createTenant/<newTenant>/<typeTenant>', methods=['GET'])
def create_tenant(newTenant,typeTenant):
    try:
        backend_only_create_tenant(newTenant,typeTenant)

        return {'message': 'Done'},200
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly,
                             # but may be overridden in exception subclasses
        return {'message': 'Error importing or exporting data'},400



@app.route('/api/sandboxReset', methods=['GET'])
def sandboxReset():
    try:
        backend_only_sandbox_reset()

        return {'message': 'Done' },200
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly,
                             # but may be overridden in exception subclasses
        return {'message': 'Error importing or exporting data'},400


@app.route('/api/info', methods=['GET'])
def getApiInfo():
    try:



        return jsonify(
            [
                {
                'id': 1,
                'name': "dolar today",
                'imagePath': "recetario.png",
                'tasa': 1.1,
                },
                {
                    'id': 2,
                    'name': "tasa2",
                    'imagePath': "recetario.png",
                    'tasa': 1.1,
                }
            ]
        )
    except Exception as e:
        print(type(e))    # the exception instance
        print(e.args)     # arguments stored in .args
        print(e)          # __str__ allows args to be printed directly,
                          # but may be overridden in exception subclasses
        return jsonify(error=str(e)), 403