from django.contrib import admin
from  .models import *
# Register your models here.
admin.site.register(Medicine)
admin.site.register(PrescribedMedicine)
admin.site.register(Prescription)