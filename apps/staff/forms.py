from django.forms import *
from apps.management import models


# class NewComplaintForm(ModelForm):
#
#     class Meta:
#         model = models.Complaint
#         fields = ('complaint',)
#         widgets = {
#             'complaint': forms.Textarea(attrs={'required': True, 'rows': 1, 'class': 'form-control border-0',
#                                                'placeholder': 'Type Complaints Here', 'autofocus':True})
#         }
