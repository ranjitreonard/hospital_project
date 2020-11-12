from django.urls import path
from .views import *

app_name = 'staff'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    # path('complaint/', create_complaint, name='complaint'),
    path('complaint/add/', add_complaint, name='add-complaint'),
    path('complaint/cancel/<id>/', cancel_complaint, name='cancel'),


]