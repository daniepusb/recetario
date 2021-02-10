import datetime
import firebase_admin
from flask import session
from firebase_admin import firestore

app = firebase_admin.initialize_app()
db = firestore.client()

## when you use document.get() return a list []
## when you use collection.stream() return a generator

#
#USERS
#
def get_all_users():
    """
    Return a list with all users in your tenant
    """
    # return db.collection(session['type__of__tenant']).document(session['tenant']).collection('users').where(, u'!=', u'ADMIN').stream()
    return db.collection(session['type__of__tenant']).document(session['tenant']).collection('users').stream()

def get_user(username):
    return db.collection('users').document(username).get()

def get_user_with_tenant(username,tenant):
    """
    Return single user from DB using username as ID
    """
    return db.collection(session['type__of__tenant']).document(tenant).collection('users').document(username).get()

def user_put(user__data):
    user_ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection('users').document(user__data.username)
    user_ref.set({'password': user__data.password,'admin': False, 'tenant':session['tenant'], 'gender':user__data.gender, 'fullname':user__data.fullname})

def user_put_into_newsletter(email,tenant):
    """
    Add email to newsLetter list in BD
    """
    user_ref = db.collection('newsletter').document(email)
    user_ref.set({'tenant':tenant})



#
#RECIPES
#
def get_recipes():
    #return db.collection(u'collection').where(u'capital', u'==', True).stream()
    return db.collection(session['type__of__tenant']).document(session['tenant']).collection('recipes').stream()


def get_recipe(recipe):
    doc_ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection(u'recipes').document(recipe)
    try:
        doc = doc_ref.get()
        # a = doc.to_dict()
        # for i,j in a.items():
        #     print(i+str(j))
        # print(u'Document data: {}'.format(doc.to_dict()))
    except google.cloud.exceptions.NotFound:
        print('No such document!')
        doc = None

    return doc


def get_recipe_ingredients(recipe):
    return db.collection(session['type__of__tenant']).document(session['tenant']).collection(u'recipes').document(recipe).collection('ingredients').stream()


def recipe_put(recipe):
    recipes_collection_ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection('recipes').document(recipe.title)
    recipes_collection_ref.set({
        'description'   : recipe.description,
        'instructions'  : recipe.instructions,
        'servings'      : recipe.servings,
        'imageURL'      : recipe.imageURL,
        'product'       : recipe.product,
    })
    
    if recipe.ingredients is not None:
        recipes_ingredients_ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection('recipes').document(recipe.title).collection('ingredients')
        for k,v in recipe.ingredients.items():
            recipes_ingredients_ref.document(k).set(v)

        # recipes_ingredients_ref = db.collection('recipes').document(recipe.title).collection('ingredients')
        # for k,v in recipe.ingredients.items():

        #     print ('k:' + str(k))
        #     print ('v:' + str(v))
        #     for key,values in v.items():
        #         print ('key:' + str(key))
        #         print ('values:' + str(values))
        #         recipes_ingredients_ref.document(k).set({ 
        #             key: str(values),
        #         })

        # recipes_ingredients_ref.document('Galleta Maria').set({
        #     'daniel':   250,
        #     'unit'  :   "gr",
        #     'angy'  :   "ml",
        # }, merge=True)

    # for k,v in recipe.ingredients.items():
    #     for key,values in v.items():
    #         recipes_ingredients_ref.document(k).set({ 
    #             key: str(values),
    #         })
    

def recipe_update(recipe, old_recipe=None):
    if old_recipe is None:
        # search for collection recipe reference
        # set new content fields
        # search for collection ingredients reference

        # for each document delete those
        # set new ingredients subcollections reference
        # set new content 
        
        recipes_collection_ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection('recipes').document(recipe.title)
        recipes_collection_ref.set(
            {
                'description'   : recipe.description,
                'instructions'  : recipe.instructions,
                'servings'      : recipe.servings,
                'imageURL'      : recipe.imageURL,
                'product'       : recipe.product,
            }
        )

        recipes_ingredients_ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection('recipes').document(recipe.title).collection('ingredients')
        delete_collection(recipes_ingredients_ref, 100, 0)

        if recipe.ingredients is not None:
            for k,v in recipe.ingredients.items():
                recipes_ingredients_ref.document(k).set(v)
    else:
        ## TODO: delete old_recipe and call recipe_put(recipe):
        pass



def delete_collection(coll_ref, batch_size, counter):
    batch = db.batch()
    init_counter=counter
    docs = coll_ref.limit(500).get()
    deleted = 0

    for doc in docs:
        batch.delete(doc.reference)
        deleted = deleted + 1

    if deleted >= batch_size:
        new_counter= init_counter + deleted
        batch.commit()
        print("potentially deleted: " + str(new_counter))
        return delete_collection(coll_ref, batch_size, new_counter)
    batch.commit()



