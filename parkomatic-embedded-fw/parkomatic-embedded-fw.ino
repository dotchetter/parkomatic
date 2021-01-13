
#include "defines.h" 
#include "AzureIotHubClient_MKRGSM.h"

char mqtt_username[100];

IotHubClient* iothub = new IotHubClient(SECRET_BROKER, SECRET_DEVICE_ID);

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
	
	iothub->Begin();
	iothub->SetIncomingMessageCallback(printIncomingMessage);
}


void printIncomingMessage(int size)
{
	Serial.print("Recieved message: ");
	
	while(iothub->Available())
	{
		Serial.print((char)iothub->ReadIncoming());
	}
}


void loop() 
{
	static uint32_t last_publish;
	static uint8_t message_sent = 0;

	iothub->Update();

	#if SENDONCE
		if (!message_sent)
		{
			iothub->Publish("Hello from device");
			message_sent = 1;		
		}
	#else
		if (millis() - last_publish > PUBLISH_INTERVAL)
		{
			iothub->Publish("Hello from device");
		}
	#endif

	#if RUNONCE
		Serial.println("\n[INFO]: === Runtime completed. Restart the device if you want another go. === ");
		delete iothub;
		while(1){};
	#endif
}