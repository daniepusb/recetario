from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from .config        import Config
#from .admin         import admin
from .auth          import auth
from .ingredients   import ingredients
from .recipes       import recipes
from .models        import UserModel, RecipeModel   

login__manager = LoginManager()
login__manager.login_view = 'auth.login'

@login__manager.user_loader
def load_user(username):
    return UserModel.query(username)

def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)

    app.config.from_object(Config)
    login__manager.init_app(app)
    # login_manager.login_message = "You must be logged in to access this page."
    # login_manager.login_view = "auth.login"

    #Es necesario registrar los blueprints
    #app.register_blueprint(admin)
    app.register_blueprint(auth)
    app.register_blueprint(recipes)
    app.register_blueprint(ingredients)

    return app