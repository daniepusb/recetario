# RECETARIO
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