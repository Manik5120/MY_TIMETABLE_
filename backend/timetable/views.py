from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Faculty, Subject, TimeSlot, Availability, Timetable
import random
from django.utils import timezone

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        name = request.POST.get('name')
         
        try:
            # Create regular user
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=name
            )
            messages.success(request, 'Account created successfully. Please login.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
    return render(request, 'register.html')

@login_required
def dashboard_view(request):
    faculties = Faculty.objects.filter(user=request.user)
    subjects = Subject.objects.filter(user=request.user)
    total_subjects = subjects.count()
    total_faculties = faculties.count()
    lab_subjects = subjects.filter(is_lab=True).count()
    theory_subjects = subjects.filter(is_lab=False).count()
    
    return render(request, 'dashboard.html', {
        'faculties': faculties,
        'total_subjects': total_subjects,
        'total_faculties': total_faculties,
        'lab_subjects': lab_subjects,
        'theory_subjects': theory_subjects
    })

@login_required
def faculty_list_view(request):
    faculties = Faculty.objects.filter(user=request.user)
    return render(request, 'faculty_list.html', {
        'faculties': faculties
    })

def initialize_time_slots():
    # Create time slots if they don't exist
    slots = [
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
    
    for slot_number, _ in slots:
        TimeSlot.objects.get_or_create(slot_number=slot_number)

@login_required
def availability_view(request, faculty_id=None):
    if not faculty_id:
        messages.error(request, 'Please select a faculty member.')
        return redirect('faculty_list')
    
    try:
        faculty = Faculty.objects.get(id=faculty_id, user=request.user)
    except Faculty.DoesNotExist:
        messages.error(request, 'Faculty not found or you do not have permission to access it.')
        return redirect('faculty_list')
    
    # Initialize time slots if they don't exist
    initialize_time_slots()
    
    # Get time slots with display values
    time_slots = []
    slots = [
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
    for slot_number, display_time in slots:
        time_slots.append({
            'slot_number': slot_number,
            'display': display_time
        })
    
    subjects = Subject.objects.filter(faculty=faculty, user=request.user)
    days = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday')
    ]
    
    if request.method == 'POST':
        try:
            # Clear existing availability
            Availability.objects.filter(faculty=faculty).delete()
            
            # Create new availability entries only for checked slots
            for slot in time_slots:
                for day, _ in days:
                    is_available = request.POST.get(f'{day}_{slot["slot_number"]}') == 'on'
                    if is_available:
                        time_slot = TimeSlot.objects.get(slot_number=slot["slot_number"])
                        Availability.objects.create(
                            faculty=faculty,
                            day=day,
                            time_slot=time_slot,
                            is_available=True
                        )
            messages.success(request, f'Availability updated successfully for {faculty.name}.')
            return redirect('faculty_list')
        except Exception as e:
            messages.error(request, f'Error updating availability: {str(e)}')
            return redirect('faculty_list')
    
    # Initialize availability matrix
    availability_matrix = {}
    for day, _ in days:
        availability_matrix[day] = {int(slot['slot_number']): False for slot in time_slots}
    
    # Get all available slots for this faculty
    available_slots = Availability.objects.filter(
        faculty=faculty,
        is_available=True
    ).values_list('day', 'time_slot__slot_number')
    
    # Fill the availability matrix
    for day, slot_number in available_slots:
        availability_matrix[day][int(slot_number)] = True
    
    # Calculate total available slots
    total_available_slots = len(available_slots)
    
    return render(request, 'availability.html', {
        'faculty': faculty,
        'subjects': subjects,
        'time_slots': time_slots,
        'days': days,
        'availability_matrix': availability_matrix,
        'total_available_slots': total_available_slots
    })

@login_required
def add_subject_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        faculty_id = request.POST.get('faculty')
        credits = request.POST.get('credits')
        is_lab = request.POST.get('is_lab') == 'on'
        classes_per_week = request.POST.get('classes_per_week')
        
        # Validate required fields
        if not name or not faculty_id or not credits or not classes_per_week:
            messages.error(request, 'All fields are required.')
            return render(request, 'add_subject.html', {'faculties': Faculty.objects.filter(user=request.user)})
        
        try:
            # Convert string inputs to integers
            credits = int(credits)
            classes_per_week = int(classes_per_week)
            faculty_id = int(faculty_id)
            
            # Validate numeric fields
            if credits <= 0 or classes_per_week <= 0:
                messages.error(request, 'Credits and classes per week must be positive numbers.')
                return render(request, 'add_subject.html', {'faculties': Faculty.objects.filter(user=request.user)})
            
            # Get faculty instance and verify ownership
            faculty = Faculty.objects.get(id=faculty_id, user=request.user)
            
            # Create subject
            Subject.objects.create(
                user=request.user,
                name=name,
                faculty=faculty,
                credits=credits,
                is_lab=is_lab,
                classes_per_week=classes_per_week
            )
            messages.success(request, f'Subject {name} added successfully.')
            return redirect('subject_list')
        except Faculty.DoesNotExist:
            messages.error(request, 'Selected faculty not found or you do not have permission to use it.')
        except ValueError:
            messages.error(request, 'Credits and classes per week must be valid numbers.')
        except Exception as e:
            messages.error(request, f'Failed to add subject: {str(e)}')
        
        return render(request, 'add_subject.html', {'faculties': Faculty.objects.filter(user=request.user)})
    
    faculties = Faculty.objects.filter(user=request.user)
    return render(request, 'add_subject.html', {'faculties': faculties})

@login_required
def subject_list_view(request):
    faculty_id = request.GET.get('faculty')
    if faculty_id:
        subjects = Subject.objects.filter(faculty_id=faculty_id, user=request.user)
        faculty = Faculty.objects.get(id=faculty_id, user=request.user)
    else:
        subjects = Subject.objects.filter(user=request.user)
        faculty = None
    
    faculties = Faculty.objects.filter(user=request.user)
    return render(request, 'subject_list.html', {
        'subjects': subjects,
        'faculties': faculties,
        'current_faculty': faculty
    })

@login_required
def generate_timetable_view(request):
    if not Subject.objects.filter(user=request.user).exists():
        messages.error(request, 'Please add subjects before generating timetable.')
        return redirect('subject_list')
    
    if not Availability.objects.filter(faculty__user=request.user, is_available=True).exists():
        messages.error(request, 'Please set faculty availability before generating timetable.')
        return redirect('faculty_list')

    # Schedule constraints
    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    SLOTS = ["9:00-9:50", "9:50-10:40", "10:40-11:30", "11:30-12:20", "12:20-1:10", "1:10-2:00", "2:00-2:50", "2:50-3:40", "3:40-4:30", "4:30-5:20"]
    LUNCH_SLOTS = ["12:20-1:10", "1:10-2:00"]
    BOOKED_SLOTS = {"A": set(), "B": set()}
    
    # Calculate dynamic class hours based on subject credits
    theory_subjects = Subject.objects.filter(user=request.user, is_lab=False)
    CLASSES_PER_SECTION = sum(subject.credits for subject in theory_subjects)
    
    # Calculate lab hours (2 slots per lab)
    lab_subjects = Subject.objects.filter(user=request.user, is_lab=True)
    LAB_HOURS_PER_SECTION = lab_subjects.count() * 2
    
    sub_classes_A = []
    sub_classes_B = []

    # Cache faculty availability
    faculty_availability = {}
    for faculty in Faculty.objects.filter(user=request.user):
        faculty_availability[faculty.id] = {
            day[:3].upper(): [slot.slot_number for slot in TimeSlot.objects.filter(
                availability__faculty=faculty,
                availability__day=day[:3].upper(),
                availability__is_available=True
            )]
            for day in DAYS
        }

    def initialize_timetable():
        return {
            "A": {day: ["Free"] * len(SLOTS) for day in DAYS},
            "B": {day: ["Free"] * len(SLOTS) for day in DAYS}
        }

    def is_slot_available(timetable, section, day, slot_index):
        return timetable[section][day][slot_index] == "Free"

    def is_lab(timetable, section, day, slot_index):
        entry = timetable[section][day][slot_index]
        return isinstance(entry, str) and "(Lab)" in entry

    def is_faculty_available(faculty_id, day, slot_index):
        return slot_index + 1 in faculty_availability[faculty_id][day[:3].upper()]

    def are_consecutive_slots_free(timetable, section, day, slot_index):
        return (is_slot_available(timetable, section, day, slot_index) and
                is_slot_available(timetable, section, day, slot_index + 1))

    def assign_labs(timetable, section):
        assigned_labs = 0
        available_slots = [(day, i) for day in DAYS for i in range(len(SLOTS) - 1)]
        lab_subjects = Subject.objects.filter(user=request.user, is_lab=True)

        for lab in lab_subjects:
            faculty = lab.faculty
            while assigned_labs < LAB_HOURS_PER_SECTION:
                random.shuffle(available_slots)
                for (day, slot_index) in available_slots:
                    if SLOTS[slot_index] in LUNCH_SLOTS or SLOTS[slot_index + 1] in LUNCH_SLOTS:
                        continue
                    
                    if (are_consecutive_slots_free(timetable, section, day, slot_index) and
                        is_faculty_available(faculty.id, day[:3].upper(), slot_index) and
                        is_faculty_available(faculty.id, day[:3].upper(), slot_index + 1)):
                        
                        if (timetable["A"][day][slot_index] != f"{lab.name} (Lab)" and 
                            timetable["B"][day][slot_index] != f"{lab.name} (Lab)"):
                            lab_name = f"{lab.name} (Lab)"
                            timetable[section][day][slot_index] = lab_name
                            timetable[section][day][slot_index + 1] = lab_name
                            assigned_labs += 2
                            BOOKED_SLOTS[section].add((day, slot_index, lab_name))
                            
                            # Update faculty availability
                            if slot_index + 1 in faculty_availability[faculty.id][day[:3].upper()]:
                                faculty_availability[faculty.id][day[:3].upper()].remove(slot_index + 1)
                            if slot_index + 2 in faculty_availability[faculty.id][day[:3].upper()]:
                                faculty_availability[faculty.id][day[:3].upper()].remove(slot_index + 2)
                            break
                else:
                    continue
                break

    def assign_classes(timetable, section):
        theory_subjects = Subject.objects.filter(user=request.user, is_lab=False)
        for subject in theory_subjects:
            faculty = subject.faculty
            num_classes = subject.credits  # Use credits as number of classes
            allotted = 0
            
            for _ in range(num_classes):
                if section == "A":
                    available_slots = [(day, i) for day in DAYS for i in range(len(SLOTS)) 
                                    if (is_slot_available(timetable, "A", day, i) and 
                                        is_slot_available(timetable, "B", day, i) and
                                        is_faculty_available(faculty.id, day[:3].upper(), i))]
                else:
                    available_slots = [(day, i) for day in DAYS for i in range(len(SLOTS)) 
                                    if ((is_slot_available(timetable, "A", day, i) and 
                                         is_slot_available(timetable, "B", day, i)) and
                                        is_faculty_available(faculty.id, day[:3].upper(), i)) or 
                                       ((is_lab(timetable, "A", day, i) and
                                         is_faculty_available(faculty.id, day[:3].upper(), i)) and 
                                        is_slot_available(timetable, "B", day, i))]
                
                if available_slots:
                    day, slot_index = random.choice(available_slots)
                    timetable[section][day][slot_index] = subject.name
                    BOOKED_SLOTS[section].add((day, slot_index, subject.name))
                    allotted += 1
                    
                    # Update faculty availability
                    if slot_index + 1 in faculty_availability[faculty.id][day[:3].upper()]:
                        faculty_availability[faculty.id][day[:3].upper()].remove(slot_index + 1)
            
            left_classes = num_classes - allotted
            if left_classes:
                for _ in range(left_classes):
                    if section == "A":
                        sub_classes_A.append(subject.name)
                    else:
                        sub_classes_B.append(subject.name)

    def reassign_classes_A(timetable):
        for subject_name in sub_classes_A[:]:
            subject = Subject.objects.get(name=subject_name)
            faculty = subject.faculty
            available_slots = [(day, i) for day in DAYS for i in range(len(SLOTS)) 
                                if ((is_slot_available(timetable, "A", day, i) and 
                                     is_slot_available(timetable, "B", day, i)) and
                                    is_faculty_available(faculty.id, day[:3].upper(), i)) or 
                                is_lab(timetable, "B", day, i)]
            
            for day in DAYS:
                if (timetable["A"][day][4] in ["Free", "Lunch Break"] and 
                    timetable["A"][day][5] in ["Free", "Lunch Break"] and 
                    timetable["B"][day][4] in ["Free", "Lunch Break"] and 
                    timetable["B"][day][5] in ["Free", "Lunch Break"]):
                    available_slots.extend([(day, 4), (day, 5)])
                elif (timetable["A"][day][4] in ["Free", "Lunch Break"] and 
                      timetable["A"][day][5] in ["Free", "Lunch Break"] and 
                      timetable["B"][day][4] in ["Free", "Lunch Break"]):
                    available_slots.append((day, 4))
                elif (timetable["A"][day][4] in ["Free", "Lunch Break"] and 
                      timetable["A"][day][5] in ["Free", "Lunch Break"] and 
                      timetable["B"][day][5] in ["Free", "Lunch Break"]):
                    available_slots.append((day, 5))
            
            if available_slots:
                day, slot_index = random.choice(available_slots)
                timetable["A"][day][slot_index] = subject_name
                BOOKED_SLOTS["A"].add((day, slot_index, subject_name))
                sub_classes_A.remove(subject_name)
        
        sub_classes_A.clear()

    def reassign_classes_B(timetable):
        for subject_name in sub_classes_B[:]:
            subject = Subject.objects.get(name=subject_name)
            faculty = subject.faculty
            available_slots = [(day, i) for day in DAYS for i in range(len(SLOTS)) 
                                if ((is_slot_available(timetable, "A", day, i) and 
                                     is_slot_available(timetable, "B", day, i)) and
                                    is_faculty_available(faculty.id, day[:3].upper(), i)) or 
                                ((is_lab(timetable, "A", day, i) and
                                  is_faculty_available(faculty.id, day[:3].upper(), i)) and 
                                 is_slot_available(timetable, "B", day, i))]
            
            for day in DAYS:
                if (timetable["B"][day][4] in ["Free", "Lunch Break"] and 
                    timetable["B"][day][5] in ["Free", "Lunch Break"] and 
                    timetable["A"][day][4] in ["Free", "Lunch Break"] and 
                    timetable["A"][day][5] in ["Free", "Lunch Break"]):
                    available_slots.extend([(day, 4), (day, 5)])
                elif (timetable["B"][day][4] in ["Free", "Lunch Break"] and 
                      timetable["B"][day][5] in ["Free", "Lunch Break"] and 
                      timetable["A"][day][4] in ["Free", "Lunch Break"]):
                    available_slots.append((day, 4))
                elif (timetable["B"][day][4] in ["Free", "Lunch Break"] and 
                      timetable["B"][day][5] in ["Free", "Lunch Break"] and 
                      timetable["A"][day][5] in ["Free", "Lunch Break"]):
                    available_slots.append((day, 5))
            
            if available_slots:
                day, slot_index = random.choice(available_slots)
                timetable["B"][day][slot_index] = subject_name
                BOOKED_SLOTS["B"].add((day, slot_index, subject_name))
                sub_classes_B.remove(subject_name)
        
        sub_classes_B.clear()

    def assign_lunch_break(timetable):
        for section in ["A", "B"]:
            for day in DAYS:
                if timetable[section][day][4] == "Lunch Break" or timetable[section][day][5] == "Lunch Break":
                    continue
                # Get lab subjects
                lab_entries = [entry for entry in timetable[section][day] if isinstance(entry, str) and "(Lab)" in entry]
                # Check if lab slots are in lunch period
                if not any("(Lab)" in str(timetable[section][day][i]) for i in [4, 5]):
                    lunch_slot = random.choice(LUNCH_SLOTS)
                elif "(Lab)" in str(timetable[section][day][4]):
                    lunch_slot = LUNCH_SLOTS[1]
                elif "(Lab)" in str(timetable[section][day][5]):
                    lunch_slot = LUNCH_SLOTS[0]
                
                for recess in LUNCH_SLOTS:
                    if timetable[section][day][SLOTS.index(recess)] == "Free":
                        lunch_slot = recess
                
                slot_index = SLOTS.index(lunch_slot)
                if section == "A":
                    if timetable[section][day][slot_index] != "Free":
                        sub_classes_A.append(timetable[section][day][slot_index])
                else:
                    if timetable[section][day][slot_index] != "Free":
                        sub_classes_B.append(timetable[section][day][slot_index])
                timetable[section][day][slot_index] = "Lunch Break"

    # Main generation loop
    max_attempts = 10000
    for attempt in range(max_attempts):
        timetable = initialize_timetable()
        
        # Assign labs
        assign_labs(timetable, "A")
        assign_labs(timetable, "B")
        
        # Assign classes
        assign_classes(timetable, "A")
        assign_classes(timetable, "B")
        
        # Assign lunch breaks
        assign_lunch_break(timetable)
        
        # Reassign classes
        reassign_classes_A(timetable)
        reassign_classes_B(timetable)
        
        # Reassign lunch breaks
        assign_lunch_break(timetable)
        
        # Calculate totals
        total_assigned_A = sum(1 for day in DAYS for slot in timetable["A"][day] 
                             if slot != "Free" and slot != "Lunch Break")
        total_assigned_B = sum(1 for day in DAYS for slot in timetable["B"][day] 
                             if slot != "Free" and slot != "Lunch Break")
        
        if total_assigned_A == (LAB_HOURS_PER_SECTION + CLASSES_PER_SECTION) and \
           total_assigned_B == (LAB_HOURS_PER_SECTION + CLASSES_PER_SECTION):
            print(f"Success on attempt {attempt + 1}")
            
            # Save to database
            Timetable.objects.filter(user=request.user).delete()
            time_slots = TimeSlot.objects.all().order_by('slot_number')
            
            for section in ["A", "B"]:
                for day in DAYS:
                    for slot_idx, entry in enumerate(timetable[section][day]):
                        if entry != "Free":
                            time_slot = time_slots[slot_idx]
                            if entry == "Lunch Break":
                                Timetable.objects.create(
                                    user=request.user,
                                    section=section,
                                    day=day[:3].upper(),
                                    time_slot=time_slot,
                                    is_lunch_break=True
                                )
                            else:
                                subject_name = entry.replace(" (Lab)", "")
                                try:
                                    subject = Subject.objects.get(name=subject_name)
                                    Timetable.objects.create(
                                        user=request.user,
                                        section=section,
                                        day=day[:3].upper(),
                                        time_slot=time_slot,
                                        subject=subject,
                                        faculty=subject.faculty
                                    )
                                except Subject.DoesNotExist:
                                    continue
            
            messages.success(request, 'Timetable generated successfully.')
            return redirect('view_timetable')
    
    messages.error(request, 'Failed to generate a complete timetable. Please check faculty availability and try again.')
    return redirect('view_timetable')

@login_required
def view_timetable_view(request):
    # Get current section (default to 'A')
    current_section = request.GET.get('section', 'A')
    
    # Define days
    days = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday')
    ]
    
    # Get time slots with display values
    time_slots = [
        {'slot_number': num, 'display': time}
        for num, time in [
            (1, '9:00 - 9:50'),
            (2, '9:50 - 10:40'),
            (3, '10:40 - 11:30'),
            (4, '11:30 - 12:20'),
            (5, '12:20 - 1:10'),
            (6, '1:10 - 2:00'),
            (7, '2:00 - 2:50'),
            (8, '2:50 - 3:40'),
            (9, '3:40 - 4:30'),
            (10, '4:30 - 5:20')
        ]
    ]
    
    # Get timetable entries for the current section
    timetable_entries = Timetable.objects.filter(section=current_section).select_related('subject', 'faculty')
    
    # Create a list of cells for each time slot and day
    timetable_cells = []
    for slot in time_slots:
        row = {'time': slot['display'], 'cells': []}
        for day_code, _ in days:
            # Find entry for this day and slot
            entry = timetable_entries.filter(day=day_code, time_slot__slot_number=slot['slot_number']).first()
            if entry:
                if entry.is_lunch_break:
                    cell = {'type': 'lunch', 'content': 'Lunch Break'}
                else:
                    cell = {'type': 'class', 'content': f"{entry.subject.name}\n{entry.faculty.name}"}
            else:
                cell = {'type': 'free', 'content': 'Free'}
            row['cells'].append(cell)
        timetable_cells.append(row)
    
    return render(request, 'view_timetable.html', {
        'days': days,
        'timetable_cells': timetable_cells,
        'current_section': current_section
    })

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')

@login_required
def delete_subject_view(request, subject_id):
    try:
        subject = Subject.objects.get(id=subject_id, user=request.user)
        faculty_name = subject.faculty.name
        subject.delete()
        messages.success(request, f'Subject deleted successfully from {faculty_name}.')
    except Subject.DoesNotExist:
        messages.error(request, 'Subject not found or you do not have permission to delete it.')
    return redirect('subject_list')

@login_required
def add_faculty_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        department = request.POST.get('department')
        
        # Validate required fields
        if not name or not email or not department:
            messages.error(request, 'All fields are required.')
            return render(request, 'add_faculty.html')
        
        try:
            # Check if faculty with same email already exists for this user
            if Faculty.objects.filter(email=email, user=request.user).exists():
                messages.error(request, 'A faculty member with this email already exists.')
                return render(request, 'add_faculty.html')
            
            faculty = Faculty.objects.create(
                user=request.user,
                name=name,
                email=email,
                department=department
            )
            messages.success(request, f'Faculty {name} added successfully.') 
            return redirect('faculty_list')
        except Exception as e:
            messages.error(request, f'Failed to add faculty: {str(e)}')
            return render(request, 'add_faculty.html')
    
    return render(request, 'add_faculty.html')

@login_required
def delete_faculty_view(request, faculty_id):
    try:
        faculty = Faculty.objects.get(id=faculty_id, user=request.user)
        faculty_name = faculty.name
        faculty.delete()
        messages.success(request, f'Faculty {faculty_name} deleted successfully.')
    except Faculty.DoesNotExist:
        messages.error(request, 'Faculty not found or you do not have permission to delete it.')
    return redirect('faculty_list') 

