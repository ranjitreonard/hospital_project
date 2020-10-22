from random import randrange
from django.db import models
from django.conf import settings
from django.utils import timezone


class Ward(models.Model):
    label = models.CharField(max_length=100, blank=True, null=True)
    incharge = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='ward_incharge', blank=True, null=True)
    beds = models.ManyToManyField('Bed', related_name='ward_beds', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='wards', blank=True, null=True)
    patients = models.ManyToManyField('Patient', related_name='ward_patients', blank=True)

    def __str__(self):
        return self.label

    class Meta:
        db_table = 'ward'


BED_STATUS = {
    ('Assigned', 'Assigned'),
    ('Unassigned', 'Unassigned')
}



class Bed(models.Model):
    number = models.CharField(max_length=10, blank=True, null=True)
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, related_name='bed_ward', blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True,choices=BED_STATUS)
    allocate = models.ForeignKey('BedAllocate', on_delete=models.SET_NULL, related_name='bed_allocate', blank=True, null=True)
    bed_allocates = models.ManyToManyField('BedAllocate', related_name='bed_bed_allocates', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='beds', blank=True, null=True)

    def __str__(self):
        return self.number

    class Meta:
        db_table = 'bed'


class BedAllocate(models.Model):
    bed = models.ForeignKey(Bed, on_delete=models.SET_NULL, related_name='bed_allocate_bed', blank=True, null=True)
    patient = models.ForeignKey('Patient', on_delete=models.SET_NULL, related_name='bed_allocate_patient', blank=True, null=True)
    admitted_at = models.DateField(blank=True, null=True)
    discharged_at = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name= 'bed_allocates', blank=True, null=True)

    def __str__(self):
        return f"{self.bed} - {self.patient}"

    class Meta:
        db_table = 'bed_allocate'


def generate():
    FROM = '0123456789'
    LENGTH = 10
    pat_id = ""
    for i in range(LENGTH):
        pat_id +=  FROM[randrange(0, len(FROM))]
    return f'PT{ pat_id}/{timezone.now().year}'



GENDER = {
    ('Male', 'Male'),
    ('Female', 'Female'),
}


PATIENT_TYPE = {
    ('OPD', 'OPD'),
    ('WARD', 'Ward'),
    ('ER', 'Emergency')
}

MARITAL = {
    ('Married', 'Married'),
    ('Single', 'Single'),
    ('Divorced', 'Divorced'),
    ('Widowed', 'Widowed'),
}


class Patient(models.Model):
    patient_id = models.CharField(default=generate, unique=True, editable=False, max_length=100,)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    patient_type = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True, choices=GENDER)
    marital_status = models.CharField(max_length=100, blank=True, null=True, choices=MARITAL)
    date_of_birth = models.DateField(blank=True, null=True)
    admitted_at = models.DateTimeField(blank=True, null=True)
    discharge_at = models.DateTimeField(blank=True,null=True)
    weight = models.CharField(max_length=10, null=True, blank=True)
    bp = models.CharField(max_length=100, null=True, blank=True)
    respiration = models.CharField(max_length=100, null=True, blank=True)
    temperature = models.CharField(max_length=100,null=True, blank=True)
    diagnoses = models.ManyToManyField('MedicalDiagnosis', related_name='patient_diagnoses', blank=True)
    notes = models.ManyToManyField('department.Note',related_name='patient_notes',blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='patients', blank=True, null=True)


    def __str__(self):
        return self.patient_id

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = 'patient'



class MedicalDiagnosis(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL,related_name='diagnosis_patient', blank=True, null=True)
    diagnosis = models.CharField(max_length=100, blank=True, null=True)
    is_admitted = models.BooleanField(blank=True, null=True)
    onset = models.CharField(max_length=100, blank=True, null=True)
    treatments = models.ManyToManyField('Treatment', related_name='diagnosis_treatments', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='diagnoses',
                                   blank=True, null=True)
    complaints = models.CharField(blank=True, null=True, max_length=2000)
    symptoms = models.CharField(blank=True, null=True, max_length=2000)

    def __str__(self):
        return self.diagnosis

    class Meta:
        db_table = 'medical_diagnosis'
        ordering = ('-created_at',)


TREATMENT_STATUS = {
    ('Pending', 'Pending'),
    ('Canceled', 'Canceled'),
    ('Completed', 'Completed')

}

class Treatment(models.Model):
    diagnosis = models.ForeignKey(MedicalDiagnosis, on_delete=models.SET_NULL, related_name='treatment_diagnosis', blank=True, null=True)
    treatment = models.CharField(max_length=1000, null=True, blank=True)
    prescription = models.CharField(max_length=2000, blank=True,null=True)
    status = models.CharField(max_length=100, blank=True, null=True, choices=TREATMENT_STATUS)
    comment = models.CharField(blank=True, null=True, max_length=100)
    time_treated = models.TimeField(blank=True, null=True)
    date_treated = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,related_name='treatment', blank=True, null=True)


    def __str__(self):
        return f"{self.treatment} -  {self.prescription}"

    class Meta:
        db_table = 'treatment'


