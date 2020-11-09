# RECETARIO
Proyecto recetario, para manejar los ingredientes, porciones y precio de recetas


## Requisitos
Al ser un proyecto django/pyhton necesitarás tener python instalado. También usaremos una base de datos NoSQL y usaremos el servicio de firestore de Google
- Python 3.6
- Proyecto creado en Firebase


## Instrucciones
Empecemos por comprobar que tenemos python instalado, luego creamos el ambiente vitual necesario y luego instalar lo que necesitamos para el proyecto.
- python -m venv .denv
- source .denv/Scripts/activate
- pip install -r requirements.txt

Deberás crear un archivo 'credentials.json' 
- export GOOGLE_APPLICATION_CREDENTIALS='/path/to/credentials.json'


- python manage.py runserver



Para ambiente de desarrollo modificar el valor de DEBUG en el archivo settings.py
- settings.py [ DEBUG = True ]


