#include <MPU6050_tockn.h>
#include <Wire.h>
#include "defines.h"


/*
Parkomatic main firmware file

This file contains firmware testing for 
Accelerometer driver software. 

Physical connections for MPU6050:

Vcc  --> 5v
Gnd  --> Gnd
SCL  --> SCL
SDA  --> SDA
XDA  --> A4
XCL  --> A5
*/

MPU6050 accelerometer(Wire);

void setup() 
{
	Serial.begin(38400);
	Wire.begin();
	accelerometer.begin();
	accelerometer.calcGyroOffsets(true);
}


void loop() 
{
	static uint32_t last_iter;

	accelerometer.update();

	if (millis() - last_iter > INTERVAL)
	{
		Serial.print("Temperature: ");
		Serial.println(accelerometer.getTemp());

		Serial.print("Acceleration: ");
		Serial.print("X axis: ");
		Serial.println(accelerometer.getAccX());
		
		Serial.print("Y axis: ");
		Serial.println(accelerometer.getAccY());

		Serial.print("Z axis: ");
		Serial.println(accelerometer.getAccZ());

		last_iter = millis();
	}
}