#
#INGREDIENTS
#
def get_list_ingredients():
    return db.collection(session['type__of__tenant']).document(session['tenant']).collection('ingredients').stream()


def get_ingredient(ingredient):
    doc_ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection(u'ingredients').document(ingredient)
    try:
        doc = doc_ref.get()
        # a = doc.to_dict()
        # for i,j in a.items():
        #     print(i+str(j))
        # print(u'Document data: {}'.format(doc.to_dict()))
    except google.cloud.exceptions.NotFound:
        print('No such document!')
        doc = None

    return doc


def put_ingredient(ingredient):
    ingredient_collection_ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection('ingredients').document(ingredient.title)
    ingredient_collection_ref.set({'price': ingredient.price, 'quantity': ingredient.quantity, 'unit': ingredient.unit, 'is_gluten_free': ingredient.is_gluten_free})


def update_ingredient(ingredient, old_ingredient=None):
    if old_ingredient is None:
        ingredient_collection_ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection('ingredients').document(ingredient.title)
        ingredient_collection_ref.set({'price': ingredient.price, 'quantity': ingredient.quantity, 'unit': ingredient.unit, 'is_gluten_free': ingredient.is_gluten_free})
    else:
        ## TODO: delete old_ingredient and call put_ingredient(ingredient):
        pass


#
#GUESTS
#
def get_guest(email):
    return db.collection('guest').document(email).get()


def guest_put(guest):
    recipes_collection_ref = db.collection('guest').document(guest.email)
    recipes_collection_ref.set({'email': guest.email, 'name': guest.name, 'phone': guest.phone})


#
# ORDERS
#
def get_list_orders():
    return db.collection(session['type__of__tenant']).document(session['tenant']).collection('orders').stream()


def get_order(id):
    doc_ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection(u'orders').document(id)
    try:
        doc = doc_ref.get()
    except google.cloud.exceptions.NotFound:
        print('No such document!')
        doc = None
    return doc


def get_order_products(orderID):
    return db.collection(session['type__of__tenant']).document(session['tenant']).collection(u'orders').document(orderID).collection('products').stream()


def put_order(order):
    order_ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection('orders').document()
    order_ref.set({
        'store'         : order.store,
        'createdDate'   : datetime.datetime.now(),
        'deliveryDate'  : order.deliveryDate,
    })
    
    if order.products is not None:
        products_ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection('orders').document(order_ref.id).collection('products')
        for k,v in order.products.items():
            products_ref.document(k).set(v)

    return order_ref.id


#
# STORES
#
def get_list_stores():
    return db.collection(session['type__of__tenant']).document(session['tenant']).collection('stores').stream()


def get_store(id):
    doc_ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection(u'stores').document(id)
    try:
        doc = doc_ref.get()
    except google.cloud.exceptions.NotFound:
        print('No such document!')
        doc = None
    return doc


def put_store(store):
    store_collection_ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection('stores')
    store_collection_ref.add({
        'name'          : store.name,
        'address'       : store.address,
        'contactNumber' : store.contactNumber,
        'email'         : store.email,
        'telegram'      : store.telegram,
        'instagram'     : store.instagram,
    })


def update_store(store, old_store=None):
    if old_store is None:
        store_collection_ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection('stores').document(store.storeID)
        store_collection_ref.set({
            'name'          : store.name,
            'address'       : store.address,
            'contactNumber' : store.contactNumber,
            'email'         : store.email,
            'telegram'      : store.telegram,
            'instagram'     : store.instagram,
        })
    else:
        ## TODO: delete old_store and call put_store(store):
        pass


#
# VENDORS
#
def get_list_vendors():
    return db.collection(session['type__of__tenant']).document(session['tenant']).collection('vendors').stream()


def get_vendor(id):
    doc_ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection(u'vendors').document(id)
    try:
        doc = doc_ref.get()
    except google.cloud.exceptions.NotFound:
        print('No such document!')
        doc = None
    return doc


def put_vendor(vendor):
    vendor__collection__ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection('vendors')
    vendor__collection__ref.add({
        'name'          : vendor.name,
        'address'       : vendor.address,
        'contactNumber' : vendor.contactNumber,
        'email'         : vendor.email,
        'telegram'      : vendor.telegram,
        'instagram'     : vendor.instagram,
    })


def update_vendor(vendor, old_vendor=None):
    if old_vendor is None:
        vendor_collection_ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection('vendors').document(vendor.vendorID)
        vendor_collection_ref.set({
            'name'          : vendor.name,
            'address'       : vendor.address,
            'contactNumber' : vendor.contactNumber,
            'email'         : vendor.email,
            'telegram'      : vendor.telegram,
            'instagram'     : vendor.instagram,
        })
    else:
        ## TODO: delete old_vendor and call put_store(vendor):
        pass




