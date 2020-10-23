from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import *
from apps.department.forms import NewPatientForm
from . import forms
from apps.management.models import Patient, MedicalDiagnosis, Treatment
from .models import Note

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

    def get_context_data(self, **kwargs):
        context = super(PatientDetails, self).get_context_data(**kwargs)
        context['age'] = round((timezone.now().date()- self.object.date_of_birth).days / 365)
        return context

@login_required()
def vital_signs(request, id):
    patient = Patient.objects.get(id=id)
    weight = request.POST.get('weight')
    sys = request.POST.get('sys')
    dias = request.POST.get('dias')
    respiration = request.POST.get('respiration')
    temperature = request.POST.get('temperature')

    bp = sys + ' / ' + dias #or  f"{sys} / {dias}"
    if request.method == 'POST':
        patient.weight = weight + ' kg'
        patient.bp = bp + ' mmHg'
        patient.respiration = respiration + ' cpm'
        patient.temperature = temperature + ' °C'
        patient.patient_type = 'OPD'

    patient.save()

    return HttpResponseRedirect(reverse_lazy('department:patient-details', kwargs={'id': patient.id}))


class VitalSigns(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('department:patient-details', kwargs={'id':kwargs.get('id')})

    def post(self, request, *args, **kwargs):
        patient = Patient.objects.get(id=kwargs.get('id'))
        weight = request.POST.get('weight')
        sys = request.POST.get('sys')
        dias = request.POST.get('dias')
        respiration = request.POST.get('respiration')
        temperature = request.POST.get('temperature')

        bp = sys + ' / ' + dias  # or  f"{sys} / {dias}"
        patient.weight = weight + ' kg'
        patient.bp = bp + ' mmHg'
        patient.respiration = respiration + ' cpm'
        patient.temperature = temperature + ' °C'
        patient.patient_type = 'OPD'
        patient.save()
        return super(VitalSigns, self).post(self, request, *args, **kwargs)


class OPDPatients(LoginRequiredMixin, ListView):
    template_name = 'department/opd.html'
    queryset = Patient.objects.filter(patient_type='OPD')
    model = Patient


class PatientDiagnosis(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('department:patient-details', kwargs={'id': kwargs.get('id')})

    def post(self, request, *args, **kwargs):
        patient = Patient.objects.get(id=kwargs.get('id'))
        complaints = request.POST.get('complaints')
        symptoms = request.POST.get('symptoms')
        diagnosis = request.POST.get('diagnosis')
        is_admitted = request.POST.get('is_admitted')
        onset = request.POST.get('onset')
        treatment = request.POST.get('treatment')
        prescription = request.POST.get('prescription')

        if is_admitted == "True":
            admitted = True
        else:
            admitted = False

        md = MedicalDiagnosis.objects.create(
            patient=patient,
            complaints=complaints,
            diagnosis=diagnosis,
            is_admitted=admitted,
            onset=onset,

        )
        tmt = Treatment.objects.create(
            diagnosis=md,
            treatment=treatment,
            status='Pending',
            created_by=self.request.user,
            prescription=prescription,
        )

        md.treatments.add(tmt)
        if admitted:
            patient.patient_type = 'Ward'

        patient.diagnoses.add(md)

        md.save()
        patient.save()

        return super(PatientDiagnosis, self).post(self, request, *args, **kwargs)


@login_required()
def patient_note(request, id):
    patient = Patient.objects.get(id=id)
    note = request.POST.get('note')

    my_note = Note.objects.create(
        note=note,
        patient=patient,
        created_by=request.user
    )

    patient.notes.add(my_note)
    patient.save()
    return redirect(reverse_lazy('department:patient-details', kwargs={'id': id}))


@login_required()
def add_treatment(request, diagnosis_id, patient_id):
    diagnosis = MedicalDiagnosis.objects.get(id=diagnosis_id)
    patient = Patient.objects.get(id=patient_id)
    treatment = request.POST.get('treatment')
    prescription = request.POST.get('prescription')

    my_treatment = Treatment.objects.create(
        diagnosis=diagnosis,
        treatment=treatment,
        prescription=prescription,
        status='Pending',
        created_by=request.user
    )
    diagnosis.treatments.add(my_treatment)
    diagnosis.save()

    return redirect(reverse_lazy('department:patient-details', kwargs={'id': patient.id}))

@login_required()
def complete_treatment(request, treatment_id, patient_id):
    treatment = Treatment.objects.get(id=treatment_id)
    patient = Patient.objects.get(id=patient_id)
    time_completed = request.POST.get('time_completed')
    date_completed = request.POST.get('date_completed')

    treatment.time_treated = time_completed
    treatment.date_treated = date_completed
    treatment.status = 'Completed'

    treatment.save()
    return redirect(reverse_lazy('department:patient-details', kwargs={'id':patient.id}))


class CancelTreatment(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('department:patient-details', kwargs={'id': kwargs.get('patient_id')})

    def get(self, request, *args, **kwargs):
        treatment = Treatment.objects.get(id=kwargs.get('treatment_id'))

        if treatment.status == "Pending":
            treatment.status = "Cancelled"

        treatment.save()

        return super(CancelTreatment, self).get(self, request, *args, **kwargs)
