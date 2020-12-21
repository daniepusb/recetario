import firebase_admin
#from firebase_admin import credentials
from firebase_admin import firestore

#credential = credentials.ApplicationDefault()
app = firebase_admin.initialize_app()

db = firestore.client()

#
#USERS
#
def get_users():
    return db.collection('users').get()


def get_user(username):
    return db.collection('users').document(username).get()


def user_put(user__data):
    user_ref = db.collection('users').document(user__data.username)
    user_ref.set({'password': user__data.password,'admin': False})

#
#RECIPES
#
def get_recipes():
    #return db.collection(u'recipes').where(u'capital', u'==', True).stream()
    return db.collection('recipes').stream()


def get_recipe(recipe):
    doc_ref = db.collection(u'recipes').document(recipe)
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
    return db.collection(u'recipes').document(recipe).collection('ingredients').stream()


def recipe_put(recipe):
    recipes_collection_ref = db.collection('recipes').document(recipe.title)
    recipes_collection_ref.set({
        'description'   : recipe.description,
        'instructions'  : recipe.instructions,
        'servings'      : recipe.servings,
        'imageURL'      : recipe.imageURL,
    })
    
    if recipe.ingredients is not None:
        recipes_ingredients_ref = db.collection('recipes').document(recipe.title).collection('ingredients')
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
        
        recipes_collection_ref = db.collection('recipes').document(recipe.title)
        recipes_collection_ref.set(
            {
                'description'   : recipe.description,
                'instructions'  : recipe.instructions,
                'servings'      : recipe.servings,
            }
        )

        recipes_ingredients_ref = db.collection('recipes').document(recipe.title).collection('ingredients')
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
    return db.collection('ingredients').stream()


def get_ingredient(ingredient):
    doc_ref = db.collection(u'ingredients').document(ingredient)
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
    ingredient_collection_ref = db.collection('ingredients').document(ingredient.title)
    ingredient_collection_ref.set({'price': ingredient.price, 'quantity': ingredient.quantity, 'unit': ingredient.unit, 'is_gluten_free': ingredient.is_gluten_free})


def update_ingredient(ingredient, old_ingredient=None):
    if old_ingredient is None:
        ingredient_collection_ref = db.collection('ingredients').document(ingredient.title)
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
#DEPARTMENTS
#
def get_departments():
    #return db.collection(u'recipes').where(u'capital', u'==', True).stream()
    return db.collection('departments').stream()


"""

def get_todos(user_id):
    return db.collection('users')\
        .document(user_id)\
        .collection('todos').get()


def put_todo(user_id, description):
    todos_collection_ref = db.collection('users').document(user_id).collection('todos')
    todos_collection_ref.add({'description': description, 'done': False})


def delete_todo(user_id, todo_id):
    todo_ref = db.document('users/{}/todos/{}'.format(user_id, todo_id))
    todo_ref.delete()


"""