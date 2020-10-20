from django.forms import *
from apps.management import models
from apps.management.models import Ward



class NewPatientForm(ModelForm):
    class Meta:
        model = models.Patient
        fields = ('first_name', 'last_name', 'gender', 'marital_status', 'date_of_birth')
        widgets = {
            'date_of_birth':TextInput(attrs={
                'type':'date'
            })
        }

