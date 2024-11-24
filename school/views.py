from django.shortcuts import render

from django.shortcuts import render, redirect

def home(request):
    return render(request, 'index.html')

# school/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def student_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user by email (username) and password
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('student_dashboard')
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'login.html')


@login_required
def student_dashboard(request):
    return render(request, 'student-details.html')

from django.contrib.auth import logout
def student_logout(request):
    logout(request)
    return redirect('student_login')