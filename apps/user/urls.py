from django.urls import *

app_name = 'user'

urlpatterns = [
    path('', include('django.contrib.auth.urls') )
]