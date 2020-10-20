from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *

from apps.department.forms import NewPatientForm
from . import forms
from apps.management.models import Patient



@login_required()
def dashboard(request):
    return render(request=request, template_name='department/dashboard.html')


class NewPatient(LoginRequiredMixin, CreateView):
    template_name = 'department/new_patient.html'
    form_class = NewPatientForm
    queryset = Patient.objects.all()
    success_url = reverse_lazy('department:patients')

    def form_valid(self, form):
        valid = super(NewPatient, self). form_valid(form)

        form.instance.created_by = self.request.user
        form.save()

        return valid


class Patients(LoginRequiredMixin, ListView):
    template_name = 'department/patients.html'
    queryset = Patient.objects.all()
    model = Patient


class PatientDetails(LoginRequiredMixin, DetailView):
    template_name = 'department/patient_details.html'
    model = Patient
    queryset = Patient.objects.all()
    pk_url_kwarg = 'id'
