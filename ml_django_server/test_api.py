"""
Test script for Health Monitor API
"""
import os
import sys
import json
import requests
import django
from datetime import datetime, timedelta
import random

# Add the project directory to path so we can import modules
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(project_dir, "health_monitor_server"))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_monitor.settings')
django.setup()

# Import Django models
from api.models import Patient, HealthData, Alert, Guardian

# Base URL for API (assuming local development server)
BASE_URL = "http://127.0.0.1:8000/api"

def test_patient_endpoints():
    """Test patient API endpoints"""
    print("\n" + "="*50)
    print("TESTING PATIENT ENDPOINTS")
    print("="*50)
    
    # Get all patients
    print("\n1. Get all patients")
    try:
        response = requests.get(f"{BASE_URL}/patients/")
        if response.status_code == 200:
            patients = response.json()
            print(f"Success! Found {len(patients)} patients")
            if patients:
                print(f"Sample patient: {patients[0]['name']}")
        else:
            print(f"Error: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")
    
    # Get patients directly from database
    all_patients = Patient.objects.all()
    if all_patients:
        test_patient = all_patients[0]
        patient_id = test_patient.id
        
        # Get specific patient
        print(f"\n2. Get patient with ID {patient_id}")
        try:
            response = requests.get(f"{BASE_URL}/patients/{patient_id}/")
            if response.status_code == 200:
                patient = response.json()
                print(f"Success! Retrieved patient: {patient['name']}")
            else:
                print(f"Error: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Request failed: {e}")
    else:
        print("\nNo patients in database to test specific patient endpoint")

def test_health_data_endpoints():
    """Test health data API endpoints"""
    print("\n" + "="*50)
    print("TESTING HEALTH DATA ENDPOINTS")
    print("="*50)
    
    # Get all health data
    print("\n1. Get all health data")
    try:
        response = requests.get(f"{BASE_URL}/health-data/")
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Found {len(data)} health data entries")
            if data:
                print(f"Sample data: HR={data[0]['heart_rate']}, SpO2={data[0]['spo2']}")
        else:
            print(f"Error: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")
    
    # Get patients directly from database
    all_patients = Patient.objects.all()
    if all_patients:
        test_patient = all_patients[0]
        patient_id = test_patient.id
        
        # Get health data for specific patient
        print(f"\n2. Get health data for patient with ID {patient_id}")
        try:
            response = requests.get(f"{BASE_URL}/patients/{patient_id}/health-data/")
            if response.status_code == 200:
                data = response.json()
                print(f"Success! Found {len(data)} health data entries for {test_patient.name}")
                if data:
                    print(f"Latest data: HR={data[0]['heart_rate']}, SpO2={data[0]['spo2']}")
            else:
                print(f"Error: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Request failed: {e}")
        
        # Create test data
        print("\n3. Create new health data entry")
        try:
            # Generate random health data
            hr = random.randint(60, 100)
            spo2 = random.randint(95, 100)
            acc_x = random.uniform(-1, 1)
            acc_y = random.uniform(-1, 1)
            acc_z = random.uniform(-1, 1)
            gyr_x = random.uniform(-10, 10)
            gyr_y = random.uniform(-10, 10)
            gyr_z = random.uniform(-10, 10)
            
            data = {
                "patient": patient_id,
                "heart_rate": hr,
                "spo2": spo2,
                "accelerometer_x": acc_x,
                "accelerometer_y": acc_y,
                "accelerometer_z": acc_z,
                "gyroscope_x": gyr_x,
                "gyroscope_y": gyr_y,
                "gyroscope_z": gyr_z
            }
            
            response = requests.post(f"{BASE_URL}/health-data/", json=data)
            if response.status_code == 201:
                new_data = response.json()
                print(f"Success! Created new health data entry with ID {new_data['id']}")
                print(f"Data: HR={new_data['heart_rate']}, SpO2={new_data['spo2']}")
            else:
                print(f"Error: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Request failed: {e}")
    else:
        print("\nNo patients in database to test health data endpoints")

