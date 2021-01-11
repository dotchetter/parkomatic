#include <MKRGSM.h>
#include <ArduinoMqttClient.h>
#include <ArduinoBearSSL.h>
#include <ArduinoECCX08.h>
#include <utility/ECCX08SelfSignedCert.h>
#include "defines.h" 

/* GSM connectivity singletons */
GPRS gprs;
GSM gsmAccess;

GSMClient gsmClient;
BearSSLClient sslClient(gsmClient);
MqttClient mqttClient(sslClient);

char mqtt_username[100];
String deviceId = SECRET_DEVICE_ID;

void setup() 
{
	#ifdef DEVMODE
    Serial.begin(2000000);
	while (!Serial);				// blocking
	Serial.println("DEVMODE flag activated. This alters the behavior of the device.\n\n");
	Serial.println("[INFO]: Parkomatic firmware version: 1.0.1");
	Serial.println("[INFO]: Cloud service used: Microsoft Azure");
	Serial.println("[INFO]: Device starting up\n");
	#endif
	
	ECCX08SelfSignedCert.beginReconstruction(0, 8);
	ECCX08SelfSignedCert.setCommonName(ECCX08.serialNumber());
	ECCX08SelfSignedCert.endReconstruction();

    /* Set a callback to get the current time
       used to validate the servers certificate */
    ArduinoBearSSL.onGetTime(getGsmTime);

    /* Set the public key to be used with the certificate 
       in the ECCX08 slot */
    sslClient.setEccSlot(0,
                        ECCX08SelfSignedCert.bytes(),
                        ECCX08SelfSignedCert.length());

    /* Use the deiceId define as the MQTT client id */
    mqttClient.setId(deviceId);

    /* Format strings used in communications */
    sprintf(mqtt_username, 
            "%s/%s/api-version=2018-06-30", 
            SECRET_BROKER, 
            SECRET_DEVICE_ID);

    mqttClient.setUsernamePassword(mqtt_username, "");

    /* Bind the callback for which method to execute upon 
       recieved mqtt message */
    mqttClient.onMessage(mqtt_recieve);
}


void connect_to_gsm()
{
	Serial.print("[DEBUG]: Connecting to GSM... ");

    while ((gsmAccess.begin(SECRET_PINNUMBER) != GSM_READY) ||
           (gprs.attachGPRS(SECRET_GPRS_APN, SECRET_GPRS_LOGIN, SECRET_GPRS_PASSWORD) != GPRS_READY)) 
    {
		#ifdef DEVMODE 
		Serial.println("[DEBUG]: Not connected");
		#endif
		delay(GSM_RECONNECT_INTERVAL);
    }
    #ifdef DEVMODE
    Serial.println("[DEBUG]: connected.");
    #endif
}


void connect_to_azure()
{
	uint32_t connect_start_ms = millis();
	uint32_t previous_connect_ms;
	int mqtt_connected = 0;

    while (1)
    {
		if (millis() - connect_start_ms > MQTT_RECONNECT_TIMEOUT)
		{
			#ifdef DEVMODE
			Serial.println("[DEBUG]: MQTT reached timeout for reconnects."); // Todo - handle this state
			#endif
			break;
		}
    	
    	if (millis() - previous_connect_ms > MQTT_RECONNECT_INTERVAL)
    	{
    		#ifdef DEVMODE 
			Serial.println("[DEBUG]: Attempting to connect to the MQTT broker... ");
    		#endif
    		
    		previous_connect_ms = millis();
    		
    		if (!mqttClient.connect(SECRET_BROKER, MQTT_PORT))
    		{
    			#ifdef DEVMODE #endif
		    	Serial.print("[ERROR]: MQTT ran in to a problem. Error code: ");
		        Serial.println(mqttClient.connectError());
		        #endif
    		}
    		else
    		{
    			#ifdef DEVMODE 
				Serial.println("[DEBUG]: Connection to MQTT broker successful.");
    			#endif
    			break;
    		}
    	}
    }
}


void mqtt_send(char* msg)
{
    mqttClient.beginMessage("devices/" + deviceId + "/messages/events/");
    mqttClient.print(msg);
    mqttClient.endMessage();
}


void mqtt_recieve(int size)
{
	#ifdef DEVMODE 
	Serial.print("Recieved message. Topic: ");
	Serial.println(mqttClient.messageTopic());
	#endif

	while(mqttClient.available())
	{
		#ifdef DEVMODE 
		Serial.print((char)mqttClient.read());
		#endif
	}
	#ifdef DEVMODE
	Serial.println();
	#endif
}


unsigned long getGsmTime()
{
	return gsmAccess.getTime();
}


void loop() 
{
    static uint32_t last_publish;

	if (gsmAccess.status() != GSM_READY || gprs.status() != GPRS_READY)
	{
		connect_to_gsm();
	}

	if (!mqttClient.connected())
	{
		connect_to_azure();
	}

	mqttClient.poll();

	if (millis() - last_publish > PUBLISH_INTERVAL)
	{
		#ifdef DEVMODE 
		Serial.println("[DEBUG]: Publishing message");
		#endif
		mqtt_send("Hello from device");
		last_publish = millis();
	}

	#ifdef DEVMODE
	Serial.println("\n\n[INFO]: === Runtime completed. To try again, restart device ===");
	while(1){};
	#endif
}