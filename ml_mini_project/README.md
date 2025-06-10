# IoT Health Monitoring System

An intelligent health monitoring system that uses IoT devices to collect health data, analyzes it using machine learning, and sends alerts when anomalies are detected.

## Features

- **Health Data Collection**: Collects heart rate, blood oxygen (SpO2), and movement data from IoT devices
- **Machine Learning Analysis**: Analyzes data to detect falls and abnormal vital signs
- **Real-time Alerts**: Sends immediate notifications to caregivers when problems are detected
- **API Backend**: Django REST API for data processing and storage
- **Firebase Integration**: Push notifications to mobile devices
- **Health Assistant Chat**: AI-powered chat system for health-related questions

## Project Structure

```
ml_mini_project/
├── health_monitor_server/     # Django server
│   ├── api/                   # REST API application
│   │   ├── migrations/        # Database migrations
│   │   ├── __init__.py        
│   │   ├── admin.py           # Admin interface configuration
│   │   ├── apps.py            # App configuration
│   │   ├── firebase_service.py # Firebase integration
│   │   ├── ml_predictor.py    # ML models for predictions
│   │   ├── models.py          # Database models
│   │   ├── serializers.py     # API serializers
│   │   ├── tests.py           # Unit tests
│   │   ├── urls.py            # API URL routing
│   │   └── views.py           # API views and logic
│   ├── health_monitor/        # Project settings
│   │   ├── __init__.py
│   │   ├── asgi.py            # ASGI configuration
│   │   ├── settings.py        # Django settings
│   │   ├── urls.py            # URL configuration
│   │   └── wsgi.py            # WSGI configuration
│   ├── firebase-key.json      # Firebase credentials
│   ├── manage.py              # Django management script
│   └── test_menu.bat          # Test menu for Windows
├── send_anomalous_data.py     # Script to test anomalous data
├── test_firebase_notification.py # Script to test Firebase
└── requirements.txt           # Python dependencies
```

## Setup and Installation

1. Clone the repository
   ```
   git clone <repository-url>
   cd ml_mini_project
   ```

2. Install dependencies
   ```
   pip install -r requirements.txt
   ```

3. Configure Firebase
   - Create a Firebase project at https://console.firebase.google.com/
   - Set up Firestore Database (see FIREBASE_DATABASE_SETUP.md for detailed instructions)
   - Generate a service account key and save as `health_monitor_server/firebase-key.json`

4. Initialize the database
   ```
   cd health_monitor_server
   python manage.py makemigrations api
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. Run the server
   ```
   python manage.py runserver
   ```

## Usage

### Running the Django Server

```
cd health_monitor_server
python manage.py runserver
```

Access the admin interface at http://127.0.0.1:8000/admin/

### Testing Firebase Notifications

```
python test_firebase_notification.py
```

### Sending Test Health Data

```
python send_anomalous_data.py
```

### Using the Test Menu (Windows)

```
cd health_monitor_server
test_menu.bat
```

## API Endpoints

- `GET /api/patients/` - List all patients
- `POST /api/patients/` - Register a new patient
- `GET /api/patients/{id}/` - Get patient details
- `GET /api/patients/{id}/guardians/` - Get patient's guardians
- `GET /api/patients/{id}/alerts/` - Get patient's alerts
- `POST /api/health-data/` - Send health data from IoT devices
- `GET /api/guardians/` - List all guardians
- `POST /api/guardians/` - Add a guardian
- `GET /api/alerts/` - List all alerts
- `POST /api/alerts/{id}/acknowledge/` - Acknowledge an alert
- `POST /api/alerts/{id}/resolve/` - Resolve an alert
- `POST /api/chat/` - Chat with health assistant

## Health Assistant Chat

The system includes an AI-powered health assistant that can answer health-related questions. The chat endpoint uses llm7.io to provide intelligent, context-aware responses.

Example request:
```json
{
  "message": "What should I do if my heart rate is elevated?",
  "patient_id": 1,
  "chat_history": [
    {"text": "Hello, I'm not feeling well today", "is_bot": false},
    {"text": "I'm sorry to hear that. Can you tell me more about your symptoms?", "is_bot": true}
  ]
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.