# Generated by Django 3.1.2 on 2020-11-10 11:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('staff', '0001_initial'),
        ('management', '0022_auto_20201109_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Resolved', 'Resolved'), ('Canceled', 'Canceled')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(blank=True, choices=[('Female', 'Female'), ('Male', 'Male')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='marital_status',
            field=models.CharField(blank=True, choices=[('Single', 'Single'), ('Widowed', 'Widowed'), ('Married', 'Married'), ('Divorced', 'Divorced')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='department',
            field=models.CharField(blank=True, choices=[('HR', 'Human Resource'), ('Pharmacy', 'Pharmacy'), ('Account', 'Account'), ('Ward', 'Ward'), ('Management', 'Management')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.IntegerField(blank=True, choices=[(0, 'Pending'), (2, 'Rejected'), (1, 'Accepted')], null=True),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], max_length=100, null=True),
        ),
        migrations.AlterModelTable(
            name='request',
            table='requests',
        ),
        migrations.CreateModel(
            name='LeavePeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('number_of_days', models.IntegerField(blank=True, default=0, null=True)),
                ('days_allocated', models.IntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leave_periods', to=settings.AUTH_USER_MODEL)),
                ('staffs', models.ManyToManyField(blank=True, related_name='staff_leave', to='staff.Staff')),
            ],
            options={
                'db_table': 'leave_period',
            },
        ),
    ]
