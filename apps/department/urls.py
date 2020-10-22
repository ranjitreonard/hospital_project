from django.urls import path
from .views import *

app_name = 'department'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('patients/', Patients.as_view(), name='patients'),
    path('patients/add/', NewPatient.as_view(), name='add-patient'),
    path('patient/<id>/', PatientDetails.as_view(), name='patient-details'),
    path('patient/vital-signs/<id>/', vital_signs, name='vital-signs'),
    path('opd/', OPDPatients.as_view(), name='opd'),
    path('patient/diagnosis/add/<id>/', PatientDiagnosis.as_view(), name='add-diagnosis')
]
