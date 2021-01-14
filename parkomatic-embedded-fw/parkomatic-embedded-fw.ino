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
			#if RUNONCE
				Serial.println("[INFO]: RUNONCE flag activated. This alters the behavior of the device.");
			#endif	
		Serial.println("[INFO]: DEVMODE flag activated. This alters the behavior of the device.\n");
		Serial.println("[INFO]: Parkomatic firmware version: 1.0.1");
		Serial.println("[INFO]: Cloud service used: Microsoft Azure");
		Serial.println("[INFO]: Device starting up\n");
	#endif

	//lcd.begin(LCD_COLUMNS, LCD_ROWS);
	lcd.setCursor(0,0);
	lcd.print("Parkering start:");
	
	GPS.begin(GPS_MODE_SHIELD);

	iothub.Begin();
	iothub.SetIncomingMessageCallback(printIncomingMessage);
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


void printIncomingMessage(int size)
{
	Serial.print("[DEBUG]: Recieved message: ");
	
	while(iothub.Available())
	{
		Serial.print((char)iothub.ReadIncoming());
	}
	Serial.println();
}


void loop() 
{
	static uint32_t last_publish;
	static uint8_t message_sent = 0;
	char json_buf[JSON_BUFSIZE];

	iothub.Update();

	#if SENDONCE
		if (!message_sent)
		{
			iothub.Publish("Hello from device");
			message_sent = 1;		
		}
	#endif

	#if RUNONCE
		Serial.println("\n[INFO]: === Runtime completed. Restart the device if you want another go. === ");
		while(1){};
	#endif

	if (GPS.available() && (millis() - last_publish) > PUBLISH_INTERVAL)
	{
		formatJsonString(json_buf,
						 JSON_BUFSIZE,
						 GPS.latitude(),
						 GPS.longitude(),
						 SECRET_DEVICE_ID,
						 GPS.getTime());

		last_publish = millis();
	}
	else
	{
		Serial.println("GPS not available.");
	}
}