from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.shortcuts import render, redirect
from .models import Patient, Guardian, HealthData, Alert
from .serializers import PatientSerializer, GuardianSerializer, HealthDataSerializer, AlertSerializer
from .ml_predictor import HealthPredictor
from .firebase_service import FirebaseService
from .firebase_repository import FirebaseRepository
import json
import requests

def home(request):
    """Render the home page"""
    # Since we might have template directory issues, let's use HttpResponse directly
    from django.http import HttpResponse
    
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IoT Health Monitor System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #2980b9;
        }
        .card {
            background: #f9f9f9;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .footer {
            margin-top: 40px;
            border-top: 1px solid #eee;
            padding-top: 20px;
            text-align: center;
            font-size: 0.9em;
            color: #7f8c8d;
        }
        a {
            color: #3498db;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        code {
            background: #f8f8f8;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: monospace;
            border: 1px solid #ddd;
        }
    </style>
</head>
<body>
    <h1>IoT Health Monitoring System</h1>
    
    <div class="card">
        <h2>System Status: Online</h2>
        <p>The IoT Health Monitoring server is running correctly.</p>
    </div>
    
    <h2>Available Endpoints</h2>
    
    <div class="card">
        <h3>Admin Interface</h3>
        <p>Manage patients, guardians, and view health data:</p>
        <p><a href="/admin/" target="_blank">Go to Admin Interface</a></p>
    </div>
    
    <div class="card">
        <h3>API Endpoints</h3>
        <p>The following API endpoints are available:</p>
        <ul>
            <li><code>GET /api/patients/</code> - List all patients</li>
            <li><code>POST /api/patients/</code> - Register a new patient</li>
            <li><code>GET /api/patients/{id}/</code> - Get patient details</li>
            <li><code>GET /api/patients/{id}/guardians/</code> - Get patient's guardians</li>
            <li><code>GET /api/patients/{id}/alerts/</code> - Get patient's alerts</li>
            <li><code>POST /api/health-data/</code> - Send health data from IoT devices</li>
            <li><code>GET /api/guardians/</code> - List all guardians</li>
            <li><code>POST /api/guardians/</code> - Add a guardian</li>
            <li><code>GET /api/alerts/</code> - List all alerts</li>
            <li><code>POST /api/alerts/{id}/acknowledge/</code> - Acknowledge an alert</li>
            <li><code>POST /api/alerts/{id}/resolve/</code> - Resolve an alert</li>
            <li><code>POST /api/chat/</code> - Chat with health assistant</li>
        </ul>
    </div>
    
    <h2>Documentation</h2>
    
    <div class="card">
        <p>Please refer to the documentation provided with this system:</p>
        <ul>
            <li><strong>USER_MANUAL.md</strong> - Comprehensive guide for system users</li>
            <li><strong>FIREBASE_SETUP.md</strong> - Details on Firebase configuration</li>
            <li><strong>ANDROID_FIREBASE_SETUP.md</strong> - Guide for setting up Firebase in Android apps</li>
        </ul>
    </div>
    
    <div class="footer">
        <p>IoT Health Monitoring System &copy; 2025</p>
    </div>
