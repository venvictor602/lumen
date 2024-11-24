# admissions/admin.py

from django.contrib import admin
from .models import *


@admin.action(description="Move selected students to next class")

def move_to_next_class(modeladmin, request, queryset):
    for student in queryset:
        # Check if the student's status is "accepted"
        if student.status != 'Accepted':
            # Skip this student if not accepted
            modeladmin.message_user(request, f"Student {student} has not been accepted and cannot be moved.")
            continue

        # Get the student's current class
        current_class = student.class_id

        if current_class is None:
            # Skip if the student has no class assigned
            modeladmin.message_user(request, f"Student {student} does not have a valid class.")
            continue

        # Get the next class
        next_class = current_class.get_next_class()

        if next_class:
            # Move the student to the next class
            student.class_id = next_class
            student.save()
            modeladmin.message_user(request, f"Student {student} has been moved to {next_class.name}.")
        else:
            # Inform that the student is already in the last class
            modeladmin.message_user(request, f"Student {student} is already in the last class and cannot be moved.")

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'class_id', 'student_code')
    actions = [move_to_next_class]

admin.site.register(Student, StudentAdmin)

admin.site.register(Class)




