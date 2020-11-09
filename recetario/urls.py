"""Platzigram URLs module."""
#from django.contrib import admin
from django.urls import path

from recetario import views as local_views
from recipes import views as recipes_views


urlpatterns = [
   #path('admin/', admin.site.urls),        #http://127.0.0.1:8000/admin/
    path('', local_views.recipes),#http://127.0.0.1:8000/recipes
    path('hello-world/', local_views.hello_world),#http://127.0.0.1:8000/hello-world/
    path('sorted/', local_views.sort_integers),   #http://127.0.0.1:8000/sorted
    path('hi/<str:name>/<int:age>/', local_views.say_hi), #http://127.0.0.1:8000/hi/jesus/33

    path('recipes/', recipes_views.list_recipes),  #http://127.0.0.1:8000/recipes
    path('postres/', recipes_views.Recipes.as_view(), name="index"),
]