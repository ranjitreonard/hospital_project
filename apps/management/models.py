from random import randrange
from django.db import models
from django.conf import settings
from django.utils import timezone


class Ward(models.Model):
    label = models.CharField(max_length=100, blank=True, null=True)
    incharge = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='ward_incharge',
                                 blank=True, null=True)
    beds = models.ManyToManyField('Bed', related_name='ward_beds', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='wards',
                                   blank=True, null=True)
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
    status = models.CharField(max_length=100, blank=True, null=True, choices=BED_STATUS)
    allocate = models.ForeignKey('BedAllocate', on_delete=models.SET_NULL, related_name='bed_allocate', blank=True,
                                 null=True)
    bed_allocates = models.ManyToManyField('BedAllocate', related_name='bed_bed_allocates', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='beds', blank=True,
                                   null=True)

    def __str__(self):
        return self.number

    class Meta:
        db_table = 'bed'
        ordering = ('number',)


class BedAllocate(models.Model):
    bed = models.ForeignKey(Bed, on_delete=models.SET_NULL, related_name='bed_allocate_bed', blank=True, null=True)
    patient = models.ForeignKey('Patient', on_delete=models.SET_NULL, related_name='bed_allocate_patient', blank=True,
                                null=True)
    date_admitted = models.DateField(blank=True, null=True)
    time_admitted = models.TimeField(blank=True, null=True)
    date_discharged = models.DateField(blank=True, null=True)
    time_discharged = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='bed_allocates',
                                   blank=True, null=True)

    def __str__(self):
        return f"{self.bed} - {self.patient}"

    class Meta:
        db_table = 'bed_allocate'


def generate():
    FROM = '0123456789'
    LENGTH = 10
    pat_id = ""
    for i in range(LENGTH):
        pat_id += FROM[randrange(0, len(FROM))]
    return f'PT{pat_id}/{timezone.now().year}'


GENDER = {
    ('Male', 'Male'),
    ('Female', 'Female'),
}

PATIENT_TYPE = {
    ('OPD', 'OPD'),
    ('WARD', 'Ward'),
    ('ER', 'Emergency'),
    ('Discharged', 'Discharged'),
}

MARITAL = {
    ('Married', 'Married'),
    ('Single', 'Single'),
    ('Divorced', 'Divorced'),
    ('Widowed', 'Widowed'),
}


class Patient(models.Model):
    patient_id = models.CharField(default=generate, unique=True, editable=False, max_length=100, )
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    patient_type = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True, choices=GENDER)
    marital_status = models.CharField(max_length=100, blank=True, null=True, choices=MARITAL)
    date_of_birth = models.DateField(blank=True, null=True)
    date_admitted = models.DateField(blank=True, null=True)
    time_admitted = models.TimeField(blank=True, null=True)
    date_discharged = models.DateField(blank=True, null=True)
    time_discharged = models.TimeField(blank=True, null=True)
    bed = models.ForeignKey(Bed, on_delete=models.SET_NULL, related_name='patient_bed', blank=True, null=True)
    weight = models.CharField(max_length=10, null=True, blank=True)
    bp = models.CharField(max_length=100, null=True, blank=True)
    respiration = models.CharField(max_length=100, null=True, blank=True)
    temperature = models.CharField(max_length=100, null=True, blank=True)
    diagnoses = models.ManyToManyField('MedicalDiagnosis', related_name='patient_diagnoses', blank=True)
    notes = models.ManyToManyField('department.Note', related_name='patient_notes', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='patients',
                                   blank=True, null=True)

    def __str__(self):
        return self.patient_id

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = 'patient'


class MedicalDiagnosis(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, related_name='diagnosis_patient', blank=True,
                                null=True)
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
    diagnosis = models.ForeignKey(MedicalDiagnosis, on_delete=models.SET_NULL,
                                  related_name='treatment_diagnosis', blank=True, null=True)
    treatment = models.CharField(max_length=1000, null=True, blank=True)
    prescription = models.CharField(max_length=2000, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True, choices=TREATMENT_STATUS)
    comment = models.CharField(blank=True, null=True, max_length=100)
    time_treated = models.TimeField(blank=True, null=True)
    date_treated = models.DateField(blank=True, null=True)
    pharmacy_prescription = models.ForeignKey('pharmacy.Prescription', on_delete=models.SET_NULL,
                                              related_name='treatment_prescription', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='treatment',
                                   blank=True, null=True)

    def __str__(self):
        return f"{self.treatment} - {self.prescription}"

    class Meta:
        db_table = 'treatment'
        ordering = ('-created_at',)


COMPLAINTS_STATUS = {
    ('Pending', 'Pending'),
    ('Canceled', 'Canceled'),
    ('Resolved', 'Resolved'),
}


class Complaint(models.Model):
    complaint = models.CharField(max_length=3000, blank=True, null=True)
    status = models.CharField(blank=True, null=True, choices=COMPLAINTS_STATUS, max_length=100)
    review = models.CharField(blank=True, null=True, max_length=3000)
    seen_at = models.DateTimeField(blank=True, null=True)
    seen_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='complaints_seen_by',
                                blank=True, null=True)
    seen = models.BooleanField(blank=True, null=True, default=False)
    created_at = models.DateTimeField(default=timezone.now)
    review_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                  related_name='complaints_review_by', blank=True, null=True)
    review_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='complaints',
                                   blank=True, null=True)

    def __str___(self):
        return str(self.complaint)

    class Meta:
        db_table = 'complaint'
        ordering = ('-created_at',)


class Leave(models.Model):
    leave = models.CharField(max_length=3000, blank=True, null=True)


DEPARTMENTS = {
    ('Ward', 'Ward'),
    ('Pharmacy', "Pharmacy"),
    ('Account', 'Account'),
    ('Management', 'Management'),
    ('HR', 'Human Resource'),
}

REQUEST_STATUS = {
    (0, 'Pending'),
    (1, 'Accepted'),
    (2, 'Rejected'),
}


class Request(models.Model):
    department = models.CharField(max_length=200, null=True, blank=True, choices=DEPARTMENTS)
    description = models.TextField(max_length=5000, blank=True, null=True)
    comment = models.CharField(max_length=1000, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True, choices=REQUEST_STATUS)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='requests',
                                   blank=True, null=True)

    def __str__(self):
        return str(self.department)

    class Meta:
        db_table = 'requests'


class LeavePeriod(models.Model):
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    number_of_days = models.IntegerField(blank=True, null=True, default=0)
    days_allowed = models.IntegerField(blank=True, null=True, default=0)
    staffs = models.ManyToManyField('staff.Staff', related_name='staff_leave', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='leave_periods',
                                   blank=True, null=True)

    def __str__(self):
        return f"{self.start_date} -  {self.end_date}"

    class Meta:
        db_table = 'leave_period'
