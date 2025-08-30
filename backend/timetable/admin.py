from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from .models import Faculty, Subject, TimeSlot, Availability, Timetable

# Customize User Admin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'date_joined', 'last_login', 'is_active', 'is_staff')
    list_filter = ('is_active', 'date_joined', 'last_login')
    search_fields = ('username', 'email', 'first_name')
    ordering = ('-date_joined',)
    
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return (
            (None, {'fields': ('username', 'password')}),
            ('Personal info', {'fields': ('first_name', 'email')}),
            ('Permissions', {'fields': ('is_active',)}),
            ('Important dates', {'fields': ('last_login', 'date_joined')})
        )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'password1', 'password2'),
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('date_joined', 'last_login', 'is_staff', 'is_superuser')
        return ()

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new user
            obj.is_staff = False
            obj.is_superuser = False
        super().save_model(request, obj, form, change)

class TimetableAdmin(admin.ModelAdmin):
    list_display = ('user', 'section', 'day', 'time_slot', 'subject', 'faculty', 'is_lunch_break')
    list_filter = ('section', 'day', 'is_lunch_break', 'faculty')
    search_fields = ('user__username', 'subject__name', 'faculty__name')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    def save_model(self, request, obj, form, change):
        if not obj.user_id:  # If creating new timetable entry
            obj.user = request.user
        super().save_model(request, obj, form, change)
    
    def has_change_permission(self, request, obj=None):
        if not obj or request.user.is_superuser:
            return True
        return obj.user == request.user
    
    def has_delete_permission(self, request, obj=None):
        if not obj or request.user.is_superuser:
            return True
        return obj.user == request.user

class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'department', 'created_at')
    search_fields = ('name', 'email', 'department')
    list_filter = ('department', 'created_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    def save_model(self, request, obj, form, change):
        if not obj.user_id:  # If creating new faculty
            obj.user = request.user
        super().save_model(request, obj, form, change)
    
    def has_change_permission(self, request, obj=None):
        if not obj or request.user.is_superuser:
            return True
        return obj.user == request.user
    
    def has_delete_permission(self, request, obj=None):
        if not obj or request.user.is_superuser:
            return True
        return obj.user == request.user

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty', 'credits', 'is_lab', 'classes_per_week', 'created_at')
    search_fields = ('name', 'faculty__name')
    list_filter = ('is_lab', 'credits', 'faculty', 'created_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    def save_model(self, request, obj, form, change):
        if not obj.user_id:  # If creating new subject
            obj.user = request.user
        super().save_model(request, obj, form, change)
    
    def has_change_permission(self, request, obj=None):
        if not obj or request.user.is_superuser:
            return True
        return obj.user == request.user
    
    def has_delete_permission(self, request, obj=None):
        if not obj or request.user.is_superuser:
            return True
        return obj.user == request.user

class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('slot_number', 'get_display_time')
    ordering = ['slot_number']

    def get_display_time(self, obj):
        try:
            slots = dict(obj.SLOTS)
            return slots.get(obj.slot_number, '')
        except (AttributeError, TypeError):
            return ''
    get_display_time.short_description = 'Time'

class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'day', 'time_slot', 'is_available', 'created_at')
    list_filter = ('faculty', 'day', 'is_available', 'created_at')
    search_fields = ('faculty__name',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(faculty__user=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "faculty" and not request.user.is_superuser:
            kwargs["queryset"] = Faculty.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def has_change_permission(self, request, obj=None):
        if not obj or request.user.is_superuser:
            return True
        return obj.faculty.user == request.user
    
    def has_delete_permission(self, request, obj=None):
        if not obj or request.user.is_superuser:
            return True
        return obj.faculty.user == request.user

def register_if_not_registered(model, admin_class):
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        admin.site.unregister(model)
        admin.site.register(model, admin_class)

# Clean up and register models
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

# Register our models using the safe registration function
register_if_not_registered(User, CustomUserAdmin)
register_if_not_registered(Faculty, FacultyAdmin)
register_if_not_registered(Subject, SubjectAdmin)
register_if_not_registered(TimeSlot, TimeSlotAdmin)
register_if_not_registered(Availability, AvailabilityAdmin)
register_if_not_registered(Timetable, TimetableAdmin) 