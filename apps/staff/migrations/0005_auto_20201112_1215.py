# Generated by Django 3.1.2 on 2020-11-12 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0004_auto_20201112_1212'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leave',
            options={},
        ),
        migrations.AlterField(
            model_name='leave',
            name='status',
            field=models.CharField(blank=True, choices=[('Rejected', 'Rejected'), ('Pending', 'Pending'), ('Approved', 'Approved')], max_length=200, null=True),
        ),
    ]
