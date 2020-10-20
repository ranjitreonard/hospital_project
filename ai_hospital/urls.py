"""ai_hospital URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.views.generic import TemplateView
from apps.management import urls as manage_urls
from apps.department import urls as department_urls
from apps.portal import urls as portal_urls
from apps.pharmacy import urls as pharmacy_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(), name='login'),
    path('apps/', TemplateView.as_view(template_name='user/apps.html'), name='apps'),
    path('layout/', TemplateView.as_view(template_name='layouts/admin_layout.html'), ),
    path('administration/', include(manage_urls, namespace='management'),),
    path('department/', include(department_urls, namespace='department')),
    path('portal/', include(portal_urls, namespace='portal')),
    path('pharmacy/', include(pharmacy_urls, namespace='pharmacy')),

]
