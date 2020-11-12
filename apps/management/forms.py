from django.forms import *
import datetime

from apps.user.models import *
from .models import *


class UserForm(ModelForm):
    password = CharField(widget=PasswordInput(attrs={'required': True}), label='Password')

    class Meta:
        model = User
        fields = ('staff_id', 'first_name', 'last_name','user_type', 'role', 'password')

    def clean_staff_id(self):
        staff_id = self.cleaned_data.get('staff_id')

        try:
            User.objects.get(staff_id=staff_id)
            raise ValidationError('Staff with this staff id already exist')
        except User.DoesNotExist:
            pass

        return staff_id

    class WardForm(ModelForm):


        class Meta:
            model = Ward
            fields = ('label',)


class LeavePeriodForm(ModelForm):
    class Meta:
        model = LeavePeriod
        fields = ('start_date', 'end_date', 'days_allocated')
        widgets = {
            'start_date': DateInput(attrs={'type': 'date', 'required': True}),
            'end_date': DateInput(attrs={'type': 'date', 'required': True})
        }

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        date1 = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    
        try:
            LeavePeriod.objects.get(end_date__year=date1.year)
            # raise error if try passes
            raise ValidationError('This Leave Period already exists')
        except LeavePeriod.DoesNotExist:
            pass

        return end_date