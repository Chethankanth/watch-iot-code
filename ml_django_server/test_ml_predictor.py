"""
Test script to check if the ML models are loading and working correctly
"""
import os
import sys
import numpy as np
import time
from tabulate import tabulate

# Add the project directory to path so we can import modules
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(project_dir, "health_monitor_server"))

# Import the ML predictor
from api.ml_predictor import HealthPredictor

def test_model_loading():
    """Test if models load properly"""
    print("Testing model loading...")
    start_time = time.time()
    predictor = HealthPredictor()
    load_time = time.time() - start_time
    print(f"Models loaded successfully in {load_time:.2f} seconds!")
    return predictor

def test_fall_detection(predictor):
    """Test fall detection prediction"""
    print("\nTesting fall detection model...")
    
    # Test with normal movement data
    print("\n1. Testing with normal movement data:")
    normal_result = predictor.predict_fall(
        acc_x=[0.1, 0.2, 0.1], 
        acc_y=[0.2, 0.3, 0.2], 
        acc_z=[9.8, 9.7, 9.8],  # Approximate gravity
        gyr_x=[0.1, 0.2, 0.1],
        gyr_y=[0.1, 0.2, 0.1],
        gyr_z=[0.1, 0.2, 0.1]
    )
    print(f"Fall detected: {normal_result['fall_detected']}")
    print(f"Fall probability: {normal_result['fall_probability']:.2%}")
    
    # Test with fall-like movement data
    print("\n2. Testing with fall-like movement data:")
    fall_result = predictor.predict_fall(
        acc_x=[2.5, 3.7, 4.2], 
        acc_y=[-3.7, -4.5, -2.1], 
        acc_z=[0.8, 1.2, 2.5],  # Significant deviation from gravity
        gyr_x=[75.0, 85.0, 65.0],  # High angular velocity
        gyr_y=[-60.0, -75.0, -45.0],
        gyr_z=[45.0, 55.0, 35.0]
    )
    print(f"Fall detected: {fall_result['fall_detected']}")
    print(f"Fall probability: {fall_result['fall_probability']:.2%}")

def test_vitals_risk_assessment(predictor):
    """Test vital signs risk assessment model"""
    print("\nTesting vital signs risk assessment model...")
    
    # Test with normal vitals
    print("\n1. Testing with normal vital signs:")
    normal_result = predictor.predict_vitals_risk(heart_rate=75.0, spo2=98.0)
    print(f"Risk level: {normal_result['risk_level']}")
    print(f"Risk probability: {normal_result['risk_probability']:.2%}")
    print(f"Is anomaly: {normal_result['is_anomaly']}")
    
    # Test with abnormal vitals - high heart rate, low SpO2
    print("\n2. Testing with abnormal vital signs (high HR, low SpO2):")
    abnormal_result = predictor.predict_vitals_risk(heart_rate=120.0, spo2=88.0)
    print(f"Risk level: {abnormal_result['risk_level']}")
    print(f"Risk probability: {abnormal_result['risk_probability']:.2%}")
    print(f"Is anomaly: {abnormal_result['is_anomaly']}")
    
    # Test with moderately concerning vitals
    print("\n3. Testing with moderately concerning vital signs:")
    moderate_result = predictor.predict_vitals_risk(heart_rate=95.0, spo2=93.0)
    print(f"Risk level: {moderate_result['risk_level']}")
    print(f"Risk probability: {moderate_result['risk_probability']:.2%}")
    print(f"Is anomaly: {moderate_result['is_anomaly']}")

