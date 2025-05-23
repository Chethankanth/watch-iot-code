#include <WiFi.h>
#include <WebServer.h>

// Wi-Fi credentials (replace with your hotspot credentials)
const char* ssid = "iQOO Neo7";
const char* password = "Ashok@93";

// Create web server on port 80
WebServer server(80);

// Sensor pin
const int sensorPin = 4;  // Use an analog-capable pin on ESP32-S2

// Heartbeat variables
int sensorValue = 0;
int threshold = 550;
bool pulseDetected = false;
unsigned long lastBeatTime = 0;
int bpm = 0;

void handleRoot() {
  String html = "<!DOCTYPE html><html><head><meta charset='UTF-8'>";
  html += "<meta name='viewport' content='width=device-width, initial-scale=1'>";
  html += "<title>ESP32 Heartbeat Monitor</title></head><body>";
  html += "<h1>Heartbeat Monitor</h1>";
  html += "<p>Current BPM: <strong>" + String(bpm) + "</strong></p>";
  html += "</body></html>";
  server.send(200, "text/html", html);
}

void setup() {
  Serial.begin(115200);
  pinMode(sensorPin, INPUT);

  // Connect to Wi-Fi
  Serial.println("Connecting to Wi-Fi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected to Wi-Fi");
  Serial.print("ESP32 IP address: ");
  Serial.println(WiFi.localIP());

  // Start web server
  server.on("/", handleRoot);
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  // Read analog value from heartbeat sensor
  int value = analogRead(sensorPin);
  unsigned long currentTime = millis();

  // Detect heartbeat pulse
  if (value > threshold && !pulseDetected) {
    pulseDetected = true;
    unsigned long timeBetweenBeats = currentTime - lastBeatTime;

    if (timeBetweenBeats > 300) { // Ignore noise and fast beats
      bpm = 60000 / timeBetweenBeats;
      Serial.print("BPM: ");
      Serial.println(bpm);
      lastBeatTime = currentTime;
    }
  }

  if (value < threshold) {
    pulseDetected = false;
  }

  server.handleClient(); // Serve HTTP requests

  delay(10); // Sampling rate
}