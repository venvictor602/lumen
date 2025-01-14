# Generated by Django 5.0.7 on 2024-11-23 20:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admissions', '0005_student_year_of_entry'),
        ('result', '0002_delete_classposition'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(choices=[('First Term', 'First Term'), ('Second Term', 'Second Term'), ('Third Term', 'Third Term')], max_length=20)),
                ('average_score', models.FloatField(default=0, editable=False)),
                ('position', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admissions.class')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admissions.student')),
            ],
        ),
    ]
