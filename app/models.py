from flask_login import UserMixin

from .firestore_service import get_user, get_recipe, get_guest, get_ingredient

#
#USERS Collection(users)
#
class UserData:
    def __init__(self, username, admin=False):
        self.username = username
        self.admin    = admin


class UserModel(UserMixin):
    def __init__(self, user__data):
        """
        :param user_data: UserData
        """
        self.id         = user__data.username
        self.admin      = user__data.admin

    @staticmethod
    def query(user_id):
        user_doc = get_user(user_id)
        user_data = UserData(
            username=user_doc.id,
            admin   =user_doc.to_dict()['admin'],
        )

        return UserModel(user_data)


#
#RECIPES Collection(recipes)
#
class RecipeData:
    def __init__(self, title, description, instructions, servings, ingredients):
        self.title          = title
        self.description    = description
        self.instructions   = instructions
        self.ingredients    = ingredients 
        self.servings       = servings 


class RecipeModel():
    def __init__(self, recipe):
        """
        :param recipe: recipeData
        """
        self.id             = recipe.title
        self.description    = recipe.description
        self.instructions   = recipe.instructions
        self.servings       = recipe.servings
        self.ingredients    = recipe.ingredients

        

    @staticmethod
    def query(recipe):
        recipe__bd  = get_recipe(recipe)
        recipe__data= RecipeData(
            title       = recipe__bd.id,
            description = recipe__bd.to_dict()['description'],
            instructions= recipe__bd.to_dict()['instructions'],
            servings    = recipe__bd.to_dict()['servings'],
            ingredients = recipe__bd.to_dict()['ingredients'],
        )
      
        return RecipeModel(recipe__data)



#
#GUESTS Collection(guest)
#
class GuestData:
    def __init__(self, name, email, phone):
        self.email   = email
        self.name    = name
        self.phone   = phone


class GuestModel():
    def __init__(self, guest):
        """
        :param guest_data: GuestData
        """
        self.email   = guest.email
        self.name    = guest.name
        self.phone   = guest.phone
    
    @staticmethod
    def query(email):
        guest__bd   = get_guest(email)
        guest_data  = GuestData(
            email   = guest__bd.id,
            name    = guest__bd.to_dict()['name'],
            phone   = guest__bd.to_dict()['phone'],
        )
      
        return GuestModel(guest_data)



#
#INGREDIENTS Collection(ingredients)
#
class IngredientData:
    def __init__(self, title, price=0, quantity=0, unit='gr', is_gluten_free=False):
        self.title          = title
        self.price          = price
        self.quantity       = quantity
        self.unit           = unit
        self.is_gluten_free = is_gluten_free

class IngredientsModel():
    def __init__(self, ingredient):
        """
        :param guest_data: GuestData
        """
        self.id             = ingredient.title
        self.price          = ingredient.price
        self.quantity       = ingredient.quantity
        self.unit           = ingredient.unit
        self.is_gluten_free = ingredient.is_gluten_free
    
    @staticmethod
    def query(ingredient):
        ingredient__bd   = get_ingredient(email)
        ingredient__data = IngredientData(
            title           = ingredient__bd.id,
            price           = ingredient__bd.price,
            quantity        = ingredient__bd.quantity,
            unit            = ingredient__bd.unit,
            is_gluten_free  = ingredient__bd.is_gluten_free,
        )