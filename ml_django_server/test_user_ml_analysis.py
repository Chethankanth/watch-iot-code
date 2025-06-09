"""
Test script to analyze specific user health data from the Django database
"""
import os
import sys
import json
import numpy as np
import django
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from tabulate import tabulate
import time

# Add the project directory to path so we can import modules
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(project_dir, "health_monitor_server"))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_monitor.settings')
django.setup()

# Import Django models and ML predictor
from api.models import HealthData, Patient, Alert
from api.ml_predictor import HealthPredictor

def get_patient_list():
    """Get list of patients with health data"""
    patients = Patient.objects.filter(health_data__isnull=False).distinct()
    return patients

def get_patient_health_data(patient_id, limit=20):
    """Get health data for a specific patient"""
    try:
        # Get the most recent health data entries for the patient
        health_data = HealthData.objects.filter(patient_id=patient_id).order_by('-timestamp')[:limit]
        
        if not health_data:
            print(f"No health data found for patient_id: {patient_id}")
            return None
        
        return health_data
    except Exception as e:
        print(f"Error fetching health data: {e}")
        return None

def analyze_vitals(predictor, health_data):
    """Analyze vital signs for user"""
    print("\nVital Signs Analysis:")
    print("---------------------")
    
    # Get the most recent health data entry
    latest_data = health_data[0]
    
    # Analyze the most recent vital signs
    heart_rate = latest_data.heart_rate
    spo2 = latest_data.spo2
    
    print(f"Latest readings (at {latest_data.timestamp}):")
    print(f"Heart Rate: {heart_rate} bpm")
    print(f"SpO2: {spo2}%")
    
    # Get prediction
    start_time = time.time()
    result = predictor.predict_vitals_risk(heart_rate=heart_rate, spo2=spo2)
    prediction_time = time.time() - start_time
    
    print("\nRisk Assessment:")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Risk Probability: {result['risk_probability']:.2%}")
    print(f"Anomaly Detected: {'Yes' if result['is_anomaly'] else 'No'}")
    print(f"Analysis Time: {prediction_time:.4f} seconds")
    
    # Interpret results
    if result['is_anomaly']:
        if result['risk_level'] == 'High':
            print("\nINTERPRETATION: Patient's vital signs indicate a high-risk condition")
            print("Recommended action: Immediate medical attention may be required")
        elif result['risk_level'] == 'Moderate':
            print("\nINTERPRETATION: Patient's vital signs show moderate risk")
            print("Recommended action: Increased monitoring and caution advised")
    else:
        print("\nINTERPRETATION: Patient's vital signs are within normal ranges")
        print("Recommended action: Continue regular monitoring")
    
    return result

def analyze_movement(predictor, health_data):
    """Analyze movement data for fall detection"""
    print("\nMovement Analysis:")
    print("-----------------")
    
    # Get accelerometer and gyroscope data from recent entries
    # Using only a few entries for simplicity
    sample_size = min(10, len(health_data))
    recent_data = health_data[:sample_size]
    
    acc_x = [data.accelerometer_x for data in recent_data]
    acc_y = [data.accelerometer_y for data in recent_data]
    acc_z = [data.accelerometer_z for data in recent_data]
    gyr_x = [data.gyroscope_x for data in recent_data]
    gyr_y = [data.gyroscope_y for data in recent_data]
    gyr_z = [data.gyroscope_z for data in recent_data]
    
    print(f"Analyzing {sample_size} recent movement data points")
    
    # Display sample of sensor data
    if sample_size > 0:
        print("\nSample sensor readings (most recent):")
        headers = ["Sensor", "X", "Y", "Z", "Magnitude"]
        
        # Calculate magnitudes
        acc_mag = np.sqrt(recent_data[0].accelerometer_x**2 + 
                         recent_data[0].accelerometer_y**2 + 
                         recent_data[0].accelerometer_z**2)
        
        gyr_mag = np.sqrt(recent_data[0].gyroscope_x**2 + 
                         recent_data[0].gyroscope_y**2 + 
                         recent_data[0].gyroscope_z**2)
        
        table_data = [
            ["Accelerometer", 
             f"{recent_data[0].accelerometer_x:.2f}", 
             f"{recent_data[0].accelerometer_y:.2f}", 
             f"{recent_data[0].accelerometer_z:.2f}",
             f"{acc_mag:.2f}"],
            ["Gyroscope", 
             f"{recent_data[0].gyroscope_x:.2f}", 
             f"{recent_data[0].gyroscope_y:.2f}", 
             f"{recent_data[0].gyroscope_z:.2f}",
             f"{gyr_mag:.2f}"]
        ]
        
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Get prediction
    start_time = time.time()
    result = predictor.predict_fall(acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z)
    prediction_time = time.time() - start_time
    
    print("\nFall Detection:")
    print(f"Fall Detected: {'Yes' if result['fall_detected'] else 'No'}")
    print(f"Fall Probability: {result['fall_probability']:.2%}")
    print(f"Analysis Time: {prediction_time:.4f} seconds")
    
    # Interpret results
    if result['fall_detected']:
        print("\nINTERPRETATION: Significant movement pattern detected")
        print(f"Confidence: {result['fall_probability']:.1%}")
        print("Recommended action: Check on patient")
    else:
        print("\nINTERPRETATION: No unusual movement patterns detected")
        print("Recommended action: Normal monitoring")
    
    return result

