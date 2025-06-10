# Health Monitoring IoT System

This repository contains code for an IoT-based health monitoring system that collects health data from wearable devices, processes it using machine learning algorithms, and provides alerts for abnormal health conditions.

## Repository Structure

The repository is organized into several modules:

- **ml_mini_project**: Main Django server with ML integration
- **bpHW827**: Blood pressure monitoring module
- **gyro**: Motion and orientation sensing module
- **latetest_heart_rate_spo2**: Heart rate and SpO2 monitoring module
- **wifi_with_heartrate**: WiFi-connected heart rate monitoring module

## Key Features

- Real-time monitoring of vital health parameters (heart rate, SpO2, blood pressure)
- Fall detection using gyroscope data
- Machine learning algorithms for anomaly detection
- Firebase integration for push notifications
- Django REST API backend for data processing and storage
- Web interface for monitoring and configuration

## Technologies Used

- **Backend**: Django REST Framework
- **Database**: SQLite (development), PostgreSQL (production)
- **Machine Learning**: scikit-learn, NumPy
- **IoT Communication**: WiFi, Bluetooth
- **Notifications**: Firebase Cloud Messaging
- **Frontend**: HTML, CSS, JavaScript

## Getting Started

1. Clone this repository
   ```
   git clone <repository-url>
   cd ml_django_server
   ```

2. Set up the Django server (main application)
   ```
   cd ml_mini_project
   pip install -r requirements.txt
   ```

3. For detailed setup instructions for each module, refer to the README.md in the respective module directories.

## Development

See the ml_mini_project directory for the main server application with complete instructions for setup, configuration, and API endpoints.

## License

This project is licensed under the MIT License.