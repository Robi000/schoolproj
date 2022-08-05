# Generated by Django 4.0.5 on 2022-08-03 12:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system2', '0002_class_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='Backup_phone_no',
            field=models.CharField(max_length=50, null=True, validators=[django.core.validators.RegexValidator(message='Phone number must be in correct form +2519xxxxxxxx', regex='^\\+?0?\\d{10,13}$')]),
        ),
        migrations.AddField(
            model_name='student',
            name='Father_full_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='mother_full_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='phone_no',
            field=models.CharField(max_length=50, null=True, validators=[django.core.validators.RegexValidator(message='Phone number must be in correct form +2519xxxxxxxx', regex='^\\+?0?\\d{10,13}$')]),
        ),
        migrations.AddField(
            model_name='student',
            name='vaccinated',
            field=models.BooleanField(default=False),
        ),
    ]
