# Generated by Django 4.0.5 on 2022-08-03 12:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system1', '0003_user_phone_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_no',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Phone number must be in correct form +2519xxxxxxxx', regex='^\\+?0?\\d{10,13}$')]),
        ),
    ]
