from django.db import models
from django.contrib.auth import get_user_model
from multiselectfield import MultiSelectField

User = get_user_model()


class StudentLevel(models.Model):
    """Model for dynamically managing student levels."""
    level = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Level {self.level}"

    class Meta:
        verbose_name = "Student Level"
        verbose_name_plural = "Student Levels"
        ordering = ['level']


class Gender(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class CertificateType(models.Model):
    """Model for dynamically managing student level types."""
    type_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = "Certificate Type"
        verbose_name_plural = "Certificate Types"
        ordering = ['type_name']


class Program(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class SoftwareComplaintCategory(models.Model):
    """Model for defining software related complaint categories and associated form fields."""

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Software Complaint Category"
        verbose_name_plural = "Software Complaint Categories"


class OtherComplaintCategory(models.Model):
    """Model for defining non software related complaint categories and associated form fields."""

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Other Complaint Category"
        verbose_name_plural = "Other Complaint Categories"


class Complaint(models.Model):
    """Main model for tracking student issues."""

    class AllocationStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'resolved', 'Resolved'
        DENIED = 'unresolved', 'Unresolved'

    class ComplaintType(models.TextChoices):
        GENDER_DESK = 'Gender Desk', 'Gender Desk'
        GENDER_DESK_ANONYMOUS = 'Gender Desk - ANONYMOUS', 'Gender Desk - ANONYMOUS'
        SOFTWARE = 'Software', 'Software'

    created_at = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    student_id = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    personal_email = models.EmailField(blank=True, null=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    complaint_status = models.CharField(max_length=10, choices=AllocationStatus.choices,
                                        default=AllocationStatus.PENDING)
    complaint_type = models.CharField(max_length=25, choices=ComplaintType.choices,
                                      default=ComplaintType.SOFTWARE)
    complaint_category = models.CharField(max_length=255, null=False)
    student_level = models.CharField(max_length=255, null=False, blank=True)
    assign_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user")

    certificate_type = models.CharField(max_length=255, null=True, blank=True)
    program = models.CharField(max_length=255, null=True, blank=True)
    course = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    resolved_at = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Complaint"
        verbose_name_plural = "Complaints"
        ordering = ['-created_at']
