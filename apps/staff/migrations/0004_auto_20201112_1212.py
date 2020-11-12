# Generated by Django 3.1.2 on 2020-11-12 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0029_auto_20201112_1212'),
        ('staff', '0003_auto_20201110_1436'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leave',
            options={'get_latest_by': 'created_at'},
        ),
        migrations.AlterModelOptions(
            name='staff',
            options={'get_latest_by': 'created_at'},
        ),
        migrations.AlterField(
            model_name='leave',
            name='status',
            field=models.CharField(blank=True, choices=[('Approved', 'Approved'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='leave_period',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staff_leave_period', to='management.leaveperiod'),
        ),
    ]
