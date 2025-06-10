"""
Test script to verify that Firebase database is working correctly
"""
import os
import sys
import django
import time

# Set up Django environment
sys.path.append(os.path.join(os.path.dirname(__file__), 'health_monitor_server'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_monitor.settings')
django.setup()

from api.models import Patient, Guardian, HealthData, Alert
from api.firebase_repository import FirebaseRepository

def test_firebase_database():
    """Test Firebase database operations"""
    print("Testing Firebase Database Integration")
    print("=====================================")
    
    # Initialize Firebase repository
    firebase_repo = FirebaseRepository()
    
    # Check if Firebase is initialized
    if not firebase_repo.firebase_service.initialized:
        print("ERROR: Firebase is not initialized. Check your firebase-key.json file.")
        return False
    
    print("Firebase initialized successfully!")
    
    # Test patient operations
    print("\nTesting Patient Operations:")
    print("--------------------------")
    
    # Get all patients from Django database
    patients = Patient.objects.all()
    
    if not patients:
        print("No patients found in database. Please create a patient first.")
    else:
        # Save a patient to Firebase
        test_patient = patients[0]
        print(f"Saving patient '{test_patient.name}' (ID: {test_patient.id}) to Firebase...")
        
        if firebase_repo.save_patient(test_patient):
            print("SUCCESS: Patient saved to Firebase!")
        else:
            print("ERROR: Failed to save patient to Firebase.")
            
        # Get patient from Firebase
        print(f"Retrieving patient (ID: {test_patient.id}) from Firebase...")
        firebase_patient = firebase_repo.get_patient(test_patient.id)
        
        if firebase_patient:
            print(f"SUCCESS: Retrieved patient from Firebase: {firebase_patient.get('name')}")
        else:
            print("ERROR: Failed to retrieve patient from Firebase.")
    
    # Test health data operations
    print("\nTesting Health Data Operations:")
    print("-----------------------------")
    
    # Get all health data from Django database
    health_data = HealthData.objects.all().order_by('-timestamp')[:1]
    
    if not health_data:
        print("No health data found in database. Please send some health data first.")
    else:
        # Save health data to Firebase
        test_data = health_data[0]
        print(f"Saving health data (ID: {test_data.id}) to Firebase...")
        
        if firebase_repo.save_health_data(test_data):
            print("SUCCESS: Health data saved to Firebase!")
        else:
            print("ERROR: Failed to save health data to Firebase.")
    
    print("\nFirebase Database Test Complete!")
    print("Check the Firebase console to verify data was saved correctly.")
    print("Visit: https://console.firebase.google.com/")
    
    return True

if __name__ == "__main__":
    test_firebase_database()
    
    # Keep the console open on Windows
    if os.name == 'nt':
        print("\nPress Enter to exit...")
        input()