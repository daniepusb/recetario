import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

db = firestore.client()


def get_users():
    return db.collection('users').get()


def get_user(username):
    return db.collection('users').document(username).get()


def user_put(user__data):
    user_ref = db.collection('users').document(user__data.username)
    user_ref.set({'password': user__data.password,'admin': False})


def get_recipes():
    #return db.collection(u'recipes').where(u'capital', u'==', True).stream()
    return db.collection('recipes').stream()


def get_recipe(recipe):
    return db.collection('recipes').document(recipe).get()


def recipe_put(recipe):
    recipes_collection_ref = db.collection('recipes').document(recipe.title)
    recipes_collection_ref.set({'description': recipe.description, 'done': False})
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