#
#INVENTORY
#
def get_inventory_products():
    return db.collection(session['type__of__tenant']).document(session['tenant']).collection('inventory').where(u'type', u'==', u'product').stream()


def get_inventory_ingredients():
    return db.collection(session['type__of__tenant']).document(session['tenant']).collection('inventory').where(u'type', u'==', u'ingredient').stream()


def get_inventory_product_info(productID):
    """
    Return info of product 
    """
    return db.collection(session['type__of__tenant']).document(session['tenant']).collection('inventory').document(productID).get()


def add_inventory(inventory):
    """
    Procedure to add a product to the inventory
    """
    ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection('inventory').document(inventory.id)
    ref.set({
        'name'      : inventory.name,
        'quantity'  : inventory.quantity,
        'type'      : inventory.typeof,
    })
    
    


#
#TENANT
#
def create_demo_tenant_and_demo_user(email,password,typeTenant='VENDOR'):
    """
    Create new demo tenant in sandbox collection
    """
    ref         = db.collection('createTenant').document(typeTenant).get()
    admin__ref  = db.collection('createTenant').document(typeTenant).collection('users').document('ADMIN').get()
    
    dicc        = ref.to_dict()
    dicc__user  = admin__ref.to_dict()
    
    dicc['name']            = email
    dicc__user['fullname']  = email
    dicc__user['tenant']    = email
    dicc__user['password']  = password
    
    to__ref     = db.collection('sandbox').document(email).set(dicc)
    to__ref_user= db.collection('sandbox').document(email).collection('users').document(email).set(dicc__user)
    

def get_tenat_info(tenant):
    return db.collection(session['type__of__tenant']).document(tenant).get()




#
# CAUTION: just for admin and sandbox trigger
#
def import__export_data():
    pass
    # from_ref= db.collection('ADMIN').stream()
    # to_ref  = db.collection('tenant').document('ARIANI')
    
    # for doc in from_ref:
    #     to_ref.document(doc.id).set(doc.to_dict())
 
        
def backend_only_create_tenant(newTenant,typeTenant='VENDOR'):
    """
    Create new Tenant
    """
    #comprobar que NO existe tenant (NO QUEREMOS SOBREESCRIBIR Todo UN CLIENTE POR FAVOR)
    #obtener referencia a VENDOR o STORE con typeTenant
    #obtener referencia a subcolección users para guardar usuario ADMIN
    ref         = db.collection('createTenant').document(typeTenant).get()
    admin__ref  = db.collection('createTenant').document(typeTenant).collection('users').document('ADMIN').get()
    
    dicc        = ref.to_dict()
    dicc__user  = admin__ref.to_dict()
    
    dicc['name']=newTenant
    dicc__user['tenant']=newTenant
    
    to__ref     = db.collection('sandbox').document(newTenant).set(dicc)
    to__ref_user= db.collection('sandbox').document(newTenant).collection('users').document('ADMIN').set(dicc__user)
    
    return True


def backend_only_sandbox_reset():
    """
    Restore sandbox state to NEW
    Is time to reboot all this mess
    Version 2
    """
    # obtener la lista de todos los tenants en la colleccion sandbox
    # para cada tenant en la lista:
        # buscar la referencia del tenant
        # buscar sus subcolecciones
        # para cada subcoleccione, borrar contenido usando delete_collection(recipes_ingredients_ref, 100, 0)
    # borrar sandbox
    # DONE

    try:
        tenants = db.collection('sandbox').stream()
        for tenant in tenants:
            print(tenant.id) 
            ref         = db.collection('sandbox').document(tenant.id)
            ref_obj     = ref.get()
            dicc        = ref_obj.to_dict()
            
            if ref.collection('recipes'):
                ref__recipes    = ref.collection('recipes')
                delete_collection(ref__recipes, 100, 0)
            if ref.collection('ingredients'):
                ref__ingredients= ref.collection('ingredients')
                delete_collection(ref__ingredients, 100, 0)
            if ref.collection('orders'):
                ref__orders     = ref.collection('orders')
                delete_collection(ref__orders, 100, 0)
            if ref.collection('users'):
                ref__users      = ref.collection('users')
                delete_collection(ref__users, 100, 0)
            if ref.collection('inventory'):
                ref__inventory  = ref.collection('inventory')
                delete_collection(ref__inventory, 100, 0)
            if ref.collection('stores'):
                ref__stores     = ref.collection('stores')
                delete_collection(ref.collection('stores'), 100, 0)


        delete_collection(db.collection('sandbox'), 100, 0)
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly,
                             # but may be overridden in exception subclasses

    


    return True


