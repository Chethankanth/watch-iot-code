from django.contrib import admin
from .models import Patient, Guardian, HealthData, Alert

class GuardianInline(admin.TabularInline):
    model = Guardian
    extra = 1

class AlertInline(admin.TabularInline):
    model = Alert
    extra = 0
    readonly_fields = ['timestamp', 'type', 'message', 'health_data', 'status', 'resolved_at']
    can_delete = False
    max_num = 5
    ordering = ['-timestamp']

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'gender', 'user_id', 'emergency_contact', 'created_at']
    search_fields = ['name', 'user_id', 'emergency_contact']
    list_filter = ['gender', 'age']
    inlines = [GuardianInline, AlertInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'age', 'gender', 'user_id', 'emergency_contact')
        }),
        ('Medical Information', {
            'fields': ('medical_history',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_patient_name', 'relationship', 'phone_number', 'notification_enabled']
    search_fields = ['name', 'patient__name', 'phone_number', 'email']
    list_filter = ['relationship', 'notification_enabled']
    
    def get_patient_name(self, obj):
        return obj.patient.name
    get_patient_name.short_description = 'Patient'
    get_patient_name.admin_order_field = 'patient__name'

@admin.register(HealthData)
class HealthDataAdmin(admin.ModelAdmin):
    list_display = ['get_patient_name', 'timestamp', 'heart_rate', 'spo2']
    search_fields = ['patient__name']
    list_filter = ['timestamp']
    readonly_fields = ['timestamp']
    
    def get_patient_name(self, obj):
        return obj.patient.name
    get_patient_name.short_description = 'Patient'
    get_patient_name.admin_order_field = 'patient__name'

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['get_patient_name', 'timestamp', 'type', 'message', 'status']
    search_fields = ['patient__name', 'message']
    list_filter = ['status', 'type', 'timestamp']
    readonly_fields = ['timestamp']
    actions = ['mark_as_acknowledged', 'mark_as_resolved']
    
    def get_patient_name(self, obj):
        return obj.patient.name
    get_patient_name.short_description = 'Patient'
    get_patient_name.admin_order_field = 'patient__name'
    
    def mark_as_acknowledged(self, request, queryset):
        queryset.update(status='ACKNOWLEDGED')
    mark_as_acknowledged.short_description = "Mark selected alerts as acknowledged"
    
    def mark_as_resolved(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='RESOLVED', resolved_at=timezone.now())
    mark_as_resolved.short_description = "Mark selected alerts as resolved"