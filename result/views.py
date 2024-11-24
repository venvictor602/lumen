from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import StudentResult, ResultPublication
import pandas as pd
from django.core.exceptions import ValidationError
from .models import *
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from django.http import HttpResponse
from django.db import transaction
import pandas as pd
from .models import *
from admissions.models import Student

from django.shortcuts import render, HttpResponse
import pandas as pd
from .models import Student, Subject, StudentResult, ClassPosition

def upload_results(request):
    if request.method == 'POST' and request.FILES.get('file'):
        excel_file = request.FILES['file']

        # Validate file type
        if not excel_file.name.endswith(('.xlsx', '.xls')):
            return HttpResponse("Please upload a valid Excel file.", status=400)

        try:
            # Load the Excel file
            df = pd.read_excel(excel_file)

            # Check for the required columns
            if 'STUDENT CODE' not in df.columns or 'TERM' not in df.columns:
                return HttpResponse("The uploaded file must contain 'STUDENT CODE' and 'TERM' columns.", status=400)

            # Initialize a list to store processed results
            results = []

            # Process each row in the Excel file
            for _, row in df.iterrows():
                student_code = row['STUDENT CODE']
                term = row['TERM']

                if pd.isna(student_code):
                    continue  # Skip rows without a student code

                try:
                    student = Student.objects.get(student_code=student_code)
                except Student.DoesNotExist:
                    continue  # Skip if the student does not exist

                # Prepare to store subject results for the student
                student_result = {'student_code': student_code, 'subjects': [], 'term': term}

                # Iterate over all columns to extract subject data
                for col in df.columns:
                    if col in ['STUDENT CODE', 'TERM']:
                        continue

                    # Extract subject name and score type
                    if '(' in col and ')' in col:
                        subject_name = col.split('(')[0].strip()
                        score_type = col.split('(')[-1].strip(')')

                        # Find or initialize the subject entry
                        subject_entry = next(
                            (subj for subj in student_result['subjects'] if subj['subject'] == subject_name),
                            None
                        )
                        if not subject_entry:
                            subject_entry = {'subject': subject_name, 'ca1_score': None, 'ca2_score': None, 'exam_score': None}
                            student_result['subjects'].append(subject_entry)

                        # Assign the score based on its type
                        if 'CA1' in score_type:
                            subject_entry['ca1_score'] = row[col]
                        elif 'CA2' in score_type:
                            subject_entry['ca2_score'] = row[col]
                        elif 'EXAM' in score_type:
                            subject_entry['exam_score'] = row[col]

                # Save the student's results in the database
                for subject in student_result['subjects']:
                    subject_obj, _ = Subject.objects.get_or_create(name=subject['subject'])
                    StudentResult.objects.update_or_create(
                        student=student,
                        class_id=student.class_id,
                        subject=subject_obj,
                        term=term,
                        defaults={
                            'ca1_score': subject['ca1_score'],
                            'ca2_score': subject['ca2_score'],
                            'exam_score': subject['exam_score'],
                        }
                    )

                # Add the processed result to the results list
                results.append(student_result)

            # Assign positions for each class, term, and year of entry
            for student in results:
                student_instance = Student.objects.get(student_code=student['student_code'])
                class_instance = student_instance.class_id
                term = student['term']
                entry_year = student_instance.year_of_entry.year  # Extract the year from year_of_entry

                # Assign positions based on class, term, and entry_year
                ClassPosition.assign_positions(class_instance.id, term, entry_year)

            # Generate HTML output for uploaded results
            html = "<h1>Uploaded Results</h1>"
            for student in results:
                html += f"<h2>Student Code: {student['student_code']}</h2>"
                html += f"<p>Term: {student['term']}</p>"
                html += "<table border='1' style='border-collapse: collapse; width: 50%;'>"
                html += "<tr><th>Subject</th><th>CA1</th><th>CA2</th><th>Exam</th></tr>"
                for subject in student['subjects']:
                    html += (
                        f"<tr><td>{subject['subject']}</td>"
                        f"<td>{subject['ca1_score'] if subject['ca1_score'] is not None else '-'}</td>"
                        f"<td>{subject['ca2_score'] if subject['ca2_score'] is not None else '-'}</td>"
                        f"<td>{subject['exam_score'] if subject['exam_score'] is not None else '-'}</td></tr>"
                    )
                html += "</table><br>"

            return HttpResponse(html)

        except Exception as e:
            return HttpResponse(f"Error processing file: {str(e)}", status=400)

    return render(request, 'upload_results.html')



