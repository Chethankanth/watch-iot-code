from rest_framework import serializers
from .models import Patient, Guardian, HealthData, Alert

class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient model"""
    class Meta:
        model = Patient
        fields = [
            'id', 'name', 'age', 'gender', 'user_id', 
            'medical_history', 'emergency_contact', 
            'created_at', 'updated_at'
        ]

class GuardianSerializer(serializers.ModelSerializer):
    """Serializer for Guardian model"""
    patient_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Guardian
        fields = [
            'id', 'patient', 'patient_name', 'name', 'relationship',
            'phone_number', 'email', 'notification_enabled', 
            'fcm_token', 'created_at', 'updated_at'
        ]
    
    def get_patient_name(self, obj):
        return obj.patient.name if obj.patient else None

class HealthDataSerializer(serializers.ModelSerializer):
    """Serializer for HealthData model"""
    patient_name = serializers.SerializerMethodField()
    
    class Meta:
        model = HealthData
        fields = [
            'id', 'patient', 'patient_name', 'timestamp', 
            'heart_rate', 'spo2', 
            'accelerometer_x', 'accelerometer_y', 'accelerometer_z',
            'gyroscope_x', 'gyroscope_y', 'gyroscope_z',
            'temperature', 'systolic_bp', 'diastolic_bp', 'respiratory_rate'
        ]
    
    def get_patient_name(self, obj):
        return obj.patient.name if obj.patient else None

class AlertSerializer(serializers.ModelSerializer):
    """Serializer for Alert model"""
    patient_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Alert
        fields = [
            'id', 'patient', 'patient_name', 'timestamp', 
            'type', 'message', 'health_data', 'status', 
            'resolved_at'
        ]
    
    def get_patient_name(self, obj):
        return obj.patient.name if obj.patient else None