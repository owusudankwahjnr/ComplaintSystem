from django.urls import path
from .views import (
    anonymous_complaint_success, software_complaint, complaint_detail, complaint_list, complaint_dashboard,
    update_complaint_status, anonymous_complaint, sip_complaint_success
)

urlpatterns = [
    path('complaint-dashboard/', complaint_dashboard, name='complaint-dashboard'),
    path('software-complaint-form/', software_complaint, name='software-complaint-form'),
    path('', anonymous_complaint, name='anonymous-complaint-form'),
    path('complaints/', complaint_list, name='complaint-list'),
    path('anonymous_complaint_success/', anonymous_complaint_success, name='anonymous-complaint-success'),
    path('sip_complaint_success/', sip_complaint_success, name='software-complaint-success'),
    path('complaint/<int:pk>/', complaint_detail, name='complaint-detail'),
    path('complaint/<int:pk>/update-status/', update_complaint_status, name='update-complaint-status'),
]
