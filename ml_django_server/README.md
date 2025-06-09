# IoT Health Monitoring System

## Overview

This system uses IoT devices to monitor patients' health data (heart rate, SpO2, movement) and alerts guardians in case of emergencies such as falls or abnormal vital signs.

## Key Features

- **Real-time Monitoring**: Track health vitals and movement data in real-time
- **ML-Powered Analysis**: Automatic detection of falls and health anomalies
- **Instant Alerts**: Notify guardians immediately when emergencies are detected
- **Mobile Integration**: Full API support for mobile app development
- **Firebase Notifications**: Push notifications to caregiver mobile devices

## System Components

1. **Django Backend Server**: Processes and analyzes health data
2. **ML Models**: Detect falls and analyze vital signs
3. **Firebase Integration**: Send notifications to guardian mobile devices
4. **Mobile App**: View health data and receive alerts (implemented separately)
5. **IoT Devices**: Collect health data from patients (implemented separately)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Django 5.2 or higher
- Firebase account
- IoT devices with sensors (heart rate, SpO2, accelerometer, gyroscope)

### Running the Server

For quick start, use the provided batch file:

```
run_server.bat
```

Or run the following commands:

```bash
cd health_monitor_server
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### Testing

Run the test script to verify system functionality:

```
test_all.bat
```

This will guide you through testing various aspects of the system.

## Documentation

- **USER_MANUAL.md**: Comprehensive guide for system users
- **FIREBASE_SETUP.md**: Details on Firebase configuration
- **ANDROID_FIREBASE_SETUP.md**: Guide for setting up Firebase in Android apps

## Architecture

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│  IoT Devices  │────▶│ Django Server │────▶│ Firebase FCM  │
└───────────────┘     └───────────────┘     └───────────────┘
                             │                      │
                             ▼                      ▼
                      ┌───────────────┐     ┌───────────────┐
                      │   Database    │     │  Mobile Apps  │
                      └───────────────┘     └───────────────┘
```

## API Endpoints

### Patient Management
- `POST /api/patients/`: Register a new patient
- `GET /api/patients/{id}/`: Get patient details
- `GET /api/patients/{id}/alerts/`: Get patient alerts

### Guardian Management
- `POST /api/guardians/`: Add a guardian for a patient
- `GET /api/guardians/{id}/`: Get guardian details

### Health Data
- `POST /api/health-data/`: Send health data from IoT devices

### Alerts
- `GET /api/alerts/`: Get all alerts
- `POST /api/alerts/{id}/acknowledge/`: Acknowledge an alert
- `POST /api/alerts/{id}/resolve/`: Resolve an alert

## Security Considerations

- Always use HTTPS in production
- Keep Firebase credentials secure
- Follow healthcare data privacy regulations
- Implement proper authentication for all API endpoints

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For more information, contact your system administrator.