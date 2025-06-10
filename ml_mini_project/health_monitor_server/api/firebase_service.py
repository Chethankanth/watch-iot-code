import firebase_admin
from firebase_admin import credentials, messaging, firestore
import os
import datetime
import json
from pathlib import Path
from django.forms.models import model_to_dict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class FirebaseService:
    """Service for Firebase integration and notifications"""
    
    def __init__(self):
        self.initialized = False
        self.db = None
        self.initialize_firebase()
    
    def initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            # The path where you would store your Firebase service account key
            service_account_path = os.path.join(BASE_DIR, 'health_monitor_server', 'firebase-key.json')
            
            # Check if credentials file exists
            if not os.path.exists(service_account_path):
                print(f"Firebase credentials file not found at {service_account_path}")
                self.initialized = False
                return
            
            # Initialize the app if not already initialized
            if not firebase_admin._apps:
                cred = credentials.Certificate(service_account_path)
                firebase_admin.initialize_app(cred)
                self.initialized = True
                self.db = firestore.client()
                print("Firebase Admin SDK initialized successfully")
            else:
                self.initialized = True
                self.db = firestore.client()
                print("Firebase Admin SDK already initialized")
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            self.initialized = False
    
    def send_alert_notification(self, token, title, body, data=None):
        """Send notification to a specific device token"""
        if not self.initialized:
            print("Firebase not initialized, cannot send notification")
            return False
        
        try:
            # Create message
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                data=data or {},
                token=token,
            )
            
            # Send message
            response = messaging.send(message)
            print(f"Successfully sent notification: {response}")
            return True
        except Exception as e:
            print(f"Error sending notification: {e}")
            return False
    
    def send_alert_to_guardians(self, guardians, patient_name, alert_type, alert_message):
        """Send notifications to all guardians of a patient"""
        if not self.initialized:
            print("Firebase not initialized, cannot send notifications to guardians")
            return False
        
        success = False
        
        for guardian in guardians:
            if not guardian.notification_enabled:
                continue
                
            # Get FCM token from Firebase
            token = guardian.fcm_token
            
            if token:
                title = f"Health Alert for {patient_name}"
                body = f"{alert_type}: {alert_message}"
                data = {
                    "alert_type": alert_type,
                    "patient_id": str(guardian.patient.id),
                    "guardian_id": str(guardian.id)
                }
                
                if self.send_alert_notification(token, title, body, data):
                    success = True
        
        return success
    
    def get_guardian_token(self, guardian):
        """Get FCM token for a guardian from Firestore"""
        if not self.initialized or not self.db:
            return None
        
        try:
            # Get guardian data from Firestore
            guardian_ref = self.db.collection('guardians').document(str(guardian.id))
            guardian_doc = guardian_ref.get()
            
            if guardian_doc.exists:
                guardian_data = guardian_doc.to_dict()
                return guardian_data.get('fcm_token', '')
            return ''
        except Exception as e:
            print(f"Error getting guardian token: {e}")
            return ''

    # Firebase Database Operations
    
    def save_patient(self, patient):
        """Save patient data to Firestore"""
        if not self.initialized or not self.db:
            print("Firebase not initialized, cannot save patient")
            return False
        
        try:
            # Convert Django model to dict
            patient_data = model_to_dict(patient)
            
            # Convert datetime objects to ISO format strings
            for key, value in patient_data.items():
                if isinstance(value, datetime.datetime):
                    patient_data[key] = value.isoformat()
            
            # Save to Firestore
            self.db.collection('patients').document(str(patient.id)).set(patient_data)
            print(f"Patient {patient.id} saved to Firebase")
            return True
        except Exception as e:
            print(f"Error saving patient to Firebase: {e}")
            return False
    
    def save_guardian(self, guardian):
        """Save guardian data to Firestore"""
        if not self.initialized or not self.db:
            print("Firebase not initialized, cannot save guardian")
            return False
        
        try:
            # Convert Django model to dict
            guardian_data = model_to_dict(guardian)
            
            # Convert datetime objects to ISO format strings
            for key, value in guardian_data.items():
                if isinstance(value, datetime.datetime):
                    guardian_data[key] = value.isoformat()
            
            # Replace patient with patient_id
            if 'patient' in guardian_data and guardian_data['patient']:
                guardian_data['patient_id'] = str(guardian_data['patient'].id)
                del guardian_data['patient']
            
            # Save to Firestore
            self.db.collection('guardians').document(str(guardian.id)).set(guardian_data)
            print(f"Guardian {guardian.id} saved to Firebase")
            return True
        except Exception as e:
            print(f"Error saving guardian to Firebase: {e}")
            return False
    
    def add_health_data_to_firebase(self, patient_id, health_data):
        """Add health data to Firestore"""
        if not self.initialized or not self.db:
            print("Firebase not initialized, cannot save health data")
            return False
        
        try:
            # Convert Django model to dict
            data_dict = model_to_dict(health_data)
            
            # Convert datetime objects to ISO format strings
            for key, value in data_dict.items():
                if isinstance(value, datetime.datetime):
                    data_dict[key] = value.isoformat()
            
            # Replace patient with patient_id
            if 'patient' in data_dict and data_dict['patient']:
                data_dict['patient_id'] = str(data_dict['patient'].id)
                del data_dict['patient']
            
            # Save to Firestore
            self.db.collection('health_data').document(str(health_data.id)).set(data_dict)
            print(f"Health data {health_data.id} saved to Firebase")
            return True
        except Exception as e:
            print(f"Error saving health data to Firebase: {e}")
            return False
    
    def save_alert(self, alert):
        """Save alert data to Firestore"""
        if not self.initialized or not self.db:
            print("Firebase not initialized, cannot save alert")
            return False
        
        try:
            # Convert Django model to dict
            alert_data = model_to_dict(alert)
            
            # Convert datetime objects to ISO format strings
            for key, value in alert_data.items():
                if isinstance(value, datetime.datetime):
                    alert_data[key] = value.isoformat()
            
            # Replace related objects with their IDs
            if 'patient' in alert_data and alert_data['patient']:
                alert_data['patient_id'] = str(alert_data['patient'].id)
                del alert_data['patient']
            
            if 'health_data' in alert_data and alert_data['health_data']:
                alert_data['health_data_id'] = str(alert_data['health_data'].id)
                del alert_data['health_data']
            
            # Save to Firestore
            self.db.collection('alerts').document(str(alert.id)).set(alert_data)
            print(f"Alert {alert.id} saved to Firebase")
            return True
        except Exception as e:
            print(f"Error saving alert to Firebase: {e}")
            return False

    # Methods to retrieve data from Firebase
    
    def get_all_patients(self):
        """Get all patients from Firestore"""
        if not self.initialized or not self.db:
            print("Firebase not initialized, cannot get patients")
            return []
        
        try:
            patients = []
            patient_docs = self.db.collection('patients').stream()
            
            for doc in patient_docs:
                patient_data = doc.to_dict()
                patient_data['id'] = doc.id
                patients.append(patient_data)
            
            return patients
        except Exception as e:
            print(f"Error getting patients from Firebase: {e}")
            return []

    def get_patient(self, patient_id):
        """Get patient by ID from Firestore"""
        if not self.initialized or not self.db:
            print("Firebase not initialized, cannot get patient")
            return None
        
        try:
            doc_ref = self.db.collection('patients').document(str(patient_id))
            doc = doc_ref.get()
            
            if doc.exists:
                patient_data = doc.to_dict()
                patient_data['id'] = doc.id
                return patient_data
            return None
        except Exception as e:
            print(f"Error getting patient from Firebase: {e}")
            return None