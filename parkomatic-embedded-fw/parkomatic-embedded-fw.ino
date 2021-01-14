#include "LiquidCrystal.h"
#include "defines.h"
#include <Arduino_MKRGPS.h>

LiquidCrystal lcd(LCD_RS_PIN, LCD_ENABLE_PIN, LCD_D4_PIN, LCD_D5_PIN, LCD_D6_PIN, LCD_D7_PIN);

void setup() 
{
	Serial.begin(9600);
	lcd.begin(LCD_COLUMNS, LCD_ROWS);
	lcd.setCursor(0,0);
	lcd.print("Parkering start:");

	while (!Serial){}

	if (!GPS.begin(GPS_MODE_SHIELD)) 
	{
		Serial.println("Failed to initialize GPS!");
		while (1);
	}
}


void formatJsonString(char* buf, size_t size, float lat, float lon, char* deviceId, uint32_t epoch)
{
    /*
    const char* lat = "59.2282868";
    const char* lon = "18.4985734";
    const char* deviceId = "9c758a41-mock-4711-mock-b2113f561f1d";
    const unsigned long epoch = 1610626385;
    */
    snprintf(buf, 
			 size, 
			 "{\"lat\": \"%.8f\", \"lon\": \"%.8f\", \"deviceId\": \"%s\", \"epochtime\": %ld}" , 
             lat, lon, deviceId, epoch);
}


void loop()
{
	char json_buf[JSON_BUFSIZE];

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