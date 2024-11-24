# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.admission_form, name='admission_form'),
    # other routes, such as approval, etc.
]
