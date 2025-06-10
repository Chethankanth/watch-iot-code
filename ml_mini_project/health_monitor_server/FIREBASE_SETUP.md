# Firebase Configuration Guide

This guide explains how to set up Firebase for the IoT Health Monitoring System.

## Step 1: Create a Firebase Project

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project"
3. Enter a project name (e.g., "Health Monitoring System")
4. Accept the terms and continue
5. Configure Google Analytics (optional)
6. Click "Create Project"

## Step 2: Add an Android App (for mobile notifications)

1. From the project overview, click "Add app" and select Android
2. Enter your Android package name (e.g., "com.example.healthmonitor")
3. Enter app nickname (optional)
4. Download the `google-services.json` file and keep it for your Android app
5. Follow the setup instructions to integrate Firebase into your Android app

## Step 3: Create a Service Account Key

1. In the Firebase console, go to Project Settings (gear icon)
2. Go to the "Service accounts" tab
3. Click "Generate new private key"
4. Save the JSON file as `firebase-key.json` in the `health_monitor_server` directory

## Step 4: Enable Cloud Messaging

1. In the Firebase console, go to "Cloud Messaging"
2. Enable the API if it's not already enabled

## Step 5: Configure Firebase Admin SDK in Django

1. Make sure the `firebase-key.json` file is in the correct location
2. Verify that the Firebase service is initialized in `firebase_service.py`
3. Test the configuration using the `test_firebase_notification.py` script

## Troubleshooting

### Common Issues:

1. **Initialization Failed**: Check the path to your `firebase-key.json` file.

2. **Permission Denied**: Make sure your service account has the necessary permissions.

3. **Invalid FCM Token**: If testing with a specific device token, make sure it's valid and current.

4. **Missing google-services.json**: For Android app development, make sure this file is in the correct location.

### Testing Firebase Configuration

Run the testing script:

```
python test_firebase_notification.py
```

The script will:
1. Check if the Firebase credentials file exists
2. Attempt to initialize Firebase
3. Allow you to send test notifications

## Firebase Project Structure

The IoT Health Monitoring System uses Firebase for:

1. **Cloud Messaging (FCM)**: Sending push notifications to guardians
2. **Authentication** (optional): User authentication for mobile apps
3. **Realtime Database** (optional): Syncing real-time health data to mobile apps

## Mobile App Integration

For the companion mobile app:

1. Add the `google-services.json` to your Android project
2. Configure FCM in your app following the [Android Firebase Setup](./ANDROID_FIREBASE_SETUP.md) guide
3. Implement notification handling in your mobile app

## Security Considerations

- Keep your `firebase-key.json` file secure and never commit it to public repositories
- Use Firebase Security Rules to protect your data
- Implement proper authentication in your mobile apps