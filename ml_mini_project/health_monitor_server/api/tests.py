from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Patient, Guardian, HealthData, Alert


class PatientModelTest(TestCase):
    """Test the Patient model"""
    
    def setUp(self):
        self.patient = Patient.objects.create(
            name="Test Patient",
            age=65,
            gender="MALE",
            user_id="test123",
            medical_history="Hypertension, Diabetes",
            emergency_contact="123-456-7890"
        )
    
    def test_patient_creation(self):
        """Test creating a patient"""
        self.assertEqual(self.patient.name, "Test Patient")
        self.assertEqual(self.patient.age, 65)
        self.assertEqual(self.patient.gender, "MALE")
        self.assertEqual(self.patient.user_id, "test123")
    
    def test_patient_str_representation(self):
        """Test the string representation"""
        self.assertEqual(str(self.patient), "Test Patient (65)")


class GuardianModelTest(TestCase):
    """Test the Guardian model"""
    
    def setUp(self):
        self.patient = Patient.objects.create(
            name="Test Patient",
            age=65,
            gender="MALE",
            user_id="test123"
        )
        
        self.guardian = Guardian.objects.create(
            patient=self.patient,
            name="Test Guardian",
            relationship="CAREGIVER",
            phone_number="123-456-7890",
            email="guardian@example.com",
            notification_enabled=True
        )
    
    def test_guardian_creation(self):
        """Test creating a guardian"""
        self.assertEqual(self.guardian.name, "Test Guardian")
        self.assertEqual(self.guardian.relationship, "CAREGIVER")
        self.assertEqual(self.guardian.patient, self.patient)
        self.assertTrue(self.guardian.notification_enabled)
    
    def test_guardian_str_representation(self):
        """Test the string representation"""
        self.assertEqual(str(self.guardian), "Test Guardian (CAREGIVER of Test Patient)")


class HealthDataModelTest(TestCase):
    """Test the HealthData model"""
    
    def setUp(self):
        self.patient = Patient.objects.create(
            name="Test Patient",
            age=65,
            gender="MALE",
            user_id="test123"
        )
        
        self.health_data = HealthData.objects.create(
            patient=self.patient,
            heart_rate=72.5,
            spo2=98.0,
            accelerometer_x=0.1,
            accelerometer_y=0.2,
            accelerometer_z=9.8,
            gyroscope_x=0.5,
            gyroscope_y=-0.2,
            gyroscope_z=0.1
        )
    
    def test_health_data_creation(self):
        """Test creating health data"""
        self.assertEqual(self.health_data.patient, self.patient)
        self.assertEqual(self.health_data.heart_rate, 72.5)
        self.assertEqual(self.health_data.spo2, 98.0)
        self.assertEqual(self.health_data.accelerometer_z, 9.8)


class AlertModelTest(TestCase):
    """Test the Alert model"""
    
    def setUp(self):
        self.patient = Patient.objects.create(
            name="Test Patient",
            age=65,
            gender="MALE",
            user_id="test123"
        )
        
        self.health_data = HealthData.objects.create(
            patient=self.patient,
            heart_rate=72.5,
            spo2=98.0,
            accelerometer_x=0.1,
            accelerometer_y=0.2,
            accelerometer_z=9.8,
            gyroscope_x=0.5,
            gyroscope_y=-0.2,
            gyroscope_z=0.1
        )
        
        self.alert = Alert.objects.create(
            patient=self.patient,
            type="FALL",
            message="Fall detected with 75% confidence",
            health_data=self.health_data,
            status="NEW"
        )
    
    def test_alert_creation(self):
        """Test creating an alert"""
        self.assertEqual(self.alert.patient, self.patient)
        self.assertEqual(self.alert.type, "FALL")
        self.assertEqual(self.alert.status, "NEW")
    
    def test_alert_acknowledge(self):
        """Test acknowledging an alert"""
        self.alert.acknowledge()
        self.assertEqual(self.alert.status, "ACKNOWLEDGED")
    
    def test_alert_resolve(self):
        """Test resolving an alert"""
        self.alert.resolve()
        self.assertEqual(self.alert.status, "RESOLVED")
        self.assertIsNotNone(self.alert.resolved_at)


class APITests(APITestCase):
    """Test the API endpoints"""
    
    def setUp(self):
        self.patient = Patient.objects.create(
            name="API Test Patient",
            age=70,
            gender="FEMALE",
            user_id="apitest123"
        )
        
        self.guardian = Guardian.objects.create(
            patient=self.patient,
            name="API Test Guardian",
            relationship="CHILD",
            phone_number="987-654-3210",
            email="apiguardian@example.com",
            notification_enabled=True
        )
    
    def test_get_patients(self):
        """Test getting the list of patients"""
        url = reverse('patient-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0)
    
    def test_get_patient_detail(self):
        """Test getting a specific patient"""
        url = reverse('patient-detail', kwargs={'pk': self.patient.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "API Test Patient")
    
    def test_get_patient_guardians(self):
        """Test getting a patient's guardians"""
        url = reverse('patient-guardians', kwargs={'pk': self.patient.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "API Test Guardian")
    
    def test_health_data_endpoint(self):
        """Test sending health data"""
        url = '/api/health-data/'  # Direct URL since reverse might not work for this
        data = {
            'user_id': self.patient.user_id,
            'heart_rate': 75.0,
            'spo2': 97.0,
            'accelerometer_x': 0.1,
            'accelerometer_y': 0.2,
            'accelerometer_z': 9.8,
            'gyroscope_x': 0.5,
            'gyroscope_y': -0.2,
            'gyroscope_z': 0.1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify data was saved
        self.assertTrue(HealthData.objects.filter(patient=self.patient).exists())