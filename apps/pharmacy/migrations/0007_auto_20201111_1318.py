# Generated by Django 3.1.2 on 2020-11-11 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0006_expenditure_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='dosage',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='frequency',
        ),
        migrations.AddField(
            model_name='prescribedmedicine',
            name='dosage',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='prescribedmedicine',
            name='frequency',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='medicine_type',
            field=models.CharField(blank=True, choices=[('Tablet', 'Tablet'), ('Syrup', 'Syrup'), ('Capsule', 'Capsule')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='status',
            field=models.IntegerField(blank=True, choices=[(0, 'Pending'), (1, 'Confirmed')], null=True),
        ),
    ]