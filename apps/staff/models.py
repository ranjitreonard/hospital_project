from random import randrange

from django.conf import settings
from django.db import models
from django.utils import timezone
from apps.management.models import Complaint

MARITAL = {
    ('Married', 'Married'),
    ('Single', 'Single'),
    ('Divorced', 'Divorced'),
    ('Widowed', 'Widowed'),
}


class Staff(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='staff_user', blank=True,
                             null=True)
    number_of_days_left = models.IntegerField(blank=True, null=True, default=0)
    total_number_of_days = models.IntegerField(blank=True, null=True, default=0)
    leaves = models.ManyToManyField('Leave', related_name='staff_leaves', blank=True)
    leave_period = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                     related_name='staff_leave_period', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    number_of_days_used = models.IntegerField(blank=True, null=True, default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='staffs',
                                   blank=True, null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        db_table = 'staff'


LEAVE_STATUS = {
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
}


class Leave(models.Model):
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='leave_staff',
                              blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(blank=True, null=True, choices=LEAVE_STATUS, max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='leaves',
                                   blank=True, null=True)
    number_of_days = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return f'{self.start_date} - {self.end_date}'

    class Meta:
        db_table = 'leave'
        get_latest_by = 'created_at'
