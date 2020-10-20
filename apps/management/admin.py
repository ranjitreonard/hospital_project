from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Ward)
admin.site.register(Bed)
admin.site.register(Patient)
admin.site.register(BedAllocate)
admin.site.register(MedicalDiagnosis)
admin.site.register(Treatment)


