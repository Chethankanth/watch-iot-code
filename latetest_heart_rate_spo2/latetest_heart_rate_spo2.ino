#include <Wire.h>
#include "MAX30105.h"
#include "spo2_algorithm.h"

MAX30105 particleSensor;

#define BUFFER_SIZE 50
uint32_t irBuffer[BUFFER_SIZE];
uint32_t redBuffer[BUFFER_SIZE];

int32_t spo2;
int8_t validSPO2;
int32_t heartRate;
int8_t validHeartRate;

void setup() {
  Serial.begin(115200);
  delay(1000);
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("MAX30105 not found.");
    while (1);
  }

  // Enable Red + IR mode
  particleSensor.setup(0x1F, 8, 2, 100, 411, 4096);
}

void loop() {
  // Fill buffer
  for (int i = 0; i < BUFFER_SIZE; i++) {
    while (!particleSensor.available()) particleSensor.check();
    redBuffer[i] = particleSensor.getRed();
    irBuffer[i] = particleSensor.getIR();
    particleSensor.nextSample();
  }

  // Calculate SpO2 and Heart Rate
  maxim_heart_rate_and_oxygen_saturation(irBuffer, BUFFER_SIZE, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);

  Serial.print("Heart Rate: ");
  Serial.print(heartRate);
  Serial.print(" bpm | Valid: ");
  Serial.println(validHeartRate);

  Serial.print("SpO2: ");
  Serial.print(spo2);
  Serial.print(" % | Valid: ");
  Serial.println(validSPO2);

  delay(5);  // optional delay
}
