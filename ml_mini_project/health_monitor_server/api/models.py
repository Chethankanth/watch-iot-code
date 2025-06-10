from django.db import models
from django.utils import timezone

class Patient(models.Model):
    """Model representing a patient"""
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ])
    user_id = models.CharField(max_length=100, unique=True)
    medical_history = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.age})"

class Guardian(models.Model):
    """Model representing a patient's guardian"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='guardians')
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50, choices=[
        ('PARENT', 'Parent'),
        ('CHILD', 'Child'),
        ('SPOUSE', 'Spouse'),
        ('SIBLING', 'Sibling'),
        ('CAREGIVER', 'Caregiver'),
        ('OTHER', 'Other'),
    ])
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    notification_enabled = models.BooleanField(default=True)
    fcm_token = models.CharField(max_length=255, blank=True, help_text="Firebase Cloud Messaging token")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.relationship} of {self.patient.name})"

class HealthData(models.Model):
    """Model storing health data from IoT devices"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='health_data')
    timestamp = models.DateTimeField(default=timezone.now)
    
    # Vital signs
    heart_rate = models.FloatField(help_text="Heart rate in BPM")
    spo2 = models.FloatField(help_text="Blood oxygen saturation in percentage")
    
    # Accelerometer data
    accelerometer_x = models.FloatField()
    accelerometer_y = models.FloatField()
    accelerometer_z = models.FloatField()
    
    # Gyroscope data
    gyroscope_x = models.FloatField()
    gyroscope_y = models.FloatField()
    gyroscope_z = models.FloatField()
    
    # Optional fields for future expansion
    temperature = models.FloatField(null=True, blank=True, help_text="Body temperature in Celsius")
    systolic_bp = models.IntegerField(null=True, blank=True, help_text="Systolic blood pressure")
    diastolic_bp = models.IntegerField(null=True, blank=True, help_text="Diastolic blood pressure")
    respiratory_rate = models.FloatField(null=True, blank=True, help_text="Respiratory rate in breaths per minute")
    systolic_bp = models.IntegerField(null=True, blank=True, help_text="Systolic blood pressure")
    diastolic_bp = models.IntegerField(null=True, blank=True, help_text="Diastolic blood pressure")
    respiratory_rate = models.FloatField(null=True, blank=True, help_text="Respiratory rate in breaths per minute")
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Health data for {self.patient.name} at {self.timestamp}"

class Alert(models.Model):
    """Model for health alerts"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='alerts')
    timestamp = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=20, choices=[
        ('FALL', 'Fall Detection'),
        ('VITALS', 'Abnormal Vitals'),
        ('LOCATION', 'Location Alert'),
        ('ACTIVITY', 'Activity Alert'),
        ('MEDICATION', 'Medication Reminder'),
        ('OTHER', 'Other')
    ])
    message = models.TextField()
    health_data = models.ForeignKey(HealthData, on_delete=models.SET_NULL, null=True, blank=True, related_name='alerts')
    status = models.CharField(max_length=20, default='NEW', choices=[
        ('NEW', 'New'),
        ('ACKNOWLEDGED', 'Acknowledged'),
        ('RESOLVED', 'Resolved'),
        ('FALSE_ALARM', 'False Alarm')
    ])
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.type} alert for {self.patient.name} at {self.timestamp}"
    
    def acknowledge(self):
        """Mark alert as acknowledged"""
        self.status = 'ACKNOWLEDGED'
        self.save()
    
    def resolve(self):
        """Mark alert as resolved"""
        self.status = 'RESOLVED'
        self.resolved_at = timezone.now()
        self.save()