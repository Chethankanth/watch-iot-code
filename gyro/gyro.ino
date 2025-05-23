#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

// void setup() {
//   Serial.begin(115200);              // Open Serial Monitor at 115200 baud
//   Wire.begin(33, 34);                // SDA = GPIO 33, SCL = GPIO 34 (IndusCoin board)

//   Serial.println("Initializing MPU6050...");
//   mpu.initialize();                  // Initialize the sensor

//   if (mpu.testConnection()) {
//     Serial.println("MPU6050 connection successful");
//   } else {
//     Serial.println("MPU6050 connection failed");
//     while (1); // Stop execution
//   }
// }
void setup() {
  Serial.begin(115200);
  Serial.println("Serial started");

  Wire.begin(33, 34);  // SDA, SCL
  Serial.println("Wire started");

  Serial.println("Initializing MPU6050...");
  mpu.initialize();

  if (mpu.testConnection()) {
    Serial.println("MPU6050 connection successful");
  } else {
    Serial.println("MPU6050 connection failed");
    while (1);
  }
}

void loop() {
  int16_t gx, gy, gz;

  mpu.getRotation(&gx, &gy, &gz);    // Get gyroscope values

  Serial.print("Gyroscope (X, Y, Z) = ");
  Serial.print(gx); Serial.print(", ");
  Serial.print(gy); Serial.print(", ");
  Serial.println(gz);

  delay(100);  // Adjust delay for speed of updates (100ms = 10 updates/sec)
}