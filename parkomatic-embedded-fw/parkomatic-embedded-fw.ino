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
    char mqtt_username_buf[100];

    Serial.begin(2000000);

    #ifdef DEBUG
    while (!Serial) {}
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
    bool connected = false;

    while ((gsmAccess.begin(PINNUMBER) != GSM_READY) ||
           (gprs.attachGPRS(GPRS_APN, GPRS_LOGIN, GPRS_PASSWORD) != GPRS_READY)) 
    {
      Serial.println("Not connected");
      delay(1000);
    }

    Serial.println("Connected to GSM");
}


void connect_to_azure()
{
    while (!mqttClient.connect(broker, MQTT_PORT))
    {
        Serial.print(".");
        Serial.println(mqttClient.connectError());
        delay(5000); 
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
	Serial.print("Recieved message. Topic: ");
	Serial.println(mqttClient.messageTopic());

	while(mqttClient.available())
	{
		Serial.print((char)mqttClient.read());
	}
	Serial.println();
}


void loop() 
{
    uint32_t poll_start = millis();

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
            Serial.println();
            Serial.println("disconnecting.");
            client.stop();
            break;          
        }       
    }
    Serial.println("done, softlocking =)");
    while(1){}
}