def analyze_trends(health_data, days=7):
    """Analyze trends in health data over time"""
    print("\nHealth Trends Analysis:")
    print("----------------------")
    
    # Calculate date threshold for trend analysis
    now = datetime.now()
    threshold_date = now - timedelta(days=days)
    
    # Filter data for the specified period
    filtered_data = [data for data in health_data if data.timestamp.replace(tzinfo=None) > threshold_date]
    
    if len(filtered_data) < 2:
        print(f"Insufficient data for trend analysis (need at least 2 data points in the last {days} days)")
        return None
    
    # Calculate averages and trends
    heart_rates = [data.heart_rate for data in filtered_data]
    spo2_values = [data.spo2 for data in filtered_data]
    timestamps = [data.timestamp for data in filtered_data]
    
    avg_hr = sum(heart_rates) / len(heart_rates)
    avg_spo2 = sum(spo2_values) / len(spo2_values)
    
    # Calculate standard deviation
    hr_std = np.std(heart_rates)
    spo2_std = np.std(spo2_values)
    
    # Calculate min/max values
    min_hr = min(heart_rates)
    max_hr = max(heart_rates)
    min_spo2 = min(spo2_values)
    max_spo2 = max(spo2_values)
    
    # Simple trend calculation (comparing first and last values)
    hr_trend = heart_rates[0] - heart_rates[-1]
    spo2_trend = spo2_values[0] - spo2_values[-1]
    
    # Display summary statistics
    print(f"Analysis period: Last {days} days ({len(filtered_data)} data points)")
    
    stats_headers = ["Vital Sign", "Average", "Min", "Max", "Std Dev", "Trend"]
    stats_data = [
        ["Heart Rate", f"{avg_hr:.1f} bpm", f"{min_hr:.1f}", f"{max_hr:.1f}", f"{hr_std:.2f}",
         f"{'↑' if hr_trend > 0 else '↓' if hr_trend < 0 else '→'}"],
        ["SpO2", f"{avg_spo2:.1f}%", f"{min_spo2:.1f}%", f"{max_spo2:.1f}%", f"{spo2_std:.2f}",
         f"{'↑' if spo2_trend > 0 else '↓' if spo2_trend < 0 else '→'}"]
    ]
    
    print("\n" + tabulate(stats_data, headers=stats_headers, tablefmt="grid"))
    
    # Clinical interpretation
    print("\nClinical Interpretation:")
    
    # Heart rate interpretation
    if avg_hr < 60:
        print("- Patient shows bradycardia (low heart rate)")
    elif avg_hr > 100:
        print("- Patient shows tachycardia (elevated heart rate)")
    else:
        print("- Patient's average heart rate is within normal range")
        
    # Heart rate variability interpretation
    if hr_std > 15:
        print(f"- Significant heart rate variability detected (std dev: {hr_std:.2f})")
    
    # SpO2 interpretation
    if avg_spo2 < 95:
        print("- Patient shows below-normal oxygen saturation")
        if avg_spo2 < 90:
            print("- Low SpO2 levels may indicate respiratory issues")
    else:
        print("- Patient's average SpO2 is within normal range")
    
    # Return analysis results
    return {
        'avg_hr': avg_hr,
        'avg_spo2': avg_spo2,
        'hr_trend': hr_trend,
        'spo2_trend': spo2_trend,
        'data_points': len(filtered_data)
    }

def get_patient_alerts(patient_id, limit=5):
    """Get recent alerts for a patient"""
    alerts = Alert.objects.filter(patient_id=patient_id).order_by('-timestamp')[:limit]
    return alerts

def display_patient_summary(patient):
    """Display patient summary information"""
    print("\n" + "="*60)
    print(f"PATIENT SUMMARY: {patient.name}".center(60))
    print("="*60)
    
    print(f"Patient ID: {patient.id}")
    print(f"Age: {patient.age}")
    print(f"Gender: {patient.gender}")
    
    # Get guardians
    guardians = patient.guardians.all()
    if guardians:
        print("\nEmergency Contacts:")
        for guardian in guardians:
            print(f"- {guardian.name}: {guardian.phone}")
    
    # Get alerts history
    alerts = get_patient_alerts(patient.id)
    if alerts:
        print("\nRecent Alerts:")
        for alert in alerts:
            print(f"- {alert.timestamp.strftime('%Y-%m-%d %H:%M')}: {alert.type} - {alert.message}")
    else:
        print("\nNo recent alerts.")

