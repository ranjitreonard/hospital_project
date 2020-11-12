from django.urls import path
from .views import *

app_name = 'portal'


urlpatterns = [
    path('dashboard/', dashboard, name='portal'),
    path('portal/', portal_layout, name='portal_layout'),
    path('bills/', Bills.as_view(), name='bills'),
    path('bill/payment/confirm/<uuid>/<patient_id>/', ConfirmPayment.as_view(), name='confirm-payment'),
    path('patient/card/<id>/', PatientCard.as_view(), name='patient-card'),
    path('patient/discharge/confirm/<uuid>/', ConfirmDischarge.as_view(), name='confirm-discharge'),
    path('bill/<uuid>/', bill_details, name='bill-details'),
]
