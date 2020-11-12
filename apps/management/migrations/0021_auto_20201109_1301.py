# Generated by Django 3.1.2 on 2020-11-09 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0020_auto_20201109_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='comment',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='status',
            field=models.CharField(blank=True, choices=[('Resolved', 'Resolved'), ('Canceled', 'Canceled'), ('Pending', 'Pending')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='marital_status',
            field=models.CharField(blank=True, choices=[('Single', 'Single'), ('Widowed', 'Widowed'), ('Married', 'Married'), ('Divorced', 'Divorced')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='description',
            field=models.TextField(blank=True, choices=[('Pharmacy', 'Pharmacy'), ('HR', 'Human Resource'), ('Account', 'Account'), ('Ward', 'Ward'), ('Management', 'Management')], max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.IntegerField(blank=True, choices=[(2, 'Rejected'), (1, 'Accepted'), (0, 'Pending')], null=True),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='status',
            field=models.CharField(blank=True, choices=[('Completed', 'Completed'), ('Canceled', 'Canceled'), ('Pending', 'Pending')], max_length=100, null=True),
        ),
    ]