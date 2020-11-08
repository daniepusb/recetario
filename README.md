# RECETARIO
Proyecto recetario, para manejar los ingredientes, porciones y precio de recetas


## Requisitos
Al ser un proyecto pyhton necesitarás tener python instalado
- Python 3.6


## Instrucciones
Empecemos por comprobar que tenemos python instalado, luego creamos el ambiente vitual necesario y luego instalar lo que necesitamos para el proyecto.
- python -m venv .fenv
- source .fenv/Scripts/activate
- pip install -r requirements.txt
- export FLASK_APP=main.py
- export FLASK_DEBUG=0
- export FLASK_ENV=production

- flask run

#### Para ambiente de desarrollo
- export FLASK_DEBUG=1
- export FLASK_ENV=development

