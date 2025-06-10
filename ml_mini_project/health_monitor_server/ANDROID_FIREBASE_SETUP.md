# Android Firebase Setup Guide

This guide explains how to set up Firebase in an Android app for receiving health monitoring notifications.

## Prerequisites

- Android Studio installed
- Firebase project created (see [FIREBASE_SETUP.md](./FIREBASE_SETUP.md))
- `google-services.json` file downloaded from Firebase console

## Step 1: Create or Open Your Android Project

1. Open Android Studio
2. Create a new project or open your existing Health Monitor app

## Step 2: Add Firebase to Your Android Project

1. Copy the `google-services.json` file to your app's module directory (usually `/app`)

2. Add the Google services plugin to your project-level `build.gradle` file:

```gradle
buildscript {
    repositories {
        google()
        // other repositories
    }
    dependencies {
        classpath 'com.google.gms:google-services:4.3.15'
        // other dependencies
    }
}

allprojects {
    repositories {
        google()
        // other repositories
    }
}
```

3. Apply the Google services plugin in your app-level `build.gradle` file:

```gradle
plugins {
    id 'com.android.application'
    id 'com.google.gms.google-services'
}

dependencies {
    // Add the Firebase BOM
    implementation platform('com.google.firebase:firebase-bom:32.3.1')
    
    // Firebase Cloud Messaging
    implementation 'com.google.firebase:firebase-messaging'
    
    // Other Firebase products as needed
    implementation 'com.google.firebase:firebase-analytics'
    
    // Other dependencies
}
```

4. Sync your project with Gradle

## Step 3: Set Up Firebase Cloud Messaging (FCM)

1. Create a service class that extends `FirebaseMessagingService`:

```java
package com.example.healthmonitor;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.media.RingtoneManager;
import android.net.Uri;
import android.os.Build;
import androidx.core.app.NotificationCompat;
import android.util.Log;

import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;

public class MyFirebaseMessagingService extends FirebaseMessagingService {

    private static final String TAG = "MyFirebaseMsgService";

    @Override
    public void onMessageReceived(RemoteMessage remoteMessage) {
        // Handle FCM message here
        
        // Check if message contains a notification payload
        if (remoteMessage.getNotification() != null) {
            String title = remoteMessage.getNotification().getTitle();
            String body = remoteMessage.getNotification().getBody();
            sendNotification(title, body);
        }

        // Check if message contains data payload
        if (remoteMessage.getData().size() > 0) {
            // Handle data payload
            String alertType = remoteMessage.getData().get("alert_type");
            String patientId = remoteMessage.getData().get("patient_id");
            
            // Process data as needed
        }
    }

    @Override
    public void onNewToken(String token) {
        // Send the new token to your server
        sendRegistrationToServer(token);
    }

    private void sendRegistrationToServer(String token) {
        // TODO: Send token to your server
        // This is where you would send the token to the Django backend
    }

    private void sendNotification(String title, String messageBody) {
        Intent intent = new Intent(this, MainActivity.class);
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        PendingIntent pendingIntent = PendingIntent.getActivity(this, 0, intent,
                PendingIntent.FLAG_IMMUTABLE);

        String channelId = "health_monitor_channel";
        Uri defaultSoundUri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);
        NotificationCompat.Builder notificationBuilder =
                new NotificationCompat.Builder(this, channelId)
                        .setSmallIcon(R.drawable.ic_notification)
                        .setContentTitle(title)
                        .setContentText(messageBody)
                        .setAutoCancel(true)
                        .setSound(defaultSoundUri)
                        .setContentIntent(pendingIntent);

        NotificationManager notificationManager =
                (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);

        // Since android Oreo notification channel is needed
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(channelId,
                    "Health Monitor Notifications",
                    NotificationManager.IMPORTANCE_HIGH);
            notificationManager.createNotificationChannel(channel);
        }

        notificationManager.notify(0, notificationBuilder.build());
    }
}
```

2. Register the service in your `AndroidManifest.xml`:

```xml
<manifest ...>
    <application ...>
        <!-- Other application components -->
        
        <service
            android:name=".MyFirebaseMessagingService"
            android:exported="false">
            <intent-filter>
                <action android:name="com.google.firebase.MESSAGING_EVENT" />
            </intent-filter>
        </service>
        
        <!-- Set custom default icon -->
        <meta-data
            android:name="com.google.firebase.messaging.default_notification_icon"
            android:resource="@drawable/ic_notification" />
        <!-- Set color used with incoming notification messages -->
        <meta-data
            android:name="com.google.firebase.messaging.default_notification_color"
            android:resource="@color/colorAccent" />
        <!-- Set the notification channel for Android O and above -->
        <meta-data
            android:name="com.google.firebase.messaging.default_notification_channel_id"
            android:value="health_monitor_channel" />
    </application>
</manifest>
```

## Step 4: Get and Send FCM Token to Server

Add code to retrieve and send the FCM token to your Django server:

```java
private void getAndSendToken() {
    FirebaseMessaging.getInstance().getToken()
        .addOnCompleteListener(new OnCompleteListener<String>() {
            @Override
            public void onComplete(@NonNull Task<String> task) {
                if (!task.isSuccessful()) {
                    Log.w(TAG, "Fetching FCM registration token failed", task.getException());
                    return;
                }

                // Get new FCM registration token
                String token = task.getResult();

                // Send token to server
                sendTokenToServer(token);
            }
        });
}

private void sendTokenToServer(String token) {
    // Create JSON with token and guardian ID
    JSONObject jsonBody = new JSONObject();
    try {
        jsonBody.put("guardian_id", guardianId);
        jsonBody.put("fcm_token", token);
    } catch (JSONException e) {
        e.printStackTrace();
    }

    // Send to your Django server
    // Use Retrofit, Volley, or any HTTP client library
    
    // Example with Retrofit:
    apiService.updateFcmToken(jsonBody)
        .enqueue(new Callback<ResponseBody>() {
            @Override
            public void onResponse(Call<ResponseBody> call, Response<ResponseBody> response) {
                Log.d(TAG, "Token sent to server successfully");
            }

            @Override
            public void onFailure(Call<ResponseBody> call, Throwable t) {
                Log.e(TAG, "Failed to send token to server", t);
            }
        });
}
```

Call `getAndSendToken()` when the user logs in or when the app starts.

## Step 5: Test Notifications

1. Build and run your app on a physical device or emulator
2. Use the `test_firebase_notification.py` script from the Django project to send a test notification
3. Verify that the notification appears on your device

## Troubleshooting

### Common Issues:

1. **Token not generated**: Check Firebase initialization and internet connection
2. **Notifications not received**: 
   - Verify the token is correctly sent to your server
   - Check that your device has internet connectivity
   - Ensure your app is added to Firebase project correctly
3. **App crashes when receiving notification**: Check your implementation of FirebaseMessagingService

### Testing Firebase Integration

You can test the Firebase integration in your app using the Firebase Console:

1. Go to the Firebase Console > Your Project > Cloud Messaging
2. Click "Send your first message"
3. Create a new notification with a title and message
4. Select your Android app as the target
5. Send the message

If your app is properly configured, you should receive the notification.

## Additional Resources

- [Firebase Cloud Messaging Documentation](https://firebase.google.com/docs/cloud-messaging)
- [Send FCM messages from a server](https://firebase.google.com/docs/cloud-messaging/server)
- [Receive FCM messages in an Android app](https://firebase.google.com/docs/cloud-messaging/android/receive)