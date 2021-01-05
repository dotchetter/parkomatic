void setup() {
  // put your setup code here, to run once:
#include <MPU6050_tockn.h>

}

void loop() {
  // put your main code here, to run repeatedly:

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