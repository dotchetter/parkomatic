#include <TimeLib.h>
#include <Arduino_MKRGPS.h>

void setup() 
{
	Serial.begin(9600);
	while (!Serial){}

	if (!GPS.begin(GPS_MODE_SHIELD)) 
	{

		Serial.println("Failed to initialize GPS!");
		while (1);
	}
}

void loop()
{
	if (GPS.available()) 
	{
		
		float latitude   = GPS.latitude();
	    float longitude  = GPS.longitude();
	    float altitude   = GPS.altitude();
	    float speed      = GPS.speed();
	    int   satellites = GPS.satellites();
	   
	    unsigned long timestamp = GPS.getTime();
		char buff[10];
	    
		sprintf(buff, "%02d:%02d", hour(timestamp), minute(timestamp));
	   
	    // print GPS values
	    Serial.print("Location: ");
	    Serial.print(latitude, 7);
	    Serial.print(", ");
	    Serial.println(longitude, 7);
	    Serial.print("Altitude: ");
	    Serial.print(altitude);
	    Serial.println("m");
	    Serial.print("Ground speed: ");
	    Serial.print(round(speed));
	    Serial.println(" km/h");
	    Serial.print("Number of satellites: ");
	    Serial.println(satellites);
	    Serial.print("The time: ");
		Serial.print(buff);
	    Serial.println();
    }
}
