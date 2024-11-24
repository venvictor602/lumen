from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

class Class(models.Model):
    name = models.CharField(max_length=100)  # e.g., "JSS1", "JSS2", etc.
    level = models.IntegerField(null=True, blank=True)  # e.g., 1 for JSS1, 2 for JSS2, etc.

    def __str__(self):
        return self.name

    def get_next_class(self):
        """
        Get the next class in the sequence (e.g., from JSS1 to JSS2).
        If the current class is the last class, return None.
        """
        next_class = Class.objects.filter(level=self.level + 1).first()
        return next_class

from datetime import datetime
class Student(models.Model):
    """Represents a student with admission, account, and class details."""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    student_code = models.CharField(max_length=20, unique=True, null=True, blank=True)  # For result integration
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=15)
    year_of_entry = models.DateField(default=datetime.now)  # Automatically set to current date
    address = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('graduate', 'Graduate')],
        default='Pending'
    )
    application_date = models.DateTimeField(auto_now_add=True)
    user_account = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    class_id = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)  # Link to class

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_code or 'No Code'})"

    def create_user_account(self):
        """
        Creates a user account for the student upon acceptance and sends login details via email.
        """
        if self.status == 'Accepted' and not self.user_account:
            # Generate a random student code if it doesn't exist
            if not self.student_code:
                self.student_code = get_random_string(8, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            
            # Generate a random 6-character password
            password = get_random_string(6, 'abcdefghijklmnopqrstuvwxyz0123456789')

            # Create a User account
            user = User.objects.create_user(
                username=self.email,
                password=password,
                email=self.email,
                first_name=self.first_name,
                last_name=self.last_name
            )

            # Link the user account to the student
            self.user_account = user
            self.save()

            # Send email to the student with their login details
            send_mail(
                'Admission Approved - Your Login Details',
                f'Hello {self.first_name},\n\nYour admission has been approved! '
                f'You can log in with the following credentials:\n\n'
                f'Username: {self.email}\nPassword: {password}\n\n'
                f'Student Code: {self.student_code}\n\n'
                f'Please change your password after logging in.',
                'admin@school.com',  # Replace with your actual sender email
                [self.email],
                fail_silently=False,
            )
