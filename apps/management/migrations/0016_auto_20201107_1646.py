# Generated by Django 3.1.2 on 2020-11-07 16:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '0015_auto_20201106_1121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave', models.CharField(blank=True, max_length=3000, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='complaint',
            old_name='response',
            new_name='review',
        ),
        migrations.AddField(
            model_name='complaint',
            name='review_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='complaint',
            name='review_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='complaints_review_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='complaint',
            name='seen_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='complaint',
            name='seen_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='complaints_seen_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='seen',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='status',
            field=models.CharField(blank=True, choices=[('Canceled', 'Canceled'), ('Resolved', 'Resolved'), ('Pending', 'Pending')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='marital_status',
            field=models.CharField(blank=True, choices=[('Divorced', 'Divorced'), ('Widowed', 'Widowed'), ('Married', 'Married'), ('Single', 'Single')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='status',
            field=models.CharField(blank=True, choices=[('Canceled', 'Canceled'), ('Completed', 'Completed'), ('Pending', 'Pending')], max_length=100, null=True),
        ),
    ]
