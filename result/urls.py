from django.urls import path
from . import views

urlpatterns = [
    path('upload-results/', views.upload_results, name='upload_results'),
    path('view-result/', views.view_student_result, name='view_student_result'),
]
