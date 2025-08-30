from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q
from .models import Student, Attendance, LectureContent, Subject, Faculty
from datetime import datetime, timedelta

@login_required
def add_student_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        roll_number = request.POST.get('roll_number')
        section = request.POST.get('section')
        
        if not name or not roll_number or not section:
            messages.error(request, 'All fields are required.')
            return redirect('add_student')
        
        try:
            # Check if roll number already exists
            if Student.objects.filter(roll_number=roll_number).exists():
                messages.error(request, 'A student with this roll number already exists.')
                return redirect('add_student')
            
            Student.objects.create(
                user=request.user,
                name=name,
                roll_number=roll_number,
                section=section
            )
            messages.success(request, f'Student {name} added successfully.')
            return redirect('student_list')
        except Exception as e:
            messages.error(request, f'Error adding student: {str(e)}')
    
    return render(request, 'attendance/add_student.html')

@login_required
def delete_student_view(request, student_id):
    try:
        student = Student.objects.get(id=student_id, user=request.user)
        name = student.name
        student.delete()
        messages.success(request, f'Student {name} deleted successfully.')
    except Student.DoesNotExist:
        messages.error(request, 'Student not found or you do not have permission to delete them.')
    return redirect('student_list')

@login_required
def student_list_view(request):
    section = request.GET.get('section', 'A')
    students = Student.objects.filter(user=request.user, section=section).order_by('roll_number')
    subjects = Subject.objects.filter(user=request.user)
    
    # Get attendance statistics for each student
    for student in students:
        total_attendance = Attendance.objects.filter(student=student).count()
        present_count = Attendance.objects.filter(student=student, is_present=True).count()
        student.attendance_percentage = (present_count / total_attendance * 100) if total_attendance > 0 else 0
    
    return render(request, 'attendance/student_list.html', {
        'students': students,
        'subjects': subjects,
        'current_section': section
    })

@login_required
def mark_attendance_view(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        section = request.POST.get('section')
        date_str = request.POST.get('date')
        
        try:
            subject = Subject.objects.get(id=subject_id, user=request.user)
            faculty = subject.faculty
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            students = Student.objects.filter(user=request.user, section=section)
            for student in students:
                is_present = request.POST.get(f'student_{student.id}') == 'on'
                Attendance.objects.update_or_create(
                    subject=subject,
                    student=student,
                    date=date,
                    defaults={
                        'is_present': is_present,
                        'marked_by': faculty
                    }
                )
            
            messages.success(request, 'Attendance marked successfully.')
            return redirect('attendance_report', subject_id=subject_id)
        except Exception as e:
            messages.error(request, f'Error marking attendance: {str(e)}')
    
    subjects = Subject.objects.filter(user=request.user)
    section = request.GET.get('section', 'A')
    date = request.GET.get('date', timezone.now().date().strftime('%Y-%m-%d'))
    students = Student.objects.filter(user=request.user, section=section).order_by('roll_number')
    
    return render(request, 'attendance/mark_attendance.html', {
        'subjects': subjects,
        'students': students,
        'current_section': section,
        'date': date
    })

@login_required
def attendance_report_view(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    section = request.GET.get('section', 'A')
    student_id = request.GET.get('student_id')
    start_date = request.GET.get('start_date', (timezone.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    end_date = request.GET.get('end_date', timezone.now().strftime('%Y-%m-%d'))
    
    if student_id:
        students = Student.objects.filter(id=student_id)
    else:
        students = Student.objects.filter(section=section)
    
    attendance_records = []
    
    for student in students:
        attendance = Attendance.objects.filter(
            subject=subject,
            student=student,
            date__range=[start_date, end_date]
        )
        total_classes = attendance.count()
        present_count = attendance.filter(is_present=True).count()
        percentage = (present_count / total_classes * 100) if total_classes > 0 else 0
        
        attendance_records.append({
            'student': student,
            'total_classes': total_classes,
            'present_count': present_count,
            'percentage': round(percentage, 2)
        })
    
    return render(request, 'attendance/attendance_report.html', {
        'subject': subject,
        'attendance_records': attendance_records,
        'current_section': section,
        'start_date': start_date,
        'end_date': end_date,
        'selected_student_id': student_id
    })

@login_required
def add_lecture_content_view(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        section = request.POST.get('section')
        date_str = request.POST.get('date')
        topic_covered = request.POST.get('topic_covered')
        resources = request.POST.get('resources')
        remarks = request.POST.get('remarks')
        
        try:
            subject = Subject.objects.get(id=subject_id, user=request.user)
            faculty = subject.faculty
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            LectureContent.objects.create(
                subject=subject,
                faculty=faculty,
                section=section,
                date=date,
                topic_covered=topic_covered,
                resources=resources,
                remarks=remarks
            )
            
            messages.success(request, 'Lecture content added successfully.')
            return redirect('lecture_content_list')
        except Exception as e:
            messages.error(request, f'Error adding lecture content: {str(e)}')
    
    subjects = Subject.objects.filter(user=request.user)
    return render(request, 'attendance/add_lecture_content.html', {
        'subjects': subjects,
        'date': timezone.now().date().strftime('%Y-%m-%d')
    })

@login_required
def lecture_content_list_view(request):
    subject_id = request.GET.get('subject')
    section = request.GET.get('section', 'A')
    
    query = LectureContent.objects.filter(subject__user=request.user, section=section)
    if subject_id:
        query = query.filter(subject_id=subject_id)
    
    lecture_contents = query.order_by('-date')
    subjects = Subject.objects.filter(user=request.user)
    
    return render(request, 'attendance/lecture_content_list.html', {
        'lecture_contents': lecture_contents,
        'subjects': subjects,
        'current_section': section,
        'current_subject': subject_id
    }) 