def main():
    print("=" * 70)
    print("PERSONALIZED HEALTH DATA ANALYSIS SYSTEM".center(70))
    print("=" * 70)
    
    # Initialize ML predictor
    print("\nInitializing ML models...")
    start_time = time.time()
    predictor = HealthPredictor()
    init_time = time.time() - start_time
    print(f"ML models initialized in {init_time:.2f} seconds")
    
    # Get list of patients with health data
    patients = get_patient_list()
    if not patients:
        print("No patients with health data found in the database.")
        return
    
    # Display available patients
    print("\nAvailable patients with health data:")
    patient_table = []
    for i, patient in enumerate(patients, 1):
        # Count health data entries
        data_count = HealthData.objects.filter(patient=patient).count()
        # Count alerts
        alert_count = Alert.objects.filter(patient=patient).count()
        
        patient_table.append([
            i,
            patient.id,
            patient.name,
            patient.age,
            patient.gender,
            data_count,
            alert_count
        ])
    
    headers = ["#", "ID", "Name", "Age", "Gender", "Data Points", "Alerts"]
    print("\n" + tabulate(patient_table, headers=headers, tablefmt="grid"))
    
    # Get patient selection
    while True:
        try:
            selection = int(input("\nSelect a patient to analyze (number): "))
            if 1 <= selection <= len(patients):
                selected_patient = patients[selection-1]
                break
            else:
                print(f"Please enter a number between 1 and {len(patients)}")
        except ValueError:
            print("Please enter a valid number")
    
    # Display patient summary
    display_patient_summary(selected_patient)
    
    # Get health data for selected patient
    print(f"\nFetching health data for analysis...")
    health_data = get_patient_health_data(selected_patient.id)
    
    if not health_data:
        print("No health data available for analysis.")
        return
    
    print(f"Found {len(health_data)} health data entries")
    
    # Perform analyses
    print("\n" + "="*70)
    print("HEALTH DATA ANALYSIS".center(70))
    print("="*70)
    
    vitals_result = analyze_vitals(predictor, health_data)
    movement_result = analyze_movement(predictor, health_data)
    trends_result = analyze_trends(health_data)
    
    # Overall assessment
    print("\n" + "=" * 70)
    print("COMPREHENSIVE HEALTH ASSESSMENT".center(70))
    print("=" * 70)
    
    # Determine overall status
    has_anomaly = vitals_result.get('is_anomaly', False)
    has_fall = movement_result.get('fall_detected', False)
    
    # Get high-risk factors
    risk_factors = []
    if has_anomaly:
        if vitals_result.get('risk_level') == 'High':
            risk_factors.append(f"Critical vital signs: HR={health_data[0].heart_rate}, SpO2={health_data[0].spo2}%")
        else:
            risk_factors.append(f"Abnormal vital signs: {vitals_result.get('risk_level')} risk")
    
    if has_fall:
        risk_factors.append(f"Potential fall detected ({movement_result.get('fall_probability', 0):.1%} confidence)")
    
    if trends_result:
        if trends_result.get('avg_hr', 0) > 100 or trends_result.get('avg_hr', 0) < 60:
            risk_factors.append(f"Abnormal average heart rate: {trends_result.get('avg_hr', 0):.1f} bpm")
        if trends_result.get('avg_spo2', 0) < 95:
            risk_factors.append(f"Below-normal average SpO2: {trends_result.get('avg_spo2', 0):.1f}%")
    
    # Display overall assessment
    if has_anomaly or has_fall:
        print("\n⚠️  ATTENTION NEEDED  ⚠️")
        print("\nIdentified risk factors:")
        for i, factor in enumerate(risk_factors, 1):
            print(f"{i}. {factor}")
        
        print("\nRecommended actions:")
        if has_anomaly and vitals_result.get('risk_level') == 'High':
            print("- Contact healthcare provider immediately")
            print("- Continuous monitoring of vital signs")
        else:
            print("- Increase monitoring frequency")
            print("- Check on patient's condition")
        
        if has_fall:
            print("- Verify patient's physical status")
            print("- Check for injuries or discomfort")
    else:
        print("\n✅  PATIENT STABLE  ✅")
        print("\nAll monitored parameters are within normal ranges:")
        print(f"- Current vital signs: HR={health_data[0].heart_rate} bpm, SpO2={health_data[0].spo2}%")
        print(f"- Vital signs assessment: {vitals_result.get('risk_level', 'Normal')}")
        print(f"- Fall detection: No falls detected")
        
        if trends_result:
            print(f"- Trend analysis: Stable patterns over {trends_result.get('data_points', 0)} data points")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()