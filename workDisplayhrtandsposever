#include <Wire.h>
#include <U8g2lib.h>
#include "MAX30105.h"
#include "spo2_algorithm.h"
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

// OLED setup - SH1106 128x64 with hardware I2C (on GPIO 8 SDA, 9 SCL)
U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

// MAX30105 setup
MAX30105 particleSensor;

// SpO2 variables
uint32_t irBuffer[100];   // Infrared LED sensor data
uint32_t redBuffer[100];  // Red LED sensor data
int32_t spo2;
int8_t validSPO2;
int32_t heartRate;
int8_t validHeartRate;

// MPU6050 setup
Adafruit_MPU6050 mpu;

void setup() {
  Serial.begin(115200);
  while (!Serial)
    delay(10);

  Serial.println("Smartwatch Starting...");

  // Initialize I2C with SDA = GPIO 8, SCL = GPIO 9
  Wire.begin(8, 9);

  // OLED init
  u8g2.begin();
  u8g2.clearBuffer();
  u8g2.setFont(u8g2_font_ncenB08_tr);
  u8g2.drawStr(0, 15, "Smartwatch Booting...");
  u8g2.sendBuffer();
  delay(1000);

  // MAX30105 init
  if (!particleSensor.begin(Wire, I2C_SPEED_STANDARD)) {
    Serial.println("MAX30105 not found. Check wiring.");
    while (1)
      delay(10);
  }
  particleSensor.setup();
  particleSensor.setPulseAmplitudeRed(0x0A);   // Low power Red LED
  particleSensor.setPulseAmplitudeGreen(0);   // Green LED off

  // MPU6050 init
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1)
      delay(10);
  }
  Serial.println("MPU6050 Found!");

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  Serial.println("Sensors Initialized.");
}

void loop() {
  // --- Read MAX30105 values ---
  for (byte i = 0; i < 100; i++) {
    while (!particleSensor.available()) particleSensor.check();
    redBuffer[i] = particleSensor.getRed();
    irBuffer[i] = particleSensor.getIR();
    particleSensor.nextSample();
  }

  // --- Calculate SpO2 and Heart Rate ---
  maxim_heart_rate_and_oxygen_saturation(irBuffer, 100, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);

  // --- Read MPU6050 data ---
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // --- Serial Output ---
  Serial.println("=== Sensor Data ===");
  Serial.print("Heart Rate: "); Serial.print(heartRate); Serial.println(" BPM");
  Serial.print("SpO2: "); Serial.print(spo2); Serial.println(" %");
  Serial.print("Temperature (MPU6050): "); Serial.print(temp.temperature); Serial.println(" °C");

  Serial.print("Accel (m/s^2) X: "); Serial.print(a.acceleration.x);
  Serial.print(" Y: "); Serial.print(a.acceleration.y);
  Serial.print(" Z: "); Serial.println(a.acceleration.z);

  Serial.print("Gyro (rad/s) X: "); Serial.print(g.gyro.x);
  Serial.print(" Y: "); Serial.print(g.gyro.y);
  Serial.print(" Z: "); Serial.println(g.gyro.z);
  Serial.println("===================");

  // --- OLED Display ---
  u8g2.clearBuffer();

  u8g2.setFont(u8g2_font_6x12_tr);
  u8g2.setCursor(0, 12);
  u8g2.print("HR: "); u8g2.print(heartRate); u8g2.print(" bpm");

  u8g2.setCursor(0, 26);
  u8g2.print("SpO2: "); u8g2.print(spo2); u8g2.print(" %");

  u8g2.setCursor(0, 40);
  u8g2.print("Temp: "); u8g2.print(temp.temperature, 1); u8g2.print(" C");

  u8g2.setCursor(0, 54);
  u8g2.print("Accel X: "); u8g2.print(a.acceleration.x, 2);
  u8g2.print(" Y: "); u8g2.print(a.acceleration.y, 2);

  u8g2.setCursor(0, 64);
  u8g2.print("Accel Z: "); u8g2.print(a.acceleration.z, 2);

  u8g2.sendBuffer();

  delay(1000); // Wait 1 sec before next reading
}
