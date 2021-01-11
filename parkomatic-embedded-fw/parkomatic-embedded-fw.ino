#include <MKRGSM.h>
#include <ArduinoMqttClient.h>
#include <ArduinoBearSSL.h>
#include <ArduinoECCX08.h>
#include <utility/ECCX08SelfSignedCert.h>
#include <ArduinoMqttClient.h>
#include "defines.h" 

/* Global constants */

const char PINNUMBER[]     = SECRET_PINNUMBER;
const char GPRS_APN[]      = SECRET_GPRS_APN;
const char GPRS_LOGIN[]    = SECRET_GPRS_LOGIN;
const char GPRS_PASSWORD[] = SECRET_GPRS_PASSWORD;

/* GSM connectivity singletons */
GPRS gprs;
GSM gsmAccess;

GSMClient gsmClient;
BearSSLClient sslClient(gsmClient);
MqttClient mqttClient(sslClient);

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

    /* Set a callback to get the current time
       used to validate the servers certificate */
    ArduinoBearSSL.onGetTime(gsmAccess.getTime);

    /* Set the public key to be used with the certificate 
       in the ECCX08 slot */
    sslClient.setEccSlot(0,
                        ECCX08SelfSignedCert.bytes(),
                        ECCX08SelfSignedCert.length());

    /* Use the deiceId define as the MQTT client id */
    mqttClient.setId(deviceId);

    sprintf(mqtt_username_buf, 
            "%s/%s/api-version=2018-06-30", 
            SECRET_BROKER, 
            SECRET_DEVICE_ID);

    mqttClient.setUsernamePassword(mqtt_username_buf, "");

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
    while (!mqttClient.connect(broker, MQTT_PORT))
    {
        Serial.print(".");
        Serial.println(mqttClient.connectError());
			#ifdef DEVMODE
			Serial.println("[DEBUG]: MQTT reached timeout for reconnects."); // Todo - handle this state
			#endif
			break;
    		#ifdef DEVMODE 
			Serial.println("[DEBUG]: Attempting to connect to the MQTT broker... ");
    		#endif
    			#ifdef DEVMODE #endif
		    	Serial.print("[ERROR]: MQTT ran in to a problem. Error code: ");
		        Serial.println(mqttClient.connectError());
		        #endif
    			#ifdef DEVMODE 
				Serial.println("[DEBUG]: Connection to MQTT broker successful.");
    			#endif
    			break;
    }

    /* Subscribe to MQTT topic */
    mqttClient.subscribe("devices/" + deviceId + "/messages/devicebound/#");
}


void mqtt_send(char* msg)
{
    mqttClient.beginMessage("devices/" + deviceId + "/messages/events/");
    mqttClient.print(*msg);
    mqttClient.print(millis());
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

    http_connect();
    
    while(millis() - poll_start < POLL_TIME_LIMIT)
    {
        if (client.available())
        {
            char c = client.read();
            Serial.print(c);
        }

        if (!client.available() && !client.connected()) 
        {
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