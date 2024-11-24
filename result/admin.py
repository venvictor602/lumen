from django.contrib import admin
from .models import Subject, StudentResult, ResultPublication

# Register Subject model
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

admin.site.register(Subject, SubjectAdmin)


# Register StudentResult model
class StudentResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'ca1_score', 'ca2_score', 'exam_score', 'total_score', 'class_id', 'term')
    list_filter = ('class_id', 'subject')
    search_fields = ('student__email', 'subject__name')
    readonly_fields = ('total_score',)

    def save_model(self, request, obj, form, change):
        """
        Override the save method to ensure total_score is calculated before saving.
        """
        obj.total_score = obj.ca1_score + obj.ca2_score + obj.exam_score
        super().save_model(request, obj, form, change)

admin.site.register(StudentResult, StudentResultAdmin)



from .models import ClassPosition
@admin.register(ClassPosition)
class ClassPositionAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_id', 'term', 'average_score', 'position', 'created_at')
    list_filter = ('class_id', 'term')
    search_fields = ('student__first_name', 'student__last_name', 'class_id__name')



# Register ResultPublication model
class ResultPublicationAdmin(admin.ModelAdmin):
    list_display = ('class_id', 'term', 'is_published', 'published_at')
    list_filter = ('class_id', 'term', 'is_published')
    search_fields = ('class_id__name',)

admin.site.register(ResultPublication, ResultPublicationAdmin)