def backend_only_sandbox_reset_v1():
    """
    Restore sandbox state to NEW
    Is time to reboot all this mess
    """
    # buscar la referencia a sandbox
    # obtener la lista de todos los tenants 
        # buscar la referencia del tenant
        # buscar sus subcolecciones
        # para cada subcoleccione, borrar contenido usando delete_collection(recipes_ingredients_ref, 100, 0)
        # buscar su tipo de tenant
        # buscar refencia al tenant original
        # reemplazar tenant por la referencia original 
    # DONE

    try:
        tenants = db.collection('sandbox').stream()
        for tenant in tenants:
            print(tenant.id) 
            ref         = db.collection('sandbox').document(tenant.id)
            ref_obj     = ref.get()
            dicc        = ref_obj.to_dict()
            typeTenant  = dicc['type']
            
            if ref.collection('recipes'):
                ref__recipes    = ref.collection('recipes')
                delete_collection(ref__recipes, 100, 0)
            if ref.collection('ingredients'):
                ref__ingredients= ref.collection('ingredients')
                delete_collection(ref__ingredients, 100, 0)
            if ref.collection('orders'):
                ref__orders     = ref.collection('orders')
                delete_collection(ref__orders, 100, 0)
            if ref.collection('users'):
                ref__users      = ref.collection('users')
                delete_collection(ref__users, 100, 0)
            if ref.collection('inventory'):
                ref__inventory  = ref.collection('inventory')
                delete_collection(ref__inventory, 100, 0)
            if ref.collection('stores'):
                ref__stores     = ref.collection('stores')
                delete_collection(ref__stores, 100, 0)

            original_ref                = db.collection('createTenant').document(typeTenant).get()
            admin__user__original_ref   = db.collection('createTenant').document(typeTenant).collection('users').document('ADMIN').get()

            dicc                        = original_ref.to_dict()
            dicc__user                  = admin__user__original_ref.to_dict()
            
            dicc['name']=tenant.id
            dicc['type']=tenant.id
            dicc__user['tenant']=tenant.id
            
            db.collection('sandbox').document(tenant.id).set(dicc)
            db.collection('sandbox').document(tenant.id).collection('users').document('ADMIN').set(dicc__user)
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly,
                             # but may be overridden in exception subclasses

    


    return True



#
#PRODUCTS
#
def get_list_products():
    return db.collection(session['type__of__tenant']).document(session['tenant']).collection('products').stream()


def get_product(product):
    doc_ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection(u'products').document(product)
    try:
        doc = doc_ref.get()
    except google.cloud.exceptions.NotFound:
        print('No such document!')
        doc = None

    return doc


def put_product(product):
    product_collection_ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection('products').document()
    product_collection_ref.set({ 'name': product.name, 'description': product.description,'price': product.price, 'vendor': product.vendor})


def update_product(product, old_product=None):
    if old_product is None:
        product_collection_ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection('products').document(product.id)
        product_collection_ref.set({'price': product.price, 'name': product.name, 'description': product.description, 'vendor': product.vendor})
    else:
        ## TODO: delete old_product and call put_product(product):
        pass


def check_products_if_exists(products):
    """
    return None if one of products ID is not Found
    """
    result  = {}

    for p in products:
        i   = db.collection(session['type__of__tenant']).document(session['tenant']).collection('products').document(p).get()
        
        if i.to_dict() is None:
            return None
        else:
            result[i.id] = i
            # dicc =  result[i.id]].to_dict()
            # name =  dicc.get('name')
            # print(name, i.id, dicc, ite)

    return result




#
#TRANSACTIONS
#
def get_daily_list_transactions():
    # return db.collection(session['type__of__tenant']).document(session['tenant']).collection('transactions').stream()
    return db.collection(session['type__of__tenant']).document(session['tenant']).collection('transactions').where(u'createDate', u'!=', datetime.datetime.today()).stream()


def get_transaction(transaction):
    doc_ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection('transactions').document(transaction)
    try:
        doc = doc_ref.get()
    except google.cloud.exceptions.NotFound:
        print('No such document!')
        doc = None
    return doc


def put_transaction(transaction):
    transactions_ref = db.collection(session['type__of__tenant']).document(session['tenant']).collection('transactions').document()
    transactions_ref.set({
        'createDate'    : datetime.datetime.now(),
        'customer'      : "",
        'paymentMethod' : transaction.paymentMethod,
        'price'         : transaction.price,
        'products'      : transaction.products,
        'state'         : transaction.state,
        'type'          : transaction.typeof,
        })


# def get_todos(user_id):
#     return db.collection('users')\
#         .document(user_id)\
#         .collection('todos').get()


# def put_todo(user_id, description):
#     todos_collection_ref = db.collection('users').document(user_id).collection('todos')
#     todos_collection_ref.add({'description': description, 'done': False})


# def delete_todo(user_id, todo_id):
#     todo_ref = db.document('users/{}/todos/{}'.format(user_id, todo_id))
#     todo_ref.delete()

