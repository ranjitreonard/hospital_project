# Generated by Django 3.1.2 on 2020-11-12 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20201112_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('ACC', 'Accountant'), ('DR', 'Doctor'), ('HM', 'Hospital Manager'), ('CH', 'Cashier'), ('PHM', 'Pharmacy'), ('HR', 'Human Resource'), ('IT', 'IT'), ('NRS', 'Nurse')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(blank=True, choices=[('Suspended', 'Suspended'), ('Leave', 'Leave'), ('Dismissed', 'Dismissed'), ('Active', 'Active')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(blank=True, choices=[('NU', 'Normal Support'), ('AD', 'Administrator'), ('MU', 'Manager'), ('SU', 'Support')], max_length=255, null=True),
        ),
    ]
