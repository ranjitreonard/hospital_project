# Generated by Django 3.1.2 on 2020-11-09 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='medicine_type',
            field=models.CharField(blank=True, choices=[('Syrup', 'Syrup'), ('Tablet', 'Tablet'), ('Capsule', 'Capsule')], max_length=100, null=True),
        ),
    ]
