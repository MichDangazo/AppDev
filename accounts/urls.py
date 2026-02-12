from django.urls import path
from .views import login_view, student_dashboard, instructor_dashboard, facilities_dashboard

urlpatterns = [
    path('', login_view, name='login'),
    path('student/', student_dashboard, name='student_dashboard'),
    path('instructor/', instructor_dashboard, name='instructor_dashboard'),
    path('facilities/', facilities_dashboard, name='facilities_dashboard'),
]
