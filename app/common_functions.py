from flask import render_template, session, redirect, flash, url_for
from flask_login import  current_user
##
## commons functions 
##


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

##function to detect if the user has been log-in
def isLogin():


    is__login = False

    if session.get('username'): 
        #and request.cookies.get('user_name') and request.cookies.get('user__id') 
        is__login = True

    return is__login


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.admin:
        return False
    else:
        return True