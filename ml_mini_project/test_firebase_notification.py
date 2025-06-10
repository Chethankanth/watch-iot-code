"""
Test Firebase Notification Sending
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(project_dir, "health_monitor_server"))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_monitor.settings')
django.setup()

# Import Django models and Firebase service
from api.models import Patient, Guardian
from api.firebase_service import FirebaseService

def test_firebase_initialization():
    """Test if Firebase is properly initialized"""
    print("\n" + "="*70)
    print("FIREBASE CONFIGURATION TEST".center(70))
    print("="*70)
    
    # Get service account path
    base_dir = Path(__file__).resolve().parent
    service_account_path = os.path.join(base_dir, 'health_monitor_server', 'firebase-key.json')
    
    print(f"\nChecking for Firebase credentials at: {service_account_path}")
    
    if os.path.exists(service_account_path):
        print("✅ Firebase credentials file found")
    else:
        print("❌ Firebase credentials file NOT found at the expected location")
        print("   Please ensure you have a valid firebase-key.json file in the health_monitor_server directory")
        return False
    
    # Initialize Firebase service
    print("\nInitializing Firebase service...")
    firebase_service = FirebaseService()
    
    if firebase_service.initialized:
        print("✅ Firebase successfully initialized")
    else:
        print("❌ Firebase initialization failed")
        print("   Check the error messages above for more details")
        return False
    
    print("\nFirebase configuration is correct and ready to use!")
    return True

def test_notification_sending():
    """Test sending a notification"""
    print("\n" + "="*70)
    print("FIREBASE NOTIFICATION TEST".center(70))
    print("="*70)
    
    # Only proceed if Firebase is initialized
    if not test_firebase_initialization():
        return
    
    firebase_service = FirebaseService()
    
    # Get list of patients
    patients = Patient.objects.all()
    
    if not patients:
        print("\n❌ No patients found in the database")
        print("   Please create patients first")
        return
    
    # Display available patients
    print("\nAvailable patients:")
    for i, patient in enumerate(patients, 1):
        print(f"{i}. {patient.name} (ID: {patient.id})")
    
    # Get patient selection or use default
    try:
        selection = int(input("\nSelect a patient to test notifications (number) or press Enter for first patient: ") or "1")
        if 1 <= selection <= len(patients):
            selected_patient = patients[selection-1]
        else:
            print(f"Invalid selection, using first patient")
            selected_patient = patients[0]
    except ValueError:
        print(f"Invalid input, using first patient")
        selected_patient = patients[0]
    
    print(f"\nSelected patient: {selected_patient.name}")
    
    # Get or create a guardian
    guardians = Guardian.objects.filter(patient=selected_patient)
    
    if not guardians:
        print("\n❌ No guardians found for this patient")
        create_guardian = input("Would you like to create a test guardian? (y/n): ").lower()
        
        if create_guardian == 'y':
            guardian = Guardian.objects.create(
                patient=selected_patient,
                name="Test Guardian",
                relationship="Other",
                phone_number="1234567890",
                email="test@example.com",
                notification_enabled=True
            )
            print(f"✅ Created test guardian: {guardian.name}")
            guardians = [guardian]
        else:
            print("Cannot test notifications without guardians")
            return
    else:
        print(f"\nFound {len(guardians)} guardians for this patient")
    
    # Send test notification
    print("\nSending test notification...")
    
    # In a real-world app, you would need to set up FCM tokens properly
    # This is a simplified test
    
    # For testing, we'll modify the token retrieval method temporarily
    original_get_token = firebase_service.get_guardian_token
    
    # Use test token - in a real app you would get this from the mobile app registration
    test_token = input("\nEnter FCM token for testing (press Enter to use a dummy token): ")
    if not test_token:
        test_token = "TEST_FCM_TOKEN"
        print(f"Using dummy token: {test_token}")
        print("Note: This token won't actually deliver a notification to any device")
    
    # Override the token method temporarily
    firebase_service.get_guardian_token = lambda g: test_token
    
    # Send the test notification
    success = firebase_service.send_alert_to_guardians(
        guardians,
        selected_patient.name,
        "Test Alert",
        "This is a test notification from your IoT Health Monitor"
    )
    
    # Restore original method
    firebase_service.get_guardian_token = original_get_token
    
    if success:
        print("\n✅ Test notification sent successfully!")
        print("   If you used a valid FCM token, the notification should appear on the registered device")
    else:
        print("\n❌ Failed to send test notification")
        print("   Check the error messages above for more details")

def show_menu():
    """Display menu and handle user selection"""
    while True:
        print("\n" + "="*70)
        print("FIREBASE CONFIGURATION TOOL".center(70))
        print("="*70)
        
        print("\n1. Test Firebase Initialization")
        print("2. Test Sending Notification")
        print("3. Exit")
        
        try:
            choice = int(input("\nEnter your choice (1-3): "))
            
            if choice == 1:
                test_firebase_initialization()
            elif choice == 2:
                test_notification_sending()
            elif choice == 3:
                print("\nExiting Firebase test tool")
                break
            else:
                print("Invalid choice, please try again")
        except ValueError:
            print("Please enter a valid number")

if __name__ == "__main__":
    show_menu()