from django import forms
from .models import Complaint


class SoftwareComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            'name', 'student_id', 'phone_number', 'personal_email',
            'complaint_category', 'student_level',
            'certificate_type', 'program', 'course', 'description'
        ]
        widgets = {
            'student_id': forms.TextInput(attrs={'placeholder': 'Index Number'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your complaint'}),
            'personal_email': forms.EmailInput(attrs={'placeholder': 'Enter your personal email'}),
            'name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Active Phone Number'}),
            'program': forms.TextInput(attrs={
                'list': 'programs',
                'placeholder': "Select or type a Program"
            }),
            'course': forms.TextInput(attrs={
                'list': 'courses',
                'placeholder': "Select or type a Course"
            }),
            'complaint_category': forms.TextInput(attrs={
                'list': 'complaint_categories',  # Link to the datalist
                'placeholder': 'Select or type a category',
            }),
            'certificate_type': forms.TextInput(attrs={
                'list': 'certificate_types',  # Link to the datalist
                'placeholder': 'Select or type a certificate type',
            }),
        }


class AnonymousComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            'name', 'student_id','phone_number', 'gender', 'complaint_category', 'description', 'complaint_type'
        ]

        widgets = {
            'complaint_category': forms.TextInput(attrs={
                'list': 'complaint_categories',  # Link to the datalist
                'placeholder': 'Select or type a category',
            }),
            'gender': forms.TextInput(attrs={
                'list': 'gender_type',  # Link to the datalist
                'placeholder': 'Select or type a gender',
            }),
            'name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Active Phone Number'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your complaint'}),
            'student_id': forms.TextInput(attrs={'placeholder': 'Index Number'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['phone_number'].required = False
        self.fields['gender'].required = False
        self.fields['student_id'].required = False
