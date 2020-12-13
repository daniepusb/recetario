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


def get_ingredients(recipe):
    return db.collection(u'recipes').document(recipe).collection('ingredients').stream()


def recipe_put(recipe):
    recipes_collection_ref = db.collection('recipes').document(recipe.title)
    recipes_collection_ref.set({'description': recipe.description,'instructions': recipe.instructions})
    
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
    




#
#GUESTS
#
def get_guest(email):
    return db.collection('guest').document(email).get()


def guest_put(guest):
    recipes_collection_ref = db.collection('guest').document(guest.email)
    recipes_collection_ref.set({'email': guest.email, 'name': guest.name, 'phone': guest.phone})



#
#RECIPES
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