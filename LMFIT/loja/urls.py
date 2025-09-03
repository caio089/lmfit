from django.urls import path
from .views import loja

urlpatterns = [
    path('',loja,name='loja'),
]