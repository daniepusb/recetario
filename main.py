from flask import Flask
from flask import request, make_response, redirect, flash
from flask import render_template # allow to render from templates
import qrcode # allow make qrCode

#from flask_bootstrap import Bootstrap(app)

app = Flask(__name__)

todos       = ['Comprar cafe', 'Enviar solicitud de compra', 'Entregar video a productor ']
imgAddress  = 'assets/img/'


@app.errorhandler(404)
def error(error):
    return render_template('404.html', error=error)

#decorador de pyhton
@app.route('/hello')
def hello():
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


#decorador de pyhton
@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    response.set_cookie('user_ip',user_ip)

    return response




def generarQR(url):
    nombre_imagen = imgAddress + 'qrcode.png'

    # Link for website
    input_data = url

    #Creating an instance of qrcode
    qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5)
    qr.add_data(input_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save('static/' + nombre_imagen)
    
    #print( '\nstatic/' + nombre_imagen + '\n')
    
    return nombre_imagen