from flask_login        import UserMixin
from flask              import session
from .firestore_service import get_user_with_tenant, get_recipe, get_guest, get_ingredient

#
#USERS Collection(users)
#
class UserData:
    def __init__(self, username, password, admin=False, tenant='', fullname='', gender=''):
        self.username = username
        self.password = password
        self.admin    = admin
        self.tenant   = tenant
        self.fullname = fullname
        self.gender   = gender



class UserModel(UserMixin):
    def __init__(self, user__data):
        """
        :param user_data: UserData
        """
        self.id         = user__data.username
        self.password   = user__data.password
        self.admin      = user__data.admin
        self.tenant     = user__data.tenant
        self.fullname   = user__data.fullname
        self.gender     = user__data.gender

    @staticmethod
    def query(user_id):
        ##TODO: asegurarme que este query solo se ejecute cuando session esté seteada, de lo contrario dará error y no lo estoy manejando con un try
        ##TODO: manejar con un try
        user_doc = get_user_with_tenant(user_id,session['tenant'])
        user_data = UserData(
            username=user_doc.id,
            password=user_doc.to_dict()['password'],
            admin   =user_doc.to_dict()['admin'],
            tenant  =user_doc.to_dict()['tenant'],
            fullname=user_doc.to_dict()['fullname'],
            gender  =user_doc.to_dict()['gender'],
        )

        return UserModel(user_data)


#
#RECIPES Collection(recipes)
#
class RecipeData:
    def __init__(self, title, description, instructions, servings, imageURL, ingredients, product):
        self.title          = title
        self.description    = description
        self.instructions   = instructions
        self.ingredients    = ingredients 
        self.servings       = servings 
        self.product        = product 
        self.imageURL       = imageURL 


class RecipeModel():
    def __init__(self, recipe):
        """
        :param recipe: recipeData
        """
        self.id             = recipe.title
        self.description    = recipe.description
        self.instructions   = recipe.instructions
        self.servings       = recipe.servings
        self.imageURL       = recipe.imageURL
        self.product        = recipe.product 
        self.ingredients    = recipe.ingredients

        

    @staticmethod
    def query(recipe):
        recipe__bd  = get_recipe(recipe)
        recipe__data= RecipeData(
            title       = recipe__bd.id,
            description = recipe__bd.to_dict()['description'],
            instructions= recipe__bd.to_dict()['instructions'],
            servings    = recipe__bd.to_dict()['servings'],
            imageURL    = recipe__bd.to_dict()['imageURL'],
            product     = recipe__bd.to_dict()['product'],
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
        :param ingredient: IngredientData
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





#
#STORES Collection(stores)
#
class StoreData:
    def __init__(self, storeID, name, address, contactNumber, email, telegram, instagram ):
        self.storeID        = storeID
        self.name           = name
        self.address        = address
        self.contactNumber  = contactNumber
        self.email          = email 
        self.telegram       = telegram 
        self.instagram      = instagram 


class StoreModel():
    def __init__(self, storeData):
        """
        :param store: storeData
        """
        self.id             = storeData.storeID
        self.name           = storeData.name
        self.address        = storeData.address
        self.contactNumber  = storeData.contactNumber
        self.email          = storeData.email 
        self.telegram       = storeData.telegram 
        self.instagram      = storeData.instagram 


    @staticmethod
    def query(storeID):
        store__bd  = get_store(storeID)
        store__data= StoreData(
            id              = store__bd.storeID,
            name            = store__bd.to_dict()['name'],
            address         = store__bd.to_dict()['address'],
            contactNumber   = store__bd.to_dict()['contactNumber'],
            email           = store__bd.to_dict()['email'],
            telegram        = store__bd.to_dict()['telegram'],
            instagram       = store__bd.to_dict()['instagram'],
        )
      
        return StoreModel(store__data)




#
#ORDERS Collection(orders)
#
class OrderData:
    def __init__(self, store, deliveryDate, products):
        self.store          = store
        self.deliveryDate   = deliveryDate
        self.products       = products 


class OrderModel():
    def __init__(self, orderData):
        """
        :param order: orderData
        """
        self.id             = orderData.id
        self.store          = orderData.store
        self.deliveryDate   = orderData.deliveryDate
        self.products       = orderData.products
        

    @staticmethod
    def query(order):
        order__bd  = get_order(order)
        order__data= OrderData(
            id          = order__bd.id,
            store       = order__bd.to_dict()['store'],
            deliveryDate= order__bd.to_dict()['deliveryDate'],
            products    = order__bd.to_dict()['products'],
        )
      
        return OrderModel(order__data)





#
#INVENTORY Collection(inventory)
#
class InventoryData:
    def __init__(self, products, ingredients):
        self.products       = products
        self.ingredients    = ingredients

class InventoryModel():
    def __init__(self, inventory):
        """
        :param guest_data: InventoryData
        """
        self.id             = inventory.doc
        self.products       = inventory.products
        self.ingredients    = inventory.ingredients
    



    
#
#PRODCUCTS Collection(products)
#
class ProductData:
    def __init__(self, id, price=0, name='', tenant='DEMO_VENDOR'):
        self.id     = id
        self.price  = price
        self.name   = name
        self.tenant = tenant

class ProductModel():
    def __init__(self, product):
        """
        :param product: ProductData
        """
        self.id     = product.id
        self.price  = product.price
        self.name   = product.name
        self.tenant = product.tenant
    
    @staticmethod
    def query(product):
        product__bd   = get_product(product)
        product__data = ProductData(
            id      = product__bd.id,
            price   = product__bd.price,
            name    = product__bd.name,
            tenant  = product__bd.tenant,
        )

