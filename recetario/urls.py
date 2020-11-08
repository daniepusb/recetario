"""Platzigram URLs module."""
#from django.contrib import admin
from django.urls import path

from recetario import views


urlpatterns = [
   # path('admin/', admin.site.urls),        #http://127.0.0.1:8000/admin/
    path('hello-world/', views.hello_world),#http://127.0.0.1:8000/hello-world/
    path('sorted/', views.sort_integers),   #http://127.0.0.1:8000/sorted
    path('hi/<str:name>/<int:age>/', views.say_hi), #http://127.0.0.1:8000/hi/jesus/33
]