# def upload_results_and_update(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         excel_file = request.FILES['file']

#         # Validate file type
#         if not excel_file.name.endswith(('.xlsx', '.xls')):
#             return HttpResponse("Please upload a valid Excel file.", status=400)

#         try:
#             # Load the Excel file
#             df = pd.read_excel(excel_file)

#             # Check for the required "STUDENT CODE" column
#             if 'STUDENT CODE' not in df.columns:
#                 return HttpResponse("The uploaded file must contain a 'STUDENT CODE' column.", status=400)

#             # Iterate over rows in the file
#             updated_count = 0
#             created_count = 0

#             with transaction.atomic():  # Ensure all updates are completed or rolled back
#                 for _, row in df.iterrows():
#                     student_code = row['STUDENT CODE']

#                     # Find the student by student code
#                     try:
#                         student = Student.objects.get(student_code=student_code)
#                     except Student.DoesNotExist:
#                         # Skip if student doesn't exist
#                         continue

#                     # Identify the class from the student (now using 'class_id' field)
#                     student_class = student.class_id  # Corrected to use 'class_id'

#                     for col in df.columns:
#                         if col == 'STUDENT CODE':
#                             continue  # Skip the "STUDENT CODE" column

#                         # Extract subject and score type from the column name
#                         if '(' in col and ')' in col:
#                             subject_name = col.split('(')[0].strip()
#                             score_type = col.split('(')[-1].strip(')')

#                             # Get or create the subject
#                             subject, _ = Subject.objects.get_or_create(name=subject_name)

#                             # Find or create the student result for this subject
#                             student_result, created = StudentResult.objects.get_or_create(
#                                 student=student,
#                                 class_id=student_class,
#                                 subject=subject,
#                                 defaults={
#                                     'ca1_score': 0,
#                                     'ca2_score': 0,
#                                     'exam_score': 0,
#                                 }
#                             )

#                             # Update scores based on the score type
#                             if 'CA1' in score_type:
#                                 student_result.ca1_score = row[col]
#                             elif 'CA2' in score_type:
#                                 student_result.ca2_score = row[col]
#                             elif 'EXAM' in score_type:
#                                 student_result.exam_score = row[col]

#                             # Save the result
#                             student_result.save()

#                             # Increment counters
#                             if created:
#                                 created_count += 1
#                             else:
#                                 updated_count += 1

#             # Return success message
#             return HttpResponse(
#                 f"Successfully updated results. Created: {created_count}, Updated: {updated_count}"
#             )

#         except Exception as e:
#             return HttpResponse(f"Error processing file: {e}", status=400)

#     return render(request, 'upload_results.html')

from django.shortcuts import render
from django.http import HttpResponse
from .models import Student, StudentResult, Class, ClassPosition
from django.contrib.auth.decorators import login_required

@login_required
def view_student_result(request):
    if request.method == 'POST':
        term = request.POST.get('term')  # Get the selected term
        class_id = request.POST.get('class_id')  # Get the selected class

        try:
            # Retrieve the student linked to the authenticated user
            student = Student.objects.get(user_account=request.user)

            # Debug: Print class_id to verify what's being passed
            print(f"Class ID from form: {class_id}")

            # Fetch the class based on class_id (which is the class name)
            try:
                class_obj = Class.objects.get(level=class_id)
            except Class.DoesNotExist:
                return HttpResponse(f"Class '{class_id}' not found", status=404)

            # Retrieve results for the specific student, class, and term
            results = StudentResult.objects.filter(
                student=student, class_id=class_obj, term=term
            )

            # Retrieve the student's class position in the selected class
            positions = ClassPosition.objects.filter(student=student, class_id=class_obj)

            # If results are found, pass them to the template
            if not results.exists():
                return HttpResponse("No results found for the selected class and term.", status=404)

            return render(request, 'student-result.html', {
                'student': student,
                'results': results,
                'positions': positions,
                'term':term
            })
        except Student.DoesNotExist:
            return HttpResponse("No student profile is linked to your account.", status=404)

    return render(request, 'check-result.html')
