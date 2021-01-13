#include "LiquidCrystal.h"
#include "defines.h"

#include <TimeLib.h>
#include <Arduino_MKRGPS.h>

LiquidCrystal lcd(LCD_RS_PIN, LCD_ENABLE_PIN, LCD_D4_PIN, LCD_D5_PIN, LCD_D6_PIN, LCD_D7_PIN);


void setup() 
{
	Serial.begin(9600);

	lcd.setCursor(0,0);
	lcd.print("Parkering start:");
	lcd.begin(LCD_COLUMNS, LCD_ROWS);

	while (!Serial){}

	if (!GPS.begin(GPS_MODE_SHIELD)) 
	{
		Serial.println("Failed to initialize GPS!");
		while (1);
	}
}


void displayTime()
{
	lcd.setCursor(3,1);
	lcd.print();
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

	    displayTime();
    }
}