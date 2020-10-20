from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from apps.management.forms import UserForm
from apps.user.models import User




@login_required()
def dashboard(request):
    return render(request=request, template_name='pharmacy/dashboard.html')


