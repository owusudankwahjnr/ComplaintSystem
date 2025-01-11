import openpyxl
from django.contrib import admin
import pandas as pd
from django.template.response import TemplateResponse
from django.urls import path
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.contrib import messages

from .models import (
    StudentLevel, CertificateType, Program, Course, Gender,
    SoftwareComplaintCategory, Complaint, OtherComplaintCategory)


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', ]


@admin.register(SoftwareComplaintCategory)
class SoftwareComplaintAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', ]


@admin.register(OtherComplaintCategory)
class OtherComplaintAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', ]


@admin.register(StudentLevel)
class StudentLevelAdmin(admin.ModelAdmin):
    list_display = ['level']
    search_fields = ['level']


@admin.register(CertificateType)
class CertificateTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name']
    search_fields = ['type_name']


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display fields in the admin list view
    search_fields = ('name',)
    change_list_template = "admin/program_changelist.html"  # Custom template

    def get_urls(self):
        """Add custom URL for the bulk upload page."""
        urls = super().get_urls()
        custom_urls = [
            path('bulk-upload/', self.bulk_upload, name='program-bulk-upload'),
        ]
        return custom_urls + urls

    def bulk_upload(self, request):
        """Custom view for bulk uploading programs via an Excel file."""
        if request.method == 'POST' and request.FILES.get('excel_file'):
            excel_file = request.FILES['excel_file']
            if not excel_file.name.endswith(('.xls', '.xlsx')):
                self.message_user(request, "Invalid file format. Please upload an Excel file.", level=messages.ERROR)
                return TemplateResponse(request, "admin/program_bulk_upload.html")
            try:
                # Read the Excel file
                df = pd.read_excel(excel_file)

                # Check if the required column exists
                if 'name' not in df.columns:
                    self.message_user(request, "The Excel file must contain a 'name' column.", level=messages.ERROR)
                    return TemplateResponse(request, "admin/program_bulk_upload.html")

                # Iterate through rows and create Program objects
                created_count = 0
                for index, row in df.iterrows():
                    name = row['name']
                    if not Program.objects.filter(name=name).exists():
                        Program.objects.create(name=name)
                        created_count += 1

                self.message_user(request, f"Successfully added {created_count} programs.", level=messages.SUCCESS)
                return TemplateResponse(request, "admin/program_bulk_upload.html")
            except Exception as e:
                self.message_user(request, f"Error processing file: {str(e)}", level=messages.ERROR)
                return TemplateResponse(request, "admin/program_bulk_upload.html")

        return TemplateResponse(request, "admin/program_bulk_upload.html")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display fields in the admin list view
    search_fields = ('name',)
    # search_help_text = 'name'
    change_list_template = "admin/course_changelist.html"  # Custom template

    def get_urls(self):
        """
        Add custom URL for the bulk upload page.
        """
        urls = super().get_urls()
        custom_urls = [
            path('bulk-upload/', self.bulk_upload, name='course-bulk-upload'),
        ]
        return custom_urls + urls

    def bulk_upload(self, request):
        """
        Custom view for bulk uploading courses via an Excel file.
        """
        if request.method == 'POST' and request.FILES.get('excel_file'):
            excel_file = request.FILES['excel_file']
            if not excel_file.name.endswith(('.xls', '.xlsx')):
                self.message_user(request, "Invalid file format. Please upload an Excel file.", level=messages.ERROR)
                return TemplateResponse(request, "admin/course_bulk_upload.html")

            try:
                # Read the Excel file
                df = pd.read_excel(excel_file)

                # Check if the required column exists
                if 'name' not in df.columns:
                    self.message_user(request, "The Excel file must contain a 'name' column.", level=messages.ERROR)
                    return TemplateResponse(request, "admin/course_bulk_upload.html")

                # Iterate through rows and create Course objects
                created_count = 0
                for index, row in df.iterrows():
                    name = row['name']
                    if not Course.objects.filter(name=name).exists():
                        Course.objects.create(name=name)
                        created_count += 1

                self.message_user(request, f"Successfully added {created_count} courses.", level=messages.SUCCESS)
                return TemplateResponse(request, "admin/course_bulk_upload.html")

            except Exception as e:
                self.message_user(request, f"Error processing file: {str(e)}", level=messages.ERROR)

        return TemplateResponse(request, "admin/course_bulk_upload.html")


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['name', 'student_id', 'personal_email', 'complaint_category', 'complaint_type',
                    'complaint_status', 'created_at']
    list_filter = ['complaint_status', 'created_at', 'complaint_category', 'complaint_type']
    search_fields = ['name', 'student_id', 'complaint_category', 'complaint_type']
