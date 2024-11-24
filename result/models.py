from django.db import models
from django.db.models import Avg, Sum
from admissions.models import Student, Class  # Reuse Class from the admission app


class Subject(models.Model):
    """
    Represents a subject offered in the school (e.g., Mathematics, English).
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class StudentResult(models.Model):
    """
    Stores the scores for a student in a specific subject for a specific class.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    ca1_score = models.FloatField()  # First Continuous Assessment
    ca2_score = models.FloatField()  # Second Continuous Assessment
    exam_score = models.FloatField()  # Exam Score
    total_score = models.FloatField(editable=False)  # Computed total score
    term = models.CharField(max_length=20, choices=[('First Term', 'First Term'), ('Second Term', 'Second Term'), ('Third Term', 'Third Term')], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Automatically calculate the total score before saving.
        """
        self.total_score = self.ca1_score + self.ca2_score + self.exam_score
        super(StudentResult, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.subject} - Total: {self.total_score}"


from django.db import models
from django.db.models import Avg
from datetime import datetime

class ClassPosition(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    term = models.CharField(
        max_length=20, 
        choices=[
            ('First Term', 'First Term'),
            ('Second Term', 'Second Term'),
            ('Third Term', 'Third Term')
        ]
    )
    average_score = models.FloatField(editable=False, default=0)
    position = models.PositiveIntegerField(null=True, blank=True)  # Student's position
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.class_id.name} - Term: {self.term} - Position: {self.position}"

    def calculate_average(self):
        """
        Calculate the average score for this student in the given class and term.
        """
        results = StudentResult.objects.filter(student=self.student, class_id=self.class_id, term=self.term)
        self.average_score = results.aggregate(Avg('total_score'))['total_score__avg'] or 0
        self.save()

    @classmethod
    def assign_positions(cls, class_id, term, entry_year):
        """
        Calculate and assign positions for all students in a specific class, term, and year of entry.
        """
        # Retrieve the class instance
        class_instance = Class.objects.get(id=class_id)
        
        # Filter students for the given class and year of entry
        students = Student.objects.filter(class_id=class_instance, year_of_entry__year=entry_year)

        # Calculate averages and create/update ClassPosition entries
        for student in students:
            class_position, created = cls.objects.get_or_create(
                student=student,
                class_id=class_instance,
                term=term
            )
            class_position.calculate_average()

        # Rank students based on their average scores
        positions = cls.objects.filter(
            class_id=class_instance,
            term=term,
            student__year_of_entry__year=entry_year
        ).order_by('-average_score')

        rank = 1
        prev_score = None
        ties = 0

        for idx, position in enumerate(positions, start=1):
            # Handle ties
            if prev_score == position.average_score:
                ties += 1
            else:
                rank = idx - ties
                ties = 0

            position.position = rank
            position.save()
            prev_score = position.average_score







class ResultPublication(models.Model):
    """
    Tracks the publication of results for a specific class and term.
    """
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    term = models.CharField(max_length=20, choices=[
        ('First Term', 'First Term'),
        ('Second Term', 'Second Term'),
        ('Third Term', 'Third Term')
    ])
    published_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"Results for {self.class_id.name} - {self.term} ({'Published' if self.is_published else 'Unpublished'})"