</body>
</html>"""
    
    return HttpResponse(html)

# Initialize ML predictor, Firebase service, and Firebase repository
health_predictor = HealthPredictor()
firebase_service = FirebaseService()
firebase_repository = FirebaseRepository()

class PatientViewSet(viewsets.ModelViewSet):
    """API endpoint for patients"""
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    
    def perform_create(self, serializer):
        """Override create to save patient to Firebase"""
        patient = serializer.save()
        firebase_repository.save_patient(patient)
        return patient
    
    def perform_update(self, serializer):
        """Override update to save patient to Firebase"""
        patient = serializer.save()
        firebase_repository.save_patient(patient)
        return patient
    
    @action(detail=True, methods=['get'])
    def guardians(self, request, pk=None):
        """Get guardians for a specific patient"""
        patient = self.get_object()
        guardians = Guardian.objects.filter(patient=patient)
        serializer = GuardianSerializer(guardians, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def alerts(self, request, pk=None):
        """Get alerts for a specific patient"""
        patient = self.get_object()
        alerts = Alert.objects.filter(patient=patient).order_by('-timestamp')
        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def health_data(self, request, pk=None):
        """Get health data for a specific patient"""
        patient = self.get_object()
        health_data = HealthData.objects.filter(patient=patient).order_by('-timestamp')[:100]  # Get last 100 entries
        serializer = HealthDataSerializer(health_data, many=True)
        return Response(serializer.data)

class GuardianViewSet(viewsets.ModelViewSet):
    """API endpoint for guardians"""
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializer
    
    def perform_create(self, serializer):
        """Override create to save guardian to Firebase"""
        guardian = serializer.save()
        firebase_repository.save_guardian(guardian)
        return guardian
    
    def perform_update(self, serializer):
        """Override update to save guardian to Firebase"""
        guardian = serializer.save()
        firebase_repository.save_guardian(guardian)
        return guardian

class AlertViewSet(viewsets.ModelViewSet):
    """API endpoint for alerts"""
    queryset = Alert.objects.all().order_by('-timestamp')
    serializer_class = AlertSerializer
    
    def perform_create(self, serializer):
        """Override create to save alert to Firebase"""
        alert = serializer.save()
        firebase_repository.save_alert(alert)
        return alert
    
    def perform_update(self, serializer):
        """Override update to save alert to Firebase"""
        alert = serializer.save()
        firebase_repository.save_alert(alert)
        return alert
    
    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """Mark an alert as acknowledged"""
        alert = self.get_object()
        alert.status = 'ACKNOWLEDGED'
        alert.save()
        
        # Update in Firebase
        firebase_repository.save_alert(alert)
        
        serializer = AlertSerializer(alert)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Mark an alert as resolved"""
        alert = self.get_object()
        alert.status = 'RESOLVED'
        alert.save()
        
        # Update in Firebase
        firebase_repository.save_alert(alert)
        
        serializer = AlertSerializer(alert)
        return Response(serializer.data)

