from django.contrib import admin
from django.urls import path
from timetable import views
from timetable import attendance_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('faculty/', views.faculty_list_view, name='faculty_list'),
    path('faculty/add/', views.add_faculty_view, name='add_faculty'),
    path('faculty/delete/<int:faculty_id>/', views.delete_faculty_view, name='delete_faculty'),
    path('faculty/availability/<int:faculty_id>/', views.availability_view, name='faculty_availability'),
    path('subjects/', views.subject_list_view, name='subject_list'),
    path('subjects/add/', views.add_subject_view, name='add_subject'),
    path('subjects/delete/<int:subject_id>/', views.delete_subject_view, name='delete_subject'),
    path('timetable/generate/', views.generate_timetable_view, name='generate_timetable'),
    path('timetable/view/', views.view_timetable_view, name='view_timetable'),
    path('logout/', views.logout_view, name='logout'),
    
    # Student and Attendance URLs
    path('students/', attendance_views.student_list_view, name='student_list'),
    path('students/add/', attendance_views.add_student_view, name='add_student'),
    path('students/delete/<int:student_id>/', attendance_views.delete_student_view, name='delete_student'),
    path('attendance/mark/', attendance_views.mark_attendance_view, name='mark_attendance'),
    path('attendance/report/<int:subject_id>/', attendance_views.attendance_report_view, name='attendance_report'),
    path('lecture/add/', attendance_views.add_lecture_content_view, name='add_lecture_content'),
    path('lecture/list/', attendance_views.lecture_content_list_view, name='lecture_content_list'),
    
    # Password Reset URLs
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='password_reset.html',
             email_template_name='password_reset_email.html',
             subject_template_name='password_reset_subject.txt'
         ),
         name='password_reset'),
    
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'
         ),
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'
         ),
         name='password_reset_complete'),
] 