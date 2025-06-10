"""
Firebase Repository - Handles all database operations with Firebase
"""
from .firebase_service import FirebaseService
from .models import Patient, Guardian, HealthData, Alert

class FirebaseRepository:
    """Repository pattern implementation for Firebase database operations"""
    
    def __init__(self):
        self.firebase_service = FirebaseService()
    
    # Patient operations
    
    def save_patient(self, patient):
        """Save a patient to Firebase"""
        return self.firebase_service.save_patient(patient)
    
    def get_patient(self, patient_id):
        """Get a patient by ID"""
        return self.firebase_service.get_patient(patient_id)
    
    def get_all_patients(self):
        """Get all patients"""
        return self.firebase_service.get_all_patients()
    
    def delete_patient(self, patient_id):
        """Delete a patient"""
        # Implement this method in firebase_service.py
        pass
    
    # Guardian operations
    
    def save_guardian(self, guardian):
        """Save a guardian to Firebase"""
        return self.firebase_service.save_guardian(guardian)
    
    def get_guardian(self, guardian_id):
        """Get a guardian by ID"""
        # Implement this method in firebase_service.py
        pass
    
    def get_patient_guardians(self, patient_id):
        """Get all guardians for a patient"""
        # Implement this method in firebase_service.py
        pass
    
    # Health data operations
    
    def save_health_data(self, health_data):
        """Save health data to Firebase"""
        return self.firebase_service.add_health_data_to_firebase(
            patient_id=health_data.patient.id if health_data.patient else None,
            health_data=health_data
        )
    
    def get_patient_health_data(self, patient_id, limit=20):
        """Get health data for a patient"""
        # Implement this method in firebase_service.py
        pass
    
    # Alert operations
    
    def save_alert(self, alert):
        """Save an alert to Firebase"""
        return self.firebase_service.save_alert(alert)
    
    def get_alert(self, alert_id):
        """Get an alert by ID"""
        # Implement this method in firebase_service.py
        pass
    
    def get_patient_alerts(self, patient_id, limit=20):
        """Get alerts for a patient"""
        # Implement this method in firebase_service.py
        pass
    
    def update_alert_status(self, alert_id, status):
        """Update the status of an alert"""
        # Implement this method in firebase_service.py
        pass