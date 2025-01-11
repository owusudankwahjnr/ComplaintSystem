from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.utils.timezone import now
from .forms import SoftwareComplaintForm, AnonymousComplaintForm
from .models import (StudentLevel, CertificateType, Program, Course, SoftwareComplaintCategory,
                     Complaint, OtherComplaintCategory, Gender)


def anonymous_complaint_success(request):
    return render(request, 'anonymous_complaint_success.html')


@login_required
def sip_complaint_success(request):
    return render(request, 'sip_complaint_success.html')


@login_required
def software_complaint(request):
    """View to handle software complaint submission."""
    if request.method == "POST":

        form = SoftwareComplaintForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your complaint has been submitted successfully.")
            return redirect('software-complaint-success')  # Replace with your desired redirect

    complaint_categories = SoftwareComplaintCategory.objects.all()
    programs = Program.objects.all()
    courses = Course.objects.all()
    student_levels = StudentLevel.objects.all()
    certificate_types = CertificateType.objects.all()
    form = SoftwareComplaintForm()

    context = {
        "title": "Submit SIP/LMS Related Complaint",
        "complaint_categories": complaint_categories,
        "student_levels": student_levels,
        "certificate_types": certificate_types,
        "programs": programs,
        "courses": courses,
        "form": form,

    }
    return render(request, 'sip_complaint_form.html', context)


def anonymous_complaint(request):
    if request.method == "POST":
        form = AnonymousComplaintForm(request.POST)
        form.data = form.data.copy()
        if not form.data.get('name') and not form.data.get('phone_number'):
            form.data['complaint_type'] = 'Gender Desk - ANONYMOUS'
        else:
            form.data['complaint_type'] = 'Gender Desk'

        if form.is_valid():
            form.save()
            return redirect('anonymous-complaint-success')  # Replace with your desired redirect

    gender_type = Gender.objects.all()
    complaint_categories = OtherComplaintCategory.objects.all()

    form = AnonymousComplaintForm()

    context = {
        "title": "Gender Desk Complaint Form",
        "optional": "optional",
        "gender_type": gender_type,
        "complaint_categories": complaint_categories,
        "form": form,
    }
    return render(request, 'anonymous_complaint_form.html', context)


@login_required
def complaint_list(request):
    """View to list all complaints."""
    complaints = Complaint.objects.all()
    return render(request, 'complaint_list.html', {'complaints': complaints})


@login_required
def complaint_detail(request, pk):
    """View to show complaint details."""
    complaint = get_object_or_404(Complaint, pk=pk)
    return render(request, 'complaint_detail.html', {'complaint': complaint})


@login_required
def update_complaint_status(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'resolved', 'unresolved']:
            complaint.complaint_status = new_status
            # Set `resolved_at` based on the new status
            if new_status == 'resolved':
                complaint.resolved_at = now()
            else:
                complaint.resolved_at = None
            complaint.save()
            messages.success(request, "Complaint status updated successfully.")
        else:
            messages.error(request, "Invalid status selected.")

    return redirect('complaint-detail', pk=pk)


@login_required
def complaint_dashboard(request):
    # Get filter parameters from the request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category = request.GET.get('category')
    status = request.GET.get('status')
    complaint_type = request.GET.get('complaint_type')

    # Filter complaints based on the parameters
    complaints = Complaint.objects.all()

    if start_date:
        complaints = complaints.filter(created_at__gte=start_date)
    if end_date:
        complaints = complaints.filter(created_at__lte=end_date)
    if category:
        complaints = complaints.filter(complaint_category=category)
    if status:
        complaints = complaints.filter(complaint_status=status)
    if complaint_type:
        complaints = complaints.filter(complaint_type=complaint_type)

    # Aggregate data for the overview section
    total_complaints = complaints.count()
    resolved_complaints = complaints.filter(complaint_status='resolved').count()
    pending_complaints = complaints.filter(complaint_status='pending').count()
    unresolved_complaints = complaints.filter(complaint_status='unresolved').count()

    # Consolidate categories and their counts
    category_data = (
        complaints.values('complaint_category')
        .annotate(count=Count('complaint_category'))
        .order_by('complaint_category')
    )

    complaint_type_data = (
        complaints.values('complaint_type')
        .annotate(count=Count('complaint_type'))
        .order_by('complaint_type')
    )

    # Prepare categories and counts for the chart and dropdown
    categories = [item['complaint_category'] for item in category_data]
    category_counts = [item['count'] for item in category_data]

    complaint_types = [item['complaint_type'] for item in complaint_type_data]
    context = {
        'total_complaints': total_complaints,
        'resolved_complaints': resolved_complaints,
        'pending_complaints': pending_complaints,
        'unresolved_complaints': unresolved_complaints,
        'categories': categories,
        'category_counts': category_counts,
        'complaint_types': complaint_types,
        'complaints': complaints.order_by('-created_at'),
    }

    return render(request, 'complaint_dashboard.html', context)
