# Generated by Django 5.0.7 on 2024-11-23 18:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admissions', '0004_alter_student_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='year_of_entry',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
