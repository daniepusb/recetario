from flask          import Flask
from flask_bootstrap import Bootstrap
from flask_login    import LoginManager

from .config        import Config
#from .admin         import admin
from .auth          import auth
from .faq           import faq
from .ingredients   import ingredients
from .inventory     import inventory
from .models        import UserModel, RecipeModel   
from .orders        import orders
from .products      import products
from .recipes       import recipes
from .stores        import stores
from .vendors       import vendors

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
    app.register_blueprint(faq)
    app.register_blueprint(orders)
    app.register_blueprint(products)
    app.register_blueprint(recipes)
    app.register_blueprint(stores)
    app.register_blueprint(ingredients)
    app.register_blueprint(inventory)
    app.register_blueprint(vendors)

    return app