@api_view(['POST'])
def process_health_data(request):
    """Process health data from sensors and predict anomalies"""
    try:
        # Get data from request
        data = request.data
        user_id = data.get('user_id')
        
        # Validate required fields
        required_fields = ['heart_rate', 'spo2', 'accelerometer_x', 'accelerometer_y', 
                          'accelerometer_z', 'gyroscope_x', 'gyroscope_y', 'gyroscope_z']
        
        for field in required_fields:
            if field not in data:
                return Response({'error': f'Missing required field: {field}'}, 
                              status=status.HTTP_400_BAD_REQUEST)
        
        # Find patient by user_id
        try:
            patient = Patient.objects.get(user_id=user_id)
        except Patient.DoesNotExist:
            return Response({'error': f'Patient with user_id {user_id} not found'}, 
                           status=status.HTTP_404_NOT_FOUND)
        
        # Create health data entry
        health_data = HealthData.objects.create(
            patient=patient,
            heart_rate=data['heart_rate'],
            spo2=data['spo2'],
            accelerometer_x=data['accelerometer_x'],
            accelerometer_y=data['accelerometer_y'],
            accelerometer_z=data['accelerometer_z'],
            gyroscope_x=data['gyroscope_x'],
            gyroscope_y=data['gyroscope_y'],
            gyroscope_z=data['gyroscope_z']
        )
        
        # Save health data to Firebase
        firebase_repository.save_health_data(health_data)
        
        # Run ML predictions
        # 1. Fall detection
        fall_result = health_predictor.predict_fall(
            [data['accelerometer_x']], [data['accelerometer_y']], [data['accelerometer_z']],
            [data['gyroscope_x']], [data['gyroscope_y']], [data['gyroscope_z']]
        )
        
        # 2. Vitals risk assessment
        vitals_result = health_predictor.predict_vitals_risk(
            data['heart_rate'], data['spo2']
        )
        
        # Process results and create alerts if anomalies detected
        alerts_created = []
        
        # Check for fall
        if fall_result['is_anomaly']:
            fall_alert = Alert.objects.create(
                patient=patient,
                type='FALL',
                message=f"Fall detected with {fall_result['fall_probability']:.2%} confidence",
                health_data=health_data,
                status='NEW'
            )
            alerts_created.append(fall_alert)
            
            # Save alert to Firebase
            firebase_repository.save_alert(fall_alert)
            
            # Send notifications to guardians
            guardians = Guardian.objects.filter(patient=patient, notification_enabled=True)
            firebase_service.send_alert_to_guardians(
                guardians, 
                patient.name, 
                "Fall Detected", 
                f"A fall was detected with {fall_result['fall_probability']:.2%} confidence"
            )
        
        # Check for abnormal vitals
        if vitals_result['is_anomaly']:
            vitals_alert = Alert.objects.create(
                patient=patient,
                type='VITALS',
                message=f"Abnormal vitals detected: {vitals_result['risk_level']}. " +
                        f"HR: {data['heart_rate']}, SpO2: {data['spo2']}",
                health_data=health_data,
                status='NEW'
            )
            alerts_created.append(vitals_alert)
            
            # Save alert to Firebase
            firebase_repository.save_alert(vitals_alert)
            
            # Send notifications to guardians
            guardians = Guardian.objects.filter(patient=patient, notification_enabled=True)
            firebase_service.send_alert_to_guardians(
                guardians, 
                patient.name, 
                "Abnormal Vitals", 
                f"Abnormal vitals detected: {vitals_result['risk_level']}. " +
                f"HR: {data['heart_rate']}, SpO2: {data['spo2']}"
            )
        
        # Return results
        response_data = {
            'health_data_id': health_data.id,
            'fall_detection': fall_result,
            'vitals_assessment': vitals_result,
            'alerts_created': AlertSerializer(alerts_created, many=True).data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def chat_with_health_assistant(request):
    """
    Chat endpoint that integrates with llm7.io for health-related conversations
    """
    try:
        data = request.data
        message = data.get('message')
        patient_id = data.get('patient_id')
        chat_history = data.get('chat_history', [])
        
        if not message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get patient context if patient_id is provided
        patient_context = ""
        if patient_id:
            try:
                patient = Patient.objects.get(id=patient_id)
                # Get latest health data
                latest_health_data = HealthData.objects.filter(patient=patient).order_by('-timestamp').first()
                
                if latest_health_data:
                    patient_context = f"""
Patient Information:
- Name: {patient.name}
- Age: {patient.age}
- Latest Vital Signs:
  - Heart Rate: {latest_health_data.heart_rate} bpm
  - Blood Oxygen (SpO2): {latest_health_data.spo2}%
  - Timestamp: {latest_health_data.timestamp}
"""
            except Patient.DoesNotExist:
                patient_context = "Patient information not available."
        
        # Prepare the prompt for llm7.io
        system_prompt = """You are a healthcare assistant for the IoT Health Monitoring System. 
You provide helpful, accurate, and compassionate health-related information and advice.
Keep responses concise, informative, and easy to understand.
If you don't know something or if it's a medical emergency, advise the user to contact a healthcare professional.
Never provide dangerous advice and clarify you are not a replacement for professional medical consultation."""

        # Prepare the messages for the API
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add patient context if available
        if patient_context:
            messages.append({"role": "system", "content": f"Context: {patient_context}"})
        
        # Add chat history
        for chat in chat_history:
            role = "assistant" if chat.get('is_bot', False) else "user"
            messages.append({"role": role, "content": chat.get('text', '')})
        
        # Add the current user message
        messages.append({"role": "user", "content": message})
        
        # Send request to llm7.io
        response = requests.post(
            "https://api.llm7.io/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer sk-org-llm7-QBqFaZaxZqGlYbXuBfwMcJQTiWUzXYREnLQpXpEDdWGLPg"  # Replace with your actual API key
            },
            json={
                "model": "llm7-7b",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 500
            }
        )
        
        # Check for errors
        if response.status_code != 200:
            return Response({
                'error': f'Error from LLM service: {response.text}',
                'status_code': response.status_code
            }, status=status.HTTP_502_BAD_GATEWAY)
        
        # Extract the response
        llm_response = response.json()
        assistant_message = llm_response.get('choices', [{}])[0].get('message', {}).get('content', '')
        
        # Return the assistant's response
        return Response({
            'response': assistant_message,
            'patient_context_provided': bool(patient_context)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)