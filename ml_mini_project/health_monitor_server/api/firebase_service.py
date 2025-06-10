import firebase_admin
from firebase_admin import credentials, messaging
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class FirebaseService:
    """Service for Firebase integration and notifications"""
    
    def __init__(self):
        self.initialized = False
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
                print("Firebase Admin SDK initialized successfully")
            else:
                self.initialized = True
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
                
            # In a real app, you would store FCM tokens for each guardian
            # Here we'll assume there's a token field or we get it from Firebase
            token = self.get_guardian_token(guardian)
            
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
        """Get FCM token for a guardian - in a real app, this would come from your database"""
        # This is a placeholder. In a real app, you would store and retrieve FCM tokens
        # from your database or from Firebase Authentication
        
        # For testing purposes
        return "SAMPLE_FCM_TOKEN"  # Replace with actual token retrieval logic
        
    def add_health_data_to_firebase(self, patient_id, health_data):
        """Add health data to Firebase Realtime Database or Firestore"""
        # Implementation would depend on your Firebase database structure
        pass