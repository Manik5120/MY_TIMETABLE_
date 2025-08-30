from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Faculty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.department})"

    class Meta:
        verbose_name_plural = "Faculties"

class TimeSlot(models.Model):
    SLOTS = [
        (1, '9:00 - 9:50'),
        (2, '9:50 - 10:40'),
        (3, '10:40 - 11:30'),
        (4, '11:30 - 12:20'),
        (5, '12:20 - 1:10'),
        (6, '1:10 - 2:00'),
        (7, '2:00 - 2:50'),
        (8, '2:50 - 3:40'),
        (9, '3:40 - 4:30'),
        (10, '4:30 - 5:20'),
    ]
    
    slot_number = models.IntegerField(choices=SLOTS, unique=True)
    
    def __str__(self):
        return dict(self.SLOTS)[self.slot_number]

    class Meta:
        ordering = ['slot_number']

class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    credits = models.IntegerField()
    is_lab = models.BooleanField(default=False)
    classes_per_week = models.IntegerField(default=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({'Lab' if self.is_lab else 'Theory'})"

class Availability(models.Model):
    DAYS = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday')
    ]
    
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    day = models.CharField(max_length=3, choices=DAYS)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('faculty', 'day', 'time_slot')

    def __str__(self):
        return f"{self.faculty.name} - {self.get_day_display()} - {self.time_slot}"

class Timetable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True)
    day = models.CharField(max_length=3, choices=Availability.DAYS)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    section = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B')])
    is_lunch_break = models.BooleanField(default=False)

    class Meta:
        unique_together = ('day', 'time_slot', 'section', 'user')

    def __str__(self):
        if self.is_lunch_break:
            return f"Lunch Break - {self.section} - {self.get_day_display()} - {self.time_slot}"
        return f"{self.subject.name} - {self.section} - {self.get_day_display()} - {self.time_slot}"

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    section = models.CharField(max_length=1, choices=[('A', 'Section A'), ('B', 'Section B')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.roll_number}) - Section {self.section}"

class Attendance(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)
    marked_by = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['subject', 'student', 'date']

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} - {self.date}"

class LectureContent(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    section = models.CharField(max_length=1, choices=[('A', 'Section A'), ('B', 'Section B')])
    date = models.DateField()
    topic_covered = models.TextField()
    resources = models.TextField(blank=True, null=True)  # URLs or references
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject.name} - Section {self.section} - {self.date}" 