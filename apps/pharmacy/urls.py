from django.urls import path
from .views import  *

app_name= 'pharmacy'


urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
]