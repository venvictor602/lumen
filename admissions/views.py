# views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib import messages  # Import messages for success notifications

def admission_form(request):
    if request.method == 'POST':
        # Get data from the form manually
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        date_of_birth = request.POST.get('date_of_birth')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')

        # # Validate the data manually
        # if not all([first_name, last_name, email, date_of_birth, contact_number, address]):
        #     return HttpResponse("All fields are required.", status=400)

        # Check if a student with the same email already exists
        if Student.objects.filter(email=email).exists():
            # Add a success message and redirect to the home page
            messages.success(request, "Parent's email aready exist please use another email.")
            return redirect('admission_form')

        # Create and save the new student application with "Pending" status by default
        student = Student(
            first_name=first_name,
            last_name=last_name,
            email=email,
            date_of_birth=date_of_birth,
            contact_number=contact_number,
            address=address,
            status='Pending'
        )
        student.save()

        # Add a success message and redirect to the home page
        messages.success(request, "Thank you! Your application has been submitted.")
        return redirect('home')  # Assuming 'home' is the name of the URL in the school app
    return render(request, 'add-listing.html')