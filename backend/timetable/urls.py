from django.urls import path
from . import views
from . import attendance_views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('faculty/', views.faculty_list_view, name='faculty_list'),
    path('faculty/add/', views.add_faculty_view, name='add_faculty'),
    path('faculty/<int:faculty_id>/availability/', views.availability_view, name='faculty_availability'),
    path('faculty/delete/<int:faculty_id>/', views.delete_faculty_view, name='delete_faculty'),
    path('availability/', views.availability_view, name='availability'),
    path('add-subject/', views.add_subject_view, name='add_subject'),
    path('subject-list/', views.subject_list_view, name='subject_list'),
    path('delete-subject/<int:subject_id>/', views.delete_subject_view, name='delete_subject'),
    path('generate-timetable/', views.generate_timetable_view, name='generate_timetable'),
    path('view-timetable/', views.view_timetable_view, name='view_timetable'),
    path('students/', attendance_views.student_list_view, name='student_list'),
    path('students/add/', attendance_views.add_student_view, name='add_student'),
    path('students/delete/<int:student_id>/', attendance_views.delete_student_view, name='delete_student'),
    path('attendance/mark/', attendance_views.mark_attendance_view, name='mark_attendance'),
    path('attendance/report/<int:subject_id>/', attendance_views.attendance_report_view, name='attendance_report'),
    path('lecture/add/', attendance_views.add_lecture_content_view, name='add_lecture_content'),
    path('lecture/list/', attendance_views.lecture_content_list_view, name='lecture_content_list'),
] 