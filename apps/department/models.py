from django.conf import settings
from django.db import models
from django.utils import timezone


class Note(models.Model):
    note = models.TextField(max_length=3000, blank=True, null=True)
    patient = models.ForeignKey('management.Patient', on_delete=models.SET_NULL, related_name='note_patient', blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, related_name='notes', blank=True, null=True )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.note

    class Meta:
        db_table = 'note'
