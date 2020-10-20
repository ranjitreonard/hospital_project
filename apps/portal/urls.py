from django.urls import path
from .views import *

app_name = 'portal'



urlpatterns = [
    path('dashboard/', dashboard, name='portal'),
    path('portal/', portal_layout, name='portal_layout')
]
