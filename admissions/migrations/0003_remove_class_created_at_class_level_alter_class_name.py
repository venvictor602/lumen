# Generated by Django 5.0.7 on 2024-11-23 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admissions', '0002_class_student_student_code_student_class_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='created_at',
        ),
        migrations.AddField(
            model_name='class',
            name='level',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='class',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
