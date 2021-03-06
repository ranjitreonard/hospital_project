# Generated by Django 3.1.2 on 2020-10-20 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_auto_20201020_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='marital_status',
            field=models.CharField(blank=True, choices=[('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed'), ('Single', 'Single')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='status',
            field=models.CharField(blank=True, choices=[('Completed', 'Completed'), ('Canceled', 'Canceled'), ('Pending', 'Pending')], max_length=100, null=True),
        ),
    ]
