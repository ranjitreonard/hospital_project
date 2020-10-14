from django.urls import path
from .views import *

app_name = 'management'


urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('staff/', staff_list, name='staff'),
    path('staff/add/', AddStaff.as_view(), name='staff-add'),
]