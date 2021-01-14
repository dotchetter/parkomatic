
#include <avr/dtostrf.h>
#include "LiquidCrystal.h"
#include "defines.h"
#include <Arduino_MKRGPS.h>

LiquidCrystal lcd(LCD_RS_PIN, LCD_ENABLE_PIN, LCD_D4_PIN, LCD_D5_PIN, LCD_D6_PIN, LCD_D7_PIN);

char json_buf[JSON_BUFSIZE];

void setup() 
{
	Serial.begin(9600);
	lcd.begin(LCD_COLUMNS, LCD_ROWS);
	lcd.setCursor(0,0);
	lcd.print("Parkering start:");

	while (!Serial){}

	Serial.println("Starting GPS");
	if (!GPS.begin(GPS_MODE_SHIELD)) 
	{
		Serial.println("Failed to initialize GPS!");
		while (1);
	}

	Serial.println("GPS started successfully");
}


void formatJsonString(char* buf, size_t size, float lat, float lon, char* deviceId, uint32_t epoch)
{
	char lon_buf[10];
	char lat_buf[10];

	dtostrf(lon, 7, 7, lon_buf);
	dtostrf(lat, 7, 7, lat_buf);

    snprintf(buf, 
			 size, 
			 "{\"lat\": \"%s\", \"lon\": \"%s\", \"deviceId\": \"%s\", \"epochtime\": %ld}" , 
             lat_buf, lon_buf, deviceId, epoch);
}


void loop()
{

	if (GPS.available()) 
	{

/*		float latitude   = ;
	    float longitude  = GPS.longitude();
	    float altitude   = GPS.altitude();
	    float speed      = GPS.speed();
	    int   satellites = GPS.satellites();
	   
	    unsigned long timestamp = GPS.getTime();

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
*/

	    formatJsonString(json_buf,
	    				 JSON_BUFSIZE,
	    				 GPS.latitude(),
	    				 GPS.longitude(),
	    				 "device-id-mock",
	    				 GPS.getTime());

	   	Serial.println(json_buf); // Send to iohhub.Publish();
    }
}