from django.conf import settings
from django.db import models
import uuid

from django.utils import timezone

BILL_TYPES = {
    ('WB', 'Ward Bills'),
    ('LB', 'Lab Bills'),
    ('PB', 'Procedure Bills'),
    ('PhB', 'Pharmacy Bills'),
    ('CB', 'Card Bills'),
    ('CnB', 'Consultation Bills'),
}


STATUS = {
    (1, 'Paid'),
    (0, 'Not Paid')
}


class Bill(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    bill_type = models.CharField(max_length=100, blank=True, null=True, choices=BILL_TYPES)
    patient = models.ForeignKey('management.Patient', on_delete=models.SET_NULL, related_name='bill_patient', blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    prescription = models.ForeignKey('pharmacy.Prescription', on_delete=models. SET_NULL,
                                     related_name='bill_prescription', blank=True, null=True)
    number_of_days = models.IntegerField(blank=True, null=True, choices=STATUS)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name='bills', blank=True, null=True)
    status = models.IntegerField(blank=True, null=True, choices=STATUS)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.get_bill_type_display())

    class Met:
        db_table = 'bills'


class DefaultBill(models.Model):
        bill_type = models.CharField(max_length=100, blank=True, null=True, choices=BILL_TYPES)
        service = models.CharField(max_length=200, blank=True, null=True)
        amount = models.DecimalField(decimal_places=2, max_digits=10, blank=True)
        number_of_days = models.IntegerField(blank=True, null=True)
        created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='default_bills', blank=True, null=True)
        created_at = models.DateTimeField(default=timezone.now)

        def __str__(self):
            return '{} - {}'. format(self.get_bill_type_display(), self.amount)

        class Meta:
            db_table = 'default_bill'
            ordering = ('-created_at',)



