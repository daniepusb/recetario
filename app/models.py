from flask_login import UserMixin

from .firestore_service import get_user

#users
class UserData:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class UserModel(UserMixin):
    def __init__(self, user__data):
        """
        :param user_data: UserData
        """
        self.id = user__data.username
        self.password = user__data.password

    @staticmethod
    def query(user_id):
        user_doc = get_user(user_id)
        user_data = UserData(
            username=user_doc.id,
            password=user_doc.to_dict()['password']
        )

        return UserModel(user_data)


#recipes
class RecipeData:
    def __init__(self, title, description):
        self.title = title
        self.description = description


class RecipeModel():
    def __init__(self, recipe):
        """
        :param recipe: recipeData
        """
        self.id = recipe.title
        self.description = recipe.description

    @staticmethod
    def query(recipe):
        recipe__bd = get_recipe(recipe)
        print(recipe__bd.title)
        recipe__data = RecipeData(
            title=recipe__bd.title,
            description=recipe__bd.to_dict()['description']
        )

        return RecipeModel(recipe__data)