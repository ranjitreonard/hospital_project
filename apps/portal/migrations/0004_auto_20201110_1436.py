# Generated by Django 3.1.2 on 2020-11-10 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_auto_20201103_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='bill_type',
            field=models.CharField(blank=True, choices=[('CB', 'Card Bills'), ('WB', 'Ward Bills'), ('LB', 'Lab Bills'), ('PhB', 'Pharmacy Bills'), ('CnB', 'Consultation Bills'), ('PB', 'Procedure Bills')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='defaultbill',
            name='bill_type',
            field=models.CharField(blank=True, choices=[('CB', 'Card Bills'), ('WB', 'Ward Bills'), ('LB', 'Lab Bills'), ('PhB', 'Pharmacy Bills'), ('CnB', 'Consultation Bills'), ('PB', 'Procedure Bills')], max_length=100, null=True),
        ),
    ]
