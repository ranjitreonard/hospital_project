from django.conf import settings
from django.db import models
from django.utils import timezone

MEDICINE_TYPE = {
    ('Syrup', 'Syrup'),
    ('Capsule', 'Capsule'),
    ('Tablet', 'Tablet')
}


class Medicine(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    medicine_type = models.CharField(max_length=100, blank=True, null=True, choices=MEDICINE_TYPE)
    manufacturer = models.CharField(max_length=200, blank=True, null=True)
    manufacture_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    prescribed_medicines = models.ManyToManyField('PrescribedMedicine', related_name='medicine_prescribed_medicines',
                                                  blank=True)
    cost_price_per_unit = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    no_in_box = models.IntegerField(blank=True, null=True, default=0)
    cost_price_per_box = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    accumulated_boxes_bought = models.IntegerField(blank=True, null=True, default=0)
    boxes_bought = models.IntegerField(blank=True, null=True, default=0)
    total_cost = models.DecimalField(max_digits=10, blank=True, null=True, decimal_places=2)
    accumulated_total_cost = models.DecimalField(max_digits=10, blank=True, null=True, decimal_places=2)
    selling_price_per_unit = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    selling_price_per_box = models.DecimalField(blank=True, null=True, default=0, max_digits=10, decimal_places=2)
    sold_units = models.IntegerField(blank=True, null=True, default=0)
    sold_boxes = models.IntegerField(blank=True, null=True, default=0)
    total_sales = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
    units_left = models.IntegerField(blank=True, null=True, default=0)
    boxes_left = models.IntegerField(blank=True, null=True, default=0)
    total_no_units_accumulated = models.IntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='medicines',
                                   blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'medicine'


class PrescribedMedicine(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.SET_NULL, related_name='prescribed_medicine_prescription',
                                 blank=True, null=True)
    prescription = models.ForeignKey('Prescription', on_delete=models.SET_NULL,
                                     related_name='prescribed_medicine_prescription', blank=True, null=True)
    dosage = models.CharField(max_length=2000, blank=True, null=True)
    frequency = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   related_name='prescribed_medicines',
                                   blank=True, null=True)

    def __str__(self):
        return str(self.medicine.name)

    class Meta:
        db_table = 'prescribed_medicines'


PRES_STATUS = {
#     (1, 'Paid'),
#     (0, 'Unpaid')
    (1, 'Confirmed'),
    (0, 'Pending')
 }


class Prescription(models.Model):
    prescription_id = models.CharField(max_length=200, blank=True, null=True)
    medicines = models.ManyToManyField(PrescribedMedicine, related_name='prescription_medicines', blank=True)
    patient = models.ForeignKey('management.Patient', on_delete=models.SET_NULL, related_name='prescription_patient',
                                blank=True, null=True)
    treatment = models.ForeignKey('management.Treatment', on_delete=models.SET_NULL,
                                  related_name='prescription_treatment' , blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True, choices=PRES_STATUS)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='prescriptions',
                                   blank=True, null=True)

    def __str__(self):
        return str(self.prescription_id)

    class Meta:
        db_table = 'prescriptions'


class Expenditure(models.Model):
    item = models.CharField(max_length=200, blank=True, null=True)
    category = models. CharField(max_length=100, blank=True, null=True)
    medicine = models.ForeignKey('pharmacy.Medicine', on_delete=models.SET_NULL, related_name='expenditure_medicine', blank=True, null=True)
    cost = models.DecimalField(max_digits=10, blank=True, null=True, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='expenditures', blank=True, null=True)

    def __str__(self):
        return f'{self.category}-{self.cost}'

    class Meta:
        db_table = 'expenditure'