# RECETARIO
(en desarrollo)
Podrás ver tus recetas creadas, calcular ingredientes, porciones y precios de recetas


## Requisitos
Al ser un proyecto pyhton necesitarás tener python instalado
- Python 3.6
- Se necesita crear el proyecto en Firebase


## Instrucciones
Empecemos por comprobar que tenemos python instalado, luego creamos el ambiente vitual necesario y luego instalar lo que necesitamos para el proyecto.
- python3 -m venv fenv
- source fenv/bin/activate
- pip install -r requirements.txt
- export FLASK_APP=main.py
- export GOOGLE_APPLICATION_CREDENTIALS='/path/to/credentials.json'

- flask run

#### Para ambiente de desarrollo
- export FLASK_DEBUG=1
- export FLASK_ENV=development

#### Para Windows OS deberás usar
source fenv/Scripts/activate

#### Para crear un nuevo módulo deberás
- crear una carpeta dentro de app con el nombre del modulo
- crear archivo __init__.py dentro de modulo y crear el blueprint
- crear archivo views.py dentro de modulo y las rutas necesarias 
- importar funciones de recuperacion de info en BD, por ejemplo: get_list_ingredients()
- en caso de necesitar, crear funcionenes necesarias en firestore_service.py
- en caso de usar render_template, crear el template.html correspondiente en la carpeta template
- registrar blueprint dentro del archivo __init__.py del proyecto principal dentro de la carpeta app
- crear link accesible en el navbar.html
- registrar en BD el permiso del nuevo modulo para cada tenant que lo necesite

