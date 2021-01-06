#include <MKRGSM.h>
#include "defines.h" 

const char PINNUMBER[]     = SECRET_PINNUMBER;
const char GPRS_APN[]      = SECRET_GPRS_APN;
const char GPRS_LOGIN[]    = SECRET_GPRS_LOGIN;
const char GPRS_PASSWORD[] = SECRET_GPRS_PASSWORD;

GSMClient client;
GPRS gprs;
GSM gsmAccess;

char server[] = "worldtimeapi.org";
char path[] = "/api/timezone/Europe/Stockholm.txt";
int port = 80; 

void setup() 
{
	Serial.begin(9600);
	while (!Serial) {;}

	Serial.println("Starting Arduino web client.");

	bool connected = false;

	while (!connected) 
	{
		if ((gsmAccess.begin(PINNUMBER) == GSM_READY) &&
		    (gprs.attachGPRS(GPRS_APN, GPRS_LOGIN, GPRS_PASSWORD) == GPRS_READY)) 
		{
		  connected = true;
		} 
		else 
		{
		  Serial.println("Not connected");
		  delay(1000);
		}
	}

	Serial.println(F("Connecting to server... "));

	if (client.connect(server, port)) 
	{
		Serial.print(F(" success."));
	
		client.print("GET ");
		client.print(path);
		client.println(" HTTP/1.1");
		client.print("Host: ");
		client.println(server);
		client.println("Connection: close");
		client.println();
	}
	else 
	{
		Serial.println("connection failed");
	}
}

void loop() 
{
	if (client.available())
	{
		char c = client.read();
		Serial.print(c);
	}

	if (!client.available() && !client.connected()) 
	{
		Serial.println();
		Serial.println("disconnecting.");
		client.stop();
		
		Serial.println("done.");
		while(1){}
	}
}