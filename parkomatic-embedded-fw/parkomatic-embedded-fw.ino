#include <avr/dtostrf.h>
#include <Arduino_MKRGPS.h>
#include <LiquidCrystal.h>
#include "defines.h" 
#include "AzureIotHubClient_MKRGSM.h"

LiquidCrystal lcd(LCD_RS_PIN, LCD_ENABLE_PIN, LCD_D4_PIN, LCD_D5_PIN, LCD_D6_PIN, LCD_D7_PIN);
IotHubClient iothub(SECRET_BROKER, SECRET_DEVICE_ID);

void setup() 
{
	#if DEVMODE
	    Serial.begin(2000000);
		while (!Serial);
			#if SENDONCE
				Serial.println("[INFO]: SENDONCE flag activated. This alters the behavior of the device.");
			#endif	
		Serial.println("[INFO]: DEVMODE flag activated. This alters the behavior of the device.\n");
		Serial.println("[INFO]: Parkomatic firmware version: 1.0.1");
		Serial.println("[INFO]: Cloud service used: Microsoft Azure");
		Serial.println("[INFO]: Device starting up\n");
	#endif

	GPS.begin(GPS_MODE_SHIELD);
	
	iothub.Begin();
	iothub.SetIncomingMessageCallback(printIncomingMessage);
	
	lcd.begin(LCD_COLUMNS, LCD_ROWS);
	lcd.setCursor(0,0);
	lcd.print("Parkering start:");	
}


void formatJsonString(char* buf, size_t size, float lat, float lon, char* deviceId, uint32_t epoch)
{
	char lon_buf[10];
	char lat_buf[10];

	dtostrf(lon, 7, 7, lon_buf);
	dtostrf(lat, 7, 7, lat_buf);

    snprintf(buf, size, 
			 "{\"lat\": \"%s\", \"lon\": \"%s\", \"deviceId\": \"%s\", \"epochtime\": %ld}" , 
             lat_buf, lon_buf, deviceId, epoch);
}


void printIncomingMessage(int size)
{
	char timestamp_buf[6];
	uint8_t count = 0;
	Serial.print("[DEBUG]: Recieved message: ");
	
	while(iothub.Available())
	{
		timestamp_buf[count] = (char)iothub.ReadIncoming();
		count++;
	}

	timestamp_buf[count] = '\0';

	Serial.println(timestamp_buf);
	lcd.setCursor(5,1);
	lcd.print(timestamp_buf);
}


void loop() 
{
	static uint32_t last_publish;
	char json_buf[JSON_BUFSIZE];
	
	uint32_t gps_search_start;

	gps_search_start = millis();	

	if (TIME_PASSED(PUBLISH_INTERVAL, last_publish))
	{
		#if DEVMODE
			Serial.print("\n[DEBUG]: Attempting GPS lock on... ");
		#endif
		while (!TIME_PASSED(GPS_SEARCH_TIMEOUT, gps_search_start))
		{
			if (GPS.available()) 
			{
				float lon = GPS.longitude();
				float lat = GPS.latitude();
				unsigned long t = GPS.getTime();

				formatJsonString(json_buf, JSON_BUFSIZE, 
								 lat, lon,
								 SECRET_DEVICE_ID, t);
				#if DEVMODE
					Serial.println("success"); 
					Serial.print("[INFO]: Location: ");
					Serial.print(lon, 7);

					Serial.print(", ");
					Serial.println(lat, 7);

					Serial.print("[INFO]: Constructed message: ");
					Serial.println(json_buf);
				#endif
				break;
			}
		}
		last_publish = millis();
		iothub.Publish(json_buf);

		#if SENDONCE
			Serial.println("SENDONCE flag active - stalling indefinitely");
			for(;;);
		#endif
	}
	iothub.Update();
}