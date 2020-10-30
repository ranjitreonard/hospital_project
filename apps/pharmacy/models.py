from django.db import models


class Medicine(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True)
    prod_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)


class MedicationPrice(models.Model):
    unit_price = models.IntegerField(null=True, blank=True)
    units_per_box = models.IntegerField(null=True, blank=True)
    number_of_boxes = models.IntegerField(null=True, blank=True)

