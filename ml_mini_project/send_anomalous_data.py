"""
Script to send anomalous health data through the API and trigger alerts
"""
import os
import sys
import requests
import json
import random

def send_anomalous_data():
    """Send anomalous health data to the API"""
    print("\n" + "="*70)
    print("ANOMALOUS DATA SENDER".center(70))
    print("="*70)
    
    # API endpoint
    api_url = input("\nEnter API URL (default: http://127.0.0.1:8000/api/health-data/): ") or "http://127.0.0.1:8000/api/health-data/"
    
    # Get user ID
    user_id = input("\nEnter user ID (must exist in database): ")
    if not user_id:
        print("User ID is required. Please try again.")
        return
    
    # Select anomaly type
    print("\nAnomaly types:")
    print("1. High Heart Rate (tachycardia)")
    print("2. Low Heart Rate (bradycardia)")
    print("3. Low Blood Oxygen (hypoxemia)")
    print("4. Critical Condition (tachycardia + hypoxemia)")
    print("5. Critical Condition (bradycardia + hypoxemia)")
    print("6. Fall Detection")
    print("7. Critical Condition with Fall")
    print("8. Random Anomaly")
    
    try:
        anomaly_type = int(input("\nSelect anomaly type (1-8): "))
        if not 1 <= anomaly_type <= 8:
            print("Invalid selection. Using Random Anomaly.")
            anomaly_type = 8
    except ValueError:
        print("Invalid selection. Using Random Anomaly.")
        anomaly_type = 8
    
    # Generate anomalous data based on selection
    if anomaly_type == 1:  # High Heart Rate
        heart_rate = random.randint(120, 160)
        spo2 = random.randint(95, 100)
        anomaly_name = "High Heart Rate"
    elif anomaly_type == 2:  # Low Heart Rate
        heart_rate = random.randint(35, 50)
        spo2 = random.randint(95, 100)
        anomaly_name = "Low Heart Rate"
    elif anomaly_type == 3:  # Low SpO2
        heart_rate = random.randint(60, 100)
        spo2 = random.randint(80, 89)
        anomaly_name = "Low Blood Oxygen"
    elif anomaly_type == 4:  # Critical 1
        heart_rate = random.randint(120, 160)
        spo2 = random.randint(80, 89)
        anomaly_name = "Critical Condition (High HR, Low SpO2)"
    elif anomaly_type == 5:  # Critical 2
        heart_rate = random.randint(35, 50)
        spo2 = random.randint(80, 89)
        anomaly_name = "Critical Condition (Low HR, Low SpO2)"
    elif anomaly_type == 6:  # Fall
        heart_rate = random.randint(60, 100)
        spo2 = random.randint(95, 100)
        anomaly_name = "Fall Detection"
    elif anomaly_type == 7:  # Critical with Fall
        heart_rate = random.randint(120, 160)
        spo2 = random.randint(80, 89)
        anomaly_name = "Critical Condition with Fall"
    else:  # Random
        heart_rate = random.randint(30, 180)
        spo2 = random.randint(75, 100)
        anomaly_name = "Random Anomaly"
    
    # Generate movement data - possibly fall-like for fall conditions
    if anomaly_type in [6, 7]:  # Fall scenarios
        acc_x = random.uniform(3.0, 8.0)
        acc_y = random.uniform(-8.0, -3.0)
        acc_z = random.uniform(0.5, 4.0)
        gyr_x = random.uniform(40.0, 80.0)
        gyr_y = random.uniform(-80.0, -40.0)
        gyr_z = random.uniform(30.0, 70.0)
    else:
        acc_x = random.uniform(-1.0, 1.0)
        acc_y = random.uniform(-1.0, 1.0)
        acc_z = random.uniform(9.0, 10.0)
        gyr_x = random.uniform(-5.0, 5.0)
        gyr_y = random.uniform(-5.0, 5.0)
        gyr_z = random.uniform(-5.0, 5.0)
    
    # Create data payload
    data = {
        "user_id": user_id,
        "heart_rate": heart_rate,
        "spo2": spo2,
        "accelerometer_x": acc_x,
        "accelerometer_y": acc_y,
        "accelerometer_z": acc_z,
        "gyroscope_x": gyr_x,
        "gyroscope_y": gyr_y,
        "gyroscope_z": gyr_z
    }
    
    # Preview data
    print("\n" + "-"*70)
    print("Sending the following data:".center(70))
    print("-"*70)
    for key, value in data.items():
        print(f"{key}: {value}")
    
    # Confirm before sending
    confirm = input("\nSend this data? (y/n): ").lower()
    if confirm != 'y':
        print("Operation cancelled.")
        return
    
    # Send data to API
    try:
        print("\nSending data to API...")
        response = requests.post(api_url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Data sent successfully!")
            
            # Print results
            print("\n" + "-"*70)
            print("ML ANALYSIS RESULTS".center(70))
            print("-"*70)
            
            # Vitals assessment
            vitals = result.get('vitals_assessment', {})
            print(f"Vitals Risk Level: {vitals.get('risk_level', 'Unknown')}")
            print(f"Risk Probability: {vitals.get('risk_probability', 0) * 100:.2f}%")
            print(f"Vitals Anomaly Detected: {'Yes' if vitals.get('is_anomaly', False) else 'No'}")
            
            # Fall detection
            fall = result.get('fall_detection', {})
            print(f"\nFall Detected: {'Yes' if fall.get('is_anomaly', False) else 'No'}")
            print(f"Fall Probability: {fall.get('fall_probability', 0) * 100:.2f}%")
            
            # Alerts created
            alerts = result.get('alerts_created', [])
            if alerts:
                print(f"\n{len(alerts)} alert(s) created:")
                for alert in alerts:
                    print(f"- {alert.get('type')}: {alert.get('message')}")
            else:
                print("\nNo alerts were created")
            
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
    
    except Exception as e:
        print(f"\n❌ Error sending data: {e}")
        print("\nMake sure the Django server is running and accessible.")

def test_chat_api():
    """Test the new chat endpoint that uses LLM7.io"""
    print("\n" + "="*70)
    print("HEALTH ASSISTANT CHAT TEST".center(70))
    print("="*70)
    
    # API endpoint
    api_url = input("\nEnter Chat API URL (default: http://127.0.0.1:8000/api/chat/): ") or "http://127.0.0.1:8000/api/chat/"
    
    # Get patient ID (optional)
    patient_id = input("\nEnter patient ID (optional, press Enter to skip): ")
    
    chat_history = []
    
    print("\n" + "-"*70)
    print("HEALTH ASSISTANT CHAT".center(70))
    print("-"*70)
    print("Type 'exit' to end the conversation")
    print("-"*70)
    
    while True:
        # Get user message
        user_message = input("\nYou: ")
        
        if user_message.lower() in ['exit', 'quit', 'bye']:
            print("\nEnding chat session. Goodbye!")
            break
        
        # Add to chat history
        chat_history.append({"text": user_message, "is_bot": False})
        
        # Create request data
        data = {
            "message": user_message,
            "chat_history": chat_history,
        }
        
        if patient_id:
            data["patient_id"] = patient_id
        
        # Send message to API
        try:
            response = requests.post(api_url, json=data)
            
            if response.status_code == 200:
                result = response.json()
                assistant_message = result.get('response', 'Sorry, I could not process your request.')
                
                # Display response
                print(f"\nAssistant: {assistant_message}")
                
                # Add to chat history
                chat_history.append({"text": assistant_message, "is_bot": True})
                
                # Keep chat history manageable
                if len(chat_history) > 10:
                    chat_history = chat_history[-10:]
            else:
                print(f"\n❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
        
        except Exception as e:
            print(f"\n❌ Error communicating with API: {e}")
            print("\nMake sure the Django server is running and accessible.")

def show_menu():
    """Display main menu"""
    while True:
        print("\n" + "="*70)
        print("HEALTH MONITORING SYSTEM TEST TOOLS".center(70))
        print("="*70)
        
        print("\n1. Send Anomalous Health Data")
        print("2. Test Health Assistant Chat")
        print("3. Exit")
        
        try:
            choice = int(input("\nEnter your choice (1-3): "))
            
            if choice == 1:
                send_anomalous_data()
            elif choice == 2:
                test_chat_api()
            elif choice == 3:
                print("\nExiting. Goodbye!")
                break
            else:
                print("Invalid choice, please try again")
        except ValueError:
            print("Please enter a valid number")

if __name__ == "__main__":
    show_menu()