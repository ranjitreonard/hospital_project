from django.forms import *
from apps.management import models
from apps.management.models import Ward
from apps.portal.models import DefaultBill


class NewPatientForm(ModelForm):
    class Meta:
        model = models.Patient
        fields = ('first_name', 'last_name', 'gender', 'marital_status', 'date_of_birth')
        widgets = {
            'date_of_birth': TextInput(attrs={
                'type': 'date'
            })
        }

    def clean(self):
        try:
            card_charge = DefaultBill.objects.get(bill_type='CB')

        except DefaultBill.DoesNotExist:
            raise ValidationError(
                message='There is no card bills in the system'
            )

        return self.cleaned_data