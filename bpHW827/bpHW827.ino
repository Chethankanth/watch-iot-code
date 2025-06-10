const int pulsePin = 36;  // GPIO 36 connected to 'S' pin of HW-827 sensor

int pulseSignal;           // analog reading
int threshold = 550;       // adjust this threshold if needed
bool pulseDetected = false;

unsigned long lastBeatTime = 0;
int bpm = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("HW-827 Heart Rate Monitor Starting...");
}

void loop() {
  pulseSignal = analogRead(pulsePin);
  unsigned long currentTime = millis();

  // Optional: Print raw analog signal for debugging
  Serial.print("Signal: ");
  Serial.println(pulseSignal);

  if (pulseSignal > threshold && !pulseDetected) {
    pulseDetected = true;
    unsigned long timeBetweenBeats = currentTime - lastBeatTime;

    if (timeBetweenBeats > 300) {  // Only count if it's been at least 300ms (BPM < 200)
      bpm = 60000 / timeBetweenBeats;
      Serial.print("BPM: ");
      Serial.println(bpm);
      lastBeatTime = currentTime;
    }
  }

  if (pulseSignal < threshold) {
    pulseDetected = false;
  }

  delay(10);  // Short delay for smoother readings
}