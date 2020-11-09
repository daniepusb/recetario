"""Recipes views."""

# Django
#from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View 
# Utilities
from datetime import datetime

# Firebase connections
#from recetario import firestore_service
from recetario.firestore_service import get_recipes

posts = [
    {
        'name': 'Mont Blac',
        'user': 'Yésica Cortés',
        'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
        'picture': 'https://picsum.photos/200/200/?image=1036',
    },
    {
        'name': 'Via Láctea',
        'user': 'C. Vander',
        'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
        'picture': 'https://picsum.photos/200/200/?image=903',
    },
    {
        'name': 'Nuevo auditorio',
        'user': 'Thespianartist',
        'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
        'picture': 'https://picsum.photos/200/200/?image=1076',
    }
]


def list_recipes(request):
    """List existing recipes."""

    return render(request,'feed.html', {'posts':posts})


 
 
class Recipes(View):
    # Especifico la plantilla o template que usaré 
    template_name = "index.html"

    # Llamo los datos que se encuentran en la tabla 'recipes' 
    datos = get_recipes()

    # Envio los datos de la tabla 'recipes' a la vista o template 
    def get(self, request): 
        return render(request, self.template_name, { "recipes": self.datos})