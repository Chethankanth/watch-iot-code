# Firebase Database Setup Guide

This guide explains how to set up Firebase Firestore Database for the IoT Health Monitoring System.

## Step 1: Create a Firebase Project

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project"
3. Enter a project name (e.g., "Health Monitoring System")
4. Accept the terms and continue
5. Configure Google Analytics (optional)
6. Click "Create Project"

## Step 2: Set Up Firestore Database

1. In the Firebase console, go to "Firestore Database" in the left navigation
2. Click "Create database"
3. Choose "Start in production mode" (recommended) or "Start in test mode" (easier for development)
4. Select a location closest to your users
5. Click "Enable"

## Step 3: Set Up Database Rules

In the Firestore Database section, go to the "Rules" tab and set up appropriate security rules:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Patients collection
    match /patients/{patientId} {
      allow read, write: if request.auth != null;
    }
    
    // Guardians collection
    match /guardians/{guardianId} {
      allow read, write: if request.auth != null;
    }
    
    // Health data collection
    match /health_data/{dataId} {
      allow read, write: if request.auth != null;
    }
    
    // Alerts collection
    match /alerts/{alertId} {
      allow read, write: if request.auth != null;
    }
  }
}
```

Click "Publish" to save your rules.

## Step 4: Create a Service Account Key

1. In the Firebase console, go to Project Settings (gear icon)
2. Go to the "Service accounts" tab
3. Click "Generate new private key"
4. Save the JSON file as `firebase-key.json` in the `health_monitor_server` directory

## Step 5: Update Dependencies

Make sure your `requirements.txt` includes:

```
firebase-admin==6.2.0
```

Run `pip install -r requirements.txt` to install it.

## Step 6: Database Structure

The system is configured to use the following Firestore collections:

- **patients** - Contains patient information
- **guardians** - Contains guardian information with references to patients
- **health_data** - Contains health measurements with references to patients
- **alerts** - Contains alerts with references to patients and health data

## Using Firebase Database

With this setup, the application will:

1. Store all data in both SQLite (for compatibility) and Firebase Firestore
2. Send notifications using Firebase Cloud Messaging
3. Allow for easy mobile app integration via Firebase

### Verifying Firebase Integration

You can verify that data is being saved to Firebase by:

1. Running the server: `python manage.py runserver`
2. Sending some test data using `python send_anomalous_data.py`
3. Checking the Firestore Database in the Firebase console - you should see collections with your data

## Troubleshooting

### Common Issues:

1. **Initialization Failed**: Check the path to your `firebase-key.json` file.

2. **Permission Denied**: Make sure your service account has the necessary permissions.

3. **Missing Collections**: If collections aren't showing up, check the console logs for any errors during save operations.

4. **Rules Preventing Access**: If you're having access issues, try setting the database to test mode temporarily.

## Firebase Data Sync Strategy

The application implements a "dual-write" strategy:

1. Data is written to both SQLite and Firebase Firestore
2. This ensures compatibility with the existing application code
3. Firebase is used for notifications and mobile app integration
4. In the future, you could remove the SQLite dependency entirely

## Security Considerations

- Keep your `firebase-key.json` file secure and never commit it to public repositories
- Use Firebase Authentication for user login (this is not currently implemented)
- Set up proper Firebase Security Rules to protect your data