def test_alert_endpoints():
    """Test alert API endpoints"""
    print("\n" + "="*50)
    print("TESTING ALERT ENDPOINTS")
    print("="*50)
    
    # Get all alerts
    print("\n1. Get all alerts")
    try:
        response = requests.get(f"{BASE_URL}/alerts/")
        if response.status_code == 200:
            alerts = response.json()
            print(f"Success! Found {len(alerts)} alerts")
            if alerts:
                print(f"Sample alert: {alerts[0]['message']}")
        else:
            print(f"Error: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")
    
    # Get patients directly from database
    all_patients = Patient.objects.all()
    all_health_data = HealthData.objects.all()
    
    if all_patients and all_health_data:
        test_patient = all_patients[0]
        test_health_data = all_health_data[0]
        patient_id = test_patient.id
        
        # Get alerts for specific patient
        print(f"\n2. Get alerts for patient with ID {patient_id}")
        try:
            response = requests.get(f"{BASE_URL}/patients/{patient_id}/alerts/")
            if response.status_code == 200:
                alerts = response.json()
                print(f"Success! Found {len(alerts)} alerts for {test_patient.name}")
                if alerts:
                    print(f"Sample alert: {alerts[0]['message']}")
            else:
                print(f"Error: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Request failed: {e}")
        
        # Create test alert
        print("\n3. Create new alert")
        try:
            alert_data = {
                "patient": patient_id,
                "type": "VITALS",
                "message": "Test alert from API test script",
                "health_data": test_health_data.id,
                "status": "NEW"
            }
            
            response = requests.post(f"{BASE_URL}/alerts/", json=alert_data)
            if response.status_code == 201:
                new_alert = response.json()
                print(f"Success! Created new alert with ID {new_alert['id']}")
                print(f"Alert message: {new_alert['message']}")
            else:
                print(f"Error: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Request failed: {e}")
    else:
        print("\nNo patients or health data in database to test alert endpoints")

def test_guardian_endpoints():
    """Test guardian API endpoints"""
    print("\n" + "="*50)
    print("TESTING GUARDIAN ENDPOINTS")
    print("="*50)
    
    # Get all guardians
    print("\n1. Get all guardians")
    try:
        response = requests.get(f"{BASE_URL}/guardians/")
        if response.status_code == 200:
            guardians = response.json()
            print(f"Success! Found {len(guardians)} guardians")
            if guardians:
                print(f"Sample guardian: {guardians[0]['name']}")
        else:
            print(f"Error: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")
    
    # Get patients directly from database
    all_patients = Patient.objects.all()
    
    if all_patients:
        test_patient = all_patients[0]
        patient_id = test_patient.id
        
        # Get guardians for specific patient
        print(f"\n2. Get guardians for patient with ID {patient_id}")
        try:
            response = requests.get(f"{BASE_URL}/patients/{patient_id}/guardians/")
            if response.status_code == 200:
                guardians = response.json()
                print(f"Success! Found {len(guardians)} guardians for {test_patient.name}")
                if guardians:
                    print(f"Sample guardian: {guardians[0]['name']}")
            else:
                print(f"Error: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Request failed: {e}")
    else:
        print("\nNo patients in database to test guardian endpoints")

def main():
    print("\n" + "*"*70)
    print("HEALTH MONITOR API TEST".center(70))
    print("*"*70)
    
    print("\nStarting API tests... Make sure the Django server is running.")
    print("Run 'python manage.py runserver' in the health_monitor_server directory.")
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/patients/")
        if response.status_code == 200:
            print("\nDjango server is running. Proceeding with tests.")
        else:
            print(f"\nServer is running but returned status code {response.status_code}.")
    except requests.exceptions.ConnectionError:
        print("\nERROR: Could not connect to Django server.")
        print("Please start the server with 'python manage.py runserver' and try again.")
        return
    
    # Run all tests
    test_patient_endpoints()
    test_health_data_endpoints()
    test_alert_endpoints()
    test_guardian_endpoints()
    
    print("\n" + "*"*70)
    print("API TESTS COMPLETED".center(70))
    print("*"*70)

if __name__ == "__main__":
    main()