def test_with_patient_data(predictor):
    """Test the model with sample patient data profiles"""
    print("\n" + "="*50)
    print("TESTING WITH PATIENT PROFILES")
    print("="*50)
    
    # Define patient profiles
    patients = [
        {
            "name": "Elderly Patient (75 years)",
            "vitals": {
                "heart_rate": 82,
                "spo2": 94
            },
            "movement": {
                "acc_x": [0.2, 0.3, 0.2, 0.1, 0.3],
                "acc_y": [0.3, 0.2, 0.4, 0.3, 0.2],
                "acc_z": [9.7, 9.8, 9.6, 9.7, 9.8],
                "gyr_x": [0.2, 0.3, 0.2, 0.1, 0.2],
                "gyr_y": [0.3, 0.2, 0.1, 0.3, 0.2],
                "gyr_z": [0.1, 0.2, 0.3, 0.2, 0.1]
            }
        },
        {
            "name": "Athlete (25 years)",
            "vitals": {
                "heart_rate": 55,
                "spo2": 99
            },
            "movement": {
                "acc_x": [1.2, 1.5, 1.3, 1.4, 1.2],
                "acc_y": [1.1, 1.3, 1.2, 1.0, 1.1],
                "acc_z": [9.5, 9.3, 9.4, 9.6, 9.5],
                "gyr_x": [5.2, 5.5, 5.3, 5.1, 5.2],
                "gyr_y": [4.3, 4.5, 4.2, 4.1, 4.3],
                "gyr_z": [3.1, 3.3, 3.2, 3.0, 3.1]
            }
        },
        {
            "name": "Patient in Distress",
            "vitals": {
                "heart_rate": 125,
                "spo2": 87
            },
            "movement": {
                "acc_x": [3.2, 4.5, 5.3, 4.4, 3.2],
                "acc_y": [-2.1, -3.3, -4.2, -3.0, -2.1],
                "acc_z": [2.5, 1.3, 0.4, 1.6, 2.5],
                "gyr_x": [45.2, 65.5, 75.3, 65.1, 45.2],
                "gyr_y": [-35.3, -55.5, -65.2, -55.1, -35.3],
                "gyr_z": [25.1, 45.3, 55.2, 45.0, 25.1]
            }
        }
    ]
    
    # Test each patient profile
    results = []
    
    for patient in patients:
        print(f"\nAnalyzing patient: {patient['name']}")
        
        # Get vitals prediction
        vitals_result = predictor.predict_vitals_risk(
            heart_rate=patient['vitals']['heart_rate'],
            spo2=patient['vitals']['spo2']
        )
        
        # Get fall prediction
        fall_result = predictor.predict_fall(
            acc_x=patient['movement']['acc_x'],
            acc_y=patient['movement']['acc_y'],
            acc_z=patient['movement']['acc_z'],
            gyr_x=patient['movement']['gyr_x'],
            gyr_y=patient['movement']['gyr_y'],
            gyr_z=patient['movement']['gyr_z']
        )
        
        # Print results
        print(f"Vitals - HR: {patient['vitals']['heart_rate']} bpm, SpO2: {patient['vitals']['spo2']}%")
        print(f"Risk Level: {vitals_result['risk_level']}")
        print(f"Risk Probability: {vitals_result['risk_probability']:.2%}")
        print(f"Anomaly Detected: {'Yes' if vitals_result['is_anomaly'] else 'No'}")
        
        print(f"Fall Detected: {'Yes' if fall_result['fall_detected'] else 'No'}")
        print(f"Fall Probability: {fall_result['fall_probability']:.2%}")
        
        # Add to results table
        results.append([
            patient['name'],
            f"{patient['vitals']['heart_rate']} / {patient['vitals']['spo2']}%",
            vitals_result['risk_level'],
            f"{vitals_result['risk_probability']:.2%}",
            'Yes' if vitals_result['is_anomaly'] else 'No',
            'Yes' if fall_result['fall_detected'] else 'No',
            f"{fall_result['fall_probability']:.2%}"
        ])
    
    # Display results table
    print("\n" + "="*80)
    print("PATIENT PROFILES ANALYSIS RESULTS".center(80))
    print("="*80)
    
    headers = ["Patient", "HR/SpO2", "Risk Level", "Risk Prob", "Anomaly", "Fall", "Fall Prob"]
    print("\n" + tabulate(results, headers=headers, tablefmt="grid"))

def main():
    print("=" * 60)
    print("ML PREDICTOR TESTING SCRIPT".center(60))
    print("=" * 60)
    
    # Test model loading
    predictor = test_model_loading()
    
    # Test fall detection
    test_fall_detection(predictor)
    
    # Test vitals risk assessment
    test_vitals_risk_assessment(predictor)
    
    # Test with patient profiles
    test_with_patient_data(predictor)
    
    print("\n" + "=" * 60)
    print("TESTING COMPLETED SUCCESSFULLY".center(60))
    print("=" * 60)

if __name__ == "